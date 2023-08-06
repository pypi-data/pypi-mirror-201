from os.path import join as path_join
from typing import List, Any

import faiss
import httpx
import numpy as np
from httpx import AsyncClient


class LaningFaissError(Exception):
    ...


class Requester:
    def __init__(self, base_url: str, timeout):
        self.base_url = base_url
        self.timeout = timeout

    async def request(self, method, url, retry=3, **kwargs):
        response = None
        exc = None
        for _ in range(retry):
            try:
                async with AsyncClient() as client:
                    response = await client.request(method, url, **kwargs)
                    break
            except Exception as e:
                print(f"laningfaiss exception {e}. Retrying.")
                exc = e

        if response is None:
            raise LaningFaissError(f"IO Error: {url}: {exc}")
        return response

    @staticmethod
    def parse(response):
        assert response.status_code == 200, f"{response.status_code} {response.reason_phrase}"
        data = response.json()
        assert data["code"] == 0, data["msg"]
        return data

    async def get(self, path: str, json=None):
        url = path_join(self.base_url, path)
        resp = await self.request("GET", url, json=json, timeout=self.timeout)
        return self.parse(resp)

    async def post(self, path: str, json=None):
        url = path_join(self.base_url, path)
        resp = await self.request("POST", url, json=json, timeout=self.timeout)
        return self.parse(resp)

    async def close(self):
        pass


class RequesterContext(Requester):
    def __init__(self, base_url: str, timeout):
        super().__init__(base_url, timeout)
        self.client = AsyncClient(
            timeout=timeout,
            # limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
        )

    async def request(self, method, url, retry=3, **kwargs):
        response = None
        exc = None
        for _ in range(retry):
            try:
                response = await self.client.request(method, url, **kwargs)
                break
            except Exception as e:
                print(f"laningfaiss exception {e}. Retrying.")
                exc = e

        if response is None:
            raise LaningFaissError(f"IO Error: {url}: {exc}")
        return response

    async def close(self):
        await self.client.aclose()


class Router:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.requester = Requester(base_url, timeout)

    async def __aenter__(self, *args, **kwargs):
        self.requester = RequesterContext(self.base_url, self.timeout)
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.requester.close()

    async def deduplication(self, vectors: List[List[float]], threshold: float, norm: bool = True):
        """
        向量去重

        :param norm:
        :param threshold:
        :param vectors:
        :return: List[Tuple[id, sim]]  eg: [(id, sim), (), ...]
        """
        faiss_index = faiss.IndexIDMap2(faiss.IndexFlatIP(512))
        xb = np.asarray(vectors).astype('float32')
        if norm:
            xb = xb / np.linalg.norm(xb, axis=1).reshape(xb.shape[0], 1)

        ids = list(range(xb.shape[0]))
        ids_array = np.asarray(ids).astype('int64')
        faiss_index.add_with_ids(xb, ids_array)

        mapping = {}
        for v, n in zip(xb, ids):
            v = np.asarray([v])
            lims, D, I = faiss_index.range_search(v, threshold)
            mapping[n] = I[0]

        number_list = list(set(mapping.values()))
        searching_vectors = np.empty((0, 512), dtype=np.float64)
        for n in number_list:
            searching_vectors = np.append(searching_vectors, [xb[n]], axis=0)

        payloads = {
            "vectors": searching_vectors.tolist(),
            "radius": threshold
        }
        response = await self.requester.post("range_search", json=payloads)
        res = response["data"]["res"]
        assert len(res) == searching_vectors.shape[0], \
            f"The response of engine is incomplete. expect {searching_vectors.shape[0]} but {len(res)}"

        searched_mapping = {}
        for ftr_cmp_res, m in zip(res, number_list):
            if ftr_cmp_res:
                vid = ftr_cmp_res[0][0]
                sim = ftr_cmp_res[0][1]
                searched_mapping[m] = (vid, sim)
            else:
                searched_mapping[m] = ()

        results = []
        for n in ids:
            m = mapping[n]
            searched = searched_mapping[m]
            if searched:
                results.append((searched[0], searched[1]))
            else:
                results.append(())

        return results

    async def ntotal(self) -> int:
        """
        查询索引中向量的数量

        :return: int
        """
        response = await self.requester.get("ntotal")
        ntotal = response["data"]["ntotal"]
        return int(ntotal)

    async def add(self, ids: List[int], vectors: List[List], train: bool = True, norm: bool = True):
        """
        批量添加向量

        :param ids: 向量id
        :param vectors: 二维向量列表，类型可以是float64,uint8等
        :param train: 是否train， 将质心添加到索引中
        :param norm: 是否要做归一化
        :return: (是否成功: bool, 错误信息: str)

        """
        assert len(ids) == len(vectors), "维度不同"
        assert len(ids) > 0, "数据不能为空"

        vectors_arr = np.array(vectors)
        if norm:
            vectors_arr = vectors_arr / np.linalg.norm(vectors_arr, axis=1).reshape(vectors_arr.shape[0], 1)
        payloads = {
            "ids": ids,
            "vectors": vectors_arr.tolist(),
            "train": train
        }
        try:
            await self.requester.post("add", json=payloads)
            return True, None

        except Exception as e:
            return False, str(e)

    async def search(self, vectors: List[List], top_k: int, norm=True) -> List[List[List]]:
        """
        搜索并返回topk结果

        :param vectors: 二维向量列表
        :param top_k: topk的k
        :param norm: 是否要做归一化
        :return: List[List[List(id: int64, sim: float)]]
        """
        assert len(vectors) > 0, "数据不能为空"
        vectors_arr = np.array(vectors)
        if norm:
            vectors_arr = vectors_arr / np.linalg.norm(vectors_arr, axis=1).reshape(vectors_arr.shape[0], 1)

        payloads = {
            "vectors": vectors_arr.tolist(),
            "k": top_k
        }
        response = await self.requester.post("search", json=payloads)
        res = response["data"]["res"]
        for ftr_cmp_res in res:
            for pair in ftr_cmp_res:
                pair[1] = round(pair[1], 3)
        return res

    async def range_search(self, vectors: List[List], radius: Any, norm=True) -> List:
        """
        搜索并返回范围内的结果

        :param vectors: 二维向量列表
        :param radius: 范围值
        :param norm: 是否要做归一化
        :return: List[List[List(id: int64, sim: float)]]
        """
        assert len(vectors) > 0, "数据不能为空"
        vectors_arr = np.array(vectors)
        if norm:
            vectors_arr = vectors_arr / np.linalg.norm(vectors_arr, axis=1).reshape(vectors_arr.shape[0], 1)

        payloads = {
            "vectors": vectors_arr.tolist(),
            "radius": radius
        }
        response = await self.requester.post("range_search", json=payloads)
        res = response["data"]["res"]
        for ftr_cmp_res in res:
            for pair in ftr_cmp_res:
                pair[1] = round(pair[1], 3)
        return res

    async def remove(self, ids: List[int]):
        """
        根据id删除向量

        :param ids: 向量id列表
        :return: (是否成功: bool, 错误信息: str)
        """
        assert len(ids) > 0, "数据不能为空"
        payloads = {
            "ids": ids,
        }
        try:
            await self.requester.post("remove", json=payloads)
            return True, None

        except Exception as e:
            return False, str(e)

    async def reconstruct(self, ids) -> List[List]:
        """
        根据ids重建向量

        :param ids: 向量id列表
        :return: 二维向量列表，如果向量不存在，返回多个空列表([[], [], [] ...])
        """
        payloads = {
            "ids": ids,
        }
        response = await self.requester.post("reconstruct", json=payloads)
        vectors = response["data"]["vectors"]
        return vectors

    async def register(self, bucket_name: str, object_name: str):
        """
        注册只读索引，每次只注册一个

        :param bucket_name: minio桶名
        :param object_name: 对象路径
        :return:
        """
        payloads = {
            "bucket_name": bucket_name,
            "object_name": object_name,
        }
        try:
            await self.requester.post("register", json=payloads)
            return True, None
        except Exception as e:
            return False, str(e)

    async def cancel(self, bucket_name: str, object_name: str):
        """
        删除只读索引，每次只删除一个

        :param bucket_name: minio桶名
        :param object_name: 对象路径
        :return:
        """
        payloads = {
            "bucket_name": bucket_name,
            "object_name": object_name,
        }
        try:
            await self.requester.post("cancel", json=payloads)
            return True, None
        except Exception as e:
            return False, str(e)

    async def info(self) -> tuple:
        """
        获取索引相关信息

        :return: (项目名称, minio地址, 存储到minio的周期<秒>)
        """
        response = await self.requester.get("info")
        data = response["data"]
        return data["name"], data["minio_addr"], data["save_period"]

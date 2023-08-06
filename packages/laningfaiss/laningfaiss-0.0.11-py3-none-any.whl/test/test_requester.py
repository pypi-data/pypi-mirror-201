import time

import numpy as np
import pytest

from laningfaiss import requester
from lib.mock import http_mock

features: list = np.random.rand(10, 512).astype("float64").tolist()


@pytest.mark.asyncio
async def test_ntotal_1():
    with http_mock() as mock:
        mock.register_once('/ntotal', {
            "code": 0,
            "msg": "",
            "data": {
                "ntotal": 123
            }
        }, method="GET")

        router = requester.Router("http://mock")
        ntotal = await router.ntotal()

    assert ntotal == 123


@pytest.mark.asyncio
async def test_add_1():
    with http_mock() as mock:
        mock.register_once('/add', {
            "code": 0,
            "msg": "",
        })

        router = requester.Router("http://mock")
        res = await router.add([1, 2], [features[0], features[1]], True)

    assert res[0] is True


@pytest.mark.asyncio
async def test_add_2():
    with http_mock() as mock:
        mock.register_once('/add', {
            "code": 1,
            "msg": "error message",
        })

        router = requester.Router("http://mock")
        res = await router.add([1, 2], [features[0], features[1]], True)

    assert res[0] is False
    assert res[1] == "error message"


@pytest.mark.asyncio
async def test_add_3():
    router = requester.Router("http://mock")
    res = await router.add([1, 2], [features[0], features[1]], True)
    assert res[0] is False
    assert res[1] == "404 Not Found"


@pytest.mark.asyncio
async def test_add_4():
    router = requester.Router("http://mock")
    with pytest.raises(AssertionError):
        res = await router.add([1], [features[0], features[1]], True)


@pytest.mark.asyncio
async def test_add_5():
    router = requester.Router("http://mock")
    with pytest.raises(AssertionError):
        res = await router.add([], [], True)


@pytest.mark.asyncio
async def test_search_1():
    with http_mock() as mock:
        mock.register_once('/search', {
            "code": 0,
            "msg": "",
            "data": {
                "res": [[(1, 0.8), (2, 0.7543)]]
            }
        })

        router = requester.Router("http://mock/")
        res = await router.search([features[0]], 2)

    assert res == [[[1, 0.8], [2, 0.754]]]


@pytest.mark.asyncio
async def test_range_search_1():
    with http_mock() as mock:
        mock.register_once('/range_search', {
            "code": 0,
            "msg": "",
            "data": {
                "res": [[(1, 0.8), (2, 0.7543)], []]
            }
        })

        router = requester.Router("http://mock/")
        res = await router.range_search([features[0], features[1]], 0.8)

    assert res == [[[1, 0.8], [2, 0.754]], []]


@pytest.mark.asyncio
async def test_remove_1():
    with http_mock() as mock:
        mock.register_once('/remove', {
            "code": 0,
            "msg": ""
        })

        router = requester.Router("http://mock/")
        res = await router.remove([1, 2, 3])

    assert res[0] is True


@pytest.mark.asyncio
async def test_reconstruct_1():
    with http_mock() as mock:
        mock.register_once('/reconstruct', {
            "code": 0,
            "msg": "",
            "data": {
                "vectors": [features[0], [], features[1]]
            }
        })

        router = requester.Router("http://mock/")
        res = await router.reconstruct([1, 2, 3])

    assert len(res) == 3


@pytest.mark.asyncio
async def test_register_1():
    with http_mock() as mock:
        mock.register_once('/register', {
            "code": 0,
            "msg": ""
        })

        router = requester.Router("http://mock/")
        res = await router.register("bucket", "/a/b/c/1.dat")
    assert res[0] is True


@pytest.mark.asyncio
async def test_cancel_1():
    with http_mock() as mock:
        mock.register_once('/cancel', {
            "code": 0,
            "msg": ""
        })

        router = requester.Router("http://mock/")
        res = await router.cancel("bucket", "/a/b/c/1.dat")
    assert res[0] is True


@pytest.mark.asyncio
async def test_info_1():
    with http_mock() as mock:
        mock.register_once('/info', {
            "code": 0,
            "msg": "",
            "data": {
                "name": "test",
                "minio_addr": "0.0.0.0",
                "save_period": 3600
            }
        }, method="GET")

        router = requester.Router("http://mock/")
        name, minio_addr, save_period = await router.info()

    assert name == "test"
    assert minio_addr == "0.0.0.0"
    assert save_period == 3600


@pytest.mark.asyncio
async def test_deduplication_1():
    vectors = [
        features[0], features[1], features[1]
    ]
    with http_mock() as mock:
        mock.register_once('/range_search', {
            "code": 0,
            "msg": "",
            "data": {
                "res": [[(1, 0.8), (2, 0.7543)], []]
            }
        })
        _time_start = time.time()
        async with requester.Router("http://mock/") as router:
            for _ in range(100):
                res = await router.deduplication(vectors, 0.8)
        _time_end = time.time()
        time_delta_1 = _time_end - _time_start
        print("Time_1", time_delta_1)

        router = requester.Router("http://mock/")
        _time_start = time.time()
        for _ in range(100):
            res = await router.deduplication(vectors, 0.8)
        _time_end = time.time()
        time_delta_2 = _time_end - _time_start
        print("Time_2", time_delta_2)

    assert res == [(1, 0.8), (), ()]
    # assert time_delta_2 > time_delta_1

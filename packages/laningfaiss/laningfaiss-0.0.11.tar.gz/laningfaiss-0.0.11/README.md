# Laning Faiss

### Example

```python
import asyncio
import laningfaiss

faiss = laningfaiss.Router("http://faiss-svc:8000")


async def main():
    ntotal = await faiss.ntotal()
    print(ntotal)
    # Output: 16

    search_res = await faiss.range_search([...], 0.8)
    print(search_res)
    # Output: [[1, 0.8587932], [2, 0.999999]]


if __name__ == '__main__':
    asyncio.run(main())

```

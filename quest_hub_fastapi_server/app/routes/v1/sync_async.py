from time import sleep as sync_sleep
from fastapi import APIRouter, BackgroundTasks
from starlette.concurrency import run_in_threadpool
from asyncio import sleep as async_sleep, gather, create_task


route = APIRouter(prefix="/sync-async", tags=["/sync-async"])


def test_sync(title: str):
    for i in range(10):
        print(f"{title} - {i}")
        sync_sleep(1)


@route.get(path="/sync")
def test_sync_point():
    test_sync("test_sync_point")  # корретно


async def test_async(title: str):
    for i in range(10):
        print(f"{title} - {i}")
        await async_sleep(1)


@route.get(path="/async")
async def test_async_point(background_tasks: BackgroundTasks):
    # корретно
    await test_async("test_async_point")
    # ошибка
    # test_sync("test_async_point")

    # asyncio.gather - корретно
    # task_1 = create_task(test_async("test_async_point"))
    # await gather(task_1)

    # run_in_threadpool - корретно
    # await run_in_threadpool(test_sync, "test_async_point")

    # BackgroundTasks - корректно
    # background_tasks.add_task(test_async, "test_async_point")

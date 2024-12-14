from time import sleep as sync_sleep
from fastapi import APIRouter
from asyncio import sleep as async_sleep


route = APIRouter(prefix="/sync-async", tags=["/sync-async"])


def test_sync(title: str):
    """Тестовая синхронная функция"""
    for i in range(10):
        print(f"{title} - {i}")
        sync_sleep(1)


async def test_async(title: str):
    """Тестовая асинхронная функция"""
    for i in range(10):
        print(f"{title} - {i}")
        await async_sleep(1)


@route.get(path="/sync")
def test_sync_point():
    test_sync("test_sync_point")


@route.get(path="/async")
async def test_async_point():
    # корретно
    await test_async("test_async_point")
    # ошибка
    # test_sync("test_async_point")

    # run_in_threadpool
    # await run_in_threadpool(test_sync, "test_async_point")

    # asyncio.gather
    # profile_task = create_task(test_async("profile_task"))
    # char_task = create_task(test_async("char_task"))
    # await gather(profile_task, char_task)

    # BackgroundTasks
    # background_tasks.add_task(test_async, "test_async_point")

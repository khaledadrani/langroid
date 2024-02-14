import asyncio
import time


def default_test_sync_callback(token: str):
    print(token, end='')
    time.sleep(0.05)


async def default_test_async_callback(token: str):
    print(token, end='')
    await asyncio.sleep(0.05)

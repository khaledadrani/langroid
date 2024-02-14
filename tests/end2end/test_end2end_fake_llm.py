import time

import pytest

from source.configuration.config import CommonConfig
from source.domain.implementations.fake_llm import FakeListLLM


def test_synchronous_generation():
    llm = FakeListLLM(CommonConfig())

    def default_test_sync_callback(token: str) -> None:
        print(token, end='')
        time.sleep(0.0001)

    response = ''
    for token in llm.generate('Blue Whales are the biggest animal to ever inhabit the Earth.',
                              callback=default_test_sync_callback):
        response += token

    assert isinstance(response, str) and len(response) > 5


@pytest.mark.asyncio
async def test_asynchronous_generation():
    llm = FakeListLLM(CommonConfig())

    async def default_test_sync_callback(token: str) -> None:
        print(token, end='')
        time.sleep(0.0001)

    response = await llm.stream('Blue Whales are the biggest animal to ever inhabit the Earth.',
                                callback=default_test_sync_callback)

    response = str(response)

    assert isinstance(response, str) and len(response) > 5

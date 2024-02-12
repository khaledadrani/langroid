import time

import pytest

from source.configuration.config import CommonConfig
from source.domain.implementations.fake_llm import FakeListLLM


def test_synchronous_generation():
    llm = FakeListLLM(CommonConfig())

    def default_test_sync_callback(token: str) -> None:
        print(token, end='')
        time.sleep(0.0001)

    text = ''
    for token in llm._generate('Blue Whales are the biggest animal to ever inhabit the Earth.',
                               callback=default_test_sync_callback):
        text += token

    assert text and isinstance(text, str)


@pytest.mark.asyncio
async def test_asynchronous_generation():
    llm = FakeListLLM(CommonConfig())

    async def default_test_sync_callback(token: str) -> None:
        print(token, end='')
        time.sleep(0.0001)

    response = await llm._stream('Blue Whales are the biggest animal to ever inhabit the Earth.',
                                 callback=default_test_sync_callback)

    assert str(response)

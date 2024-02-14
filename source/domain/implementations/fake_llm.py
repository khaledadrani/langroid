"""Fake LLM wrapper for testing purposes."""
import random
from typing import Generator

from source.configuration.config import CommonConfig
from source.domain.interfaces.base_llm import BaseLLM
from source.schema.common_schema import AsyncFunctionType


class FakeListLLM(BaseLLM):
    """Fake LLM wrapper for testing purposes."""

    def __init__(self, config: CommonConfig):
        super().__init__(config)
        self.responses = [
            "Hello World",
            "Hi, I am fine thank you!"
        ]

    def generate(
            self,
            prompt: str,
            callback: AsyncFunctionType = None,
            **kwargs
    ) -> Generator[str, None, None]:
        """Return next response"""
        response = random.choice(self.responses)
        for token in response:
            if callback:
                callback(token)
            yield token

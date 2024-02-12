from typing import Callable, Generator

from gpt4all import GPT4All

from source.configuration.config import LLMConfig
from source.domain.interfaces.base_llm import BaseLLM
from source.schema.common_schema import AsyncFunctionType


class GPT4AllLLM(BaseLLM):
    def __init__(self, config: LLMConfig):
        super().__init__(config=config)
        self.model = GPT4All(model_name=config.MODEL_NAME, model_path=config.MODEL_PATH)

    def _generate(self, prompt: str, callback: Callable = None) -> Generator[str, None, None]:
        # TODO should accept arguments from either constructor or method call
        for token in self.model.generate(prompt=prompt,
                                         max_tokens=256,
                                         streaming=True,
                                         repeat_penalty=5.0
                                         ):
            if callback:
                callback(token)
            yield token

    # async def _stream(self, prompt: str, callback: AsyncFunctionType = None):
    #
    #     for token in self.model.generate(prompt=prompt,
    #                                      temp=0,):
    #         if callback:
    #             await callback(token)
    #
    #         yield token

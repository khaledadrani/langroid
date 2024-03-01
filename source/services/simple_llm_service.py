import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Dict, Optional, AsyncGenerator

from loguru import logger
from starlette.requests import Request

from source.configuration.config import LLMConfig
from source.domain.implementations.fake_llm import FakeListLLM
from source.domain.implementations.gpt4all_llm import GPT4AllLLM
from source.domain.interfaces.base_llm import BaseLLM
from source.schema.common_schema import SupportedLLModelsEnum


class LLMService:
    def __init__(self):
        self.model_factory: Dict[SupportedLLModelsEnum, BaseLLM] = {
            SupportedLLModelsEnum.GPT_4ALL: GPT4AllLLM(LLMConfig()),
            SupportedLLModelsEnum.FAKE: FakeListLLM(LLMConfig())
        }

    def _generate_answer(self,
                         prompt: str,
                         model_type: SupportedLLModelsEnum,
                         model_params: dict
                         ) -> str:

        result = self.model_factory[model_type].generate(prompt=prompt, **model_params)

        return "".join(tuple(result))

    async def generate_answer(self,
                              prompt: str,
                              model_type: SupportedLLModelsEnum,
                              model_params: Optional[dict] = None):

        if not model_params:
            model_params = {}

        with ProcessPoolExecutor() as executor:
            text = await asyncio.get_event_loop().run_in_executor(executor,
                                                                  self._generate_answer,
                                                                  prompt, model_type,
                                                                  model_params
                                                                  )

        return {
            "response": text
        }

    async def stream_response(self, request: Request, prompt: str,
                              model_type: SupportedLLModelsEnum,
                              model_params: Optional[dict] = None) -> AsyncGenerator:

        model_wrapper = self.model_factory[model_type]

        async for token in model_wrapper.stream(prompt=prompt):
            print(token)
            if await request.is_disconnected():
                logger.warning("Connection disconnected, end streaming!")
                return
            yield token

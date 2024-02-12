import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Dict

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

    def _generate_answer(self, prompt: str, model_type: SupportedLLModelsEnum) -> str:
        result = self.model_factory[model_type].generate(prompt=prompt)

        return "".join(tuple(result))

    async def generate_answer(self, prompt: str, model_type: SupportedLLModelsEnum):
        with ProcessPoolExecutor() as executor:
            text = await asyncio.get_event_loop().run_in_executor(executor,
                                                                  self._generate_answer,
                                                                  prompt, model_type)

        return {
            "response": text
        }

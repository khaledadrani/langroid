from typing import Optional

from pydantic import BaseModel, Field

from source.configuration.constants import gpt4all_mistral_prompt_example
from source.schema.common_schema import SupportedLLModelsEnum


class LLMParams(BaseModel): #TODO common Params then translate for each model (mapper?)
    temp: Optional[int] = 0 # temp specific to gpt4all
    repeat_penalty: Optional[float] = 5


class SimpleLLMRequest(BaseModel):
    prompt: str = Field(examples=[gpt4all_mistral_prompt_example])
    llm_type: SupportedLLModelsEnum = Field(examples=[SupportedLLModelsEnum.GPT_4ALL])
    params: Optional[LLMParams] = None

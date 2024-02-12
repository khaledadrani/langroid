from pydantic import BaseModel, Field

from source.schema.common_schema import SupportedLLModelsEnum

gpt4all_mistral_template = '''
<|im_start|>system
{system_message}<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
'''
gpt4all_mistral_prompt = '''
<|im_start|>system
You are a researcher in Harverd with great knowledge about all domains<|im_end|>
<|im_start|>user
Please provide a brief summary of the book "1984" by George Orwell.<|im_end|>
assistant
'''


class SimpleLLMRequest(BaseModel):
    prompt: str = Field(examples=[gpt4all_mistral_prompt])
    llm_type: SupportedLLModelsEnum = Field(examples=[SupportedLLModelsEnum.GPT_4ALL])

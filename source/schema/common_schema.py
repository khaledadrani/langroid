from enum import Enum
from typing import Callable, Any, Awaitable


class SupportedLLModels(str, Enum):
    gpt4all = "GPT4ALL"
    fake = "FAKE"
    gpt2 = "GPT2"
    falcon = "FALCON"
    llama_cpp = "LlamaCpp"
    open_ai = "OpenAI"


AsyncFunctionType = Callable[[Any, Any], Awaitable[Any]]
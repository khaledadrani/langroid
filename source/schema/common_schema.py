from enum import Enum
from typing import Callable, Any, Awaitable


class SupportedLLModelsEnum(str, Enum):
    GPT_4ALL = "GPT4ALL"
    FAKE = "FAKE"
    # gpt2 = "GPT2" #TODO
    # falcon = "FALCON"
    # llama_cpp = "LlamaCpp"
    # open_ai = "OpenAI"


AsyncFunctionType = Callable[[Any, Any], Awaitable[Any]]
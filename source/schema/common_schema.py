from enum import Enum
from typing import Callable, Any, Awaitable


class SupportedLLModelsEnum(str, Enum):
    GPT_4ALL = "GPT4ALL"
    FAKE = "FAKE"


AsyncFunctionType = Callable[[Any, Any], Awaitable[Any]]

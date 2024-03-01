from abc import abstractmethod, ABC
from typing import Callable, Generator, Optional, Union, AsyncGenerator

from pydantic_settings import BaseSettings

from source.schema.common_schema import AsyncFunctionType


class BaseLLM(ABC):
    def __init__(self, config: BaseSettings):
        self.config = config

    @abstractmethod
    def generate(self,
                 prompt: str,
                 callback: Optional[Union[Callable, None]] = None,
                 **kwargs) -> Generator[str, None, None]:
        raise NotImplementedError()

    async def stream(self, prompt: str, callback: AsyncFunctionType = None, **kwargs) -> AsyncGenerator[str, None]:
        raise NotImplementedError()

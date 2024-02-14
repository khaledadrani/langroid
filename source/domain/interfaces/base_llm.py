import asyncio
from abc import abstractmethod, ABC
from typing import Callable, Generator, Optional, Union

from pydantic_settings import BaseSettings

from source.schema.common_schema import AsyncFunctionType


class BaseLLM(ABC):
    def __init__(self, config: BaseSettings):
        self.config = config

    @abstractmethod
    def generate(self, prompt: str, callback: Optional[Union[Callable, None]] = None, **kwargs) -> Generator[str, None, None]:
        raise NotImplementedError()

    async def stream(self, prompt: str, callback: AsyncFunctionType = None,  **kwargs) -> Generator[str, None, None]:
        """
        Default implementation for _stream
        TODO it will not work with an asynchronous callback
        """
        return await asyncio.get_running_loop().run_in_executor(
            None, self.generate, prompt, callback
        )

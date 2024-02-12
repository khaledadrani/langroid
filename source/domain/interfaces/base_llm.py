import asyncio
from abc import abstractmethod, ABC
from typing import Callable, Generator, Awaitable, Optional, Union

from pydantic_settings import BaseSettings


class BaseLLM(ABC):
    def __init__(self, config: BaseSettings):
        self.config = config

    @abstractmethod
    def _generate(self, prompt: str, callback: Optional[Union[Callable, None]] = None) -> Generator[str, None, None]:
        raise NotImplementedError()

    async def _stream(self, prompt: str, callback: Optional[Union[Awaitable, None]] = None) -> Generator[
        str, None, None]:
        """
        Default implementation for _stream
        """
        return await asyncio.get_running_loop().run_in_executor(
            None, self._generate, prompt, callback
        )

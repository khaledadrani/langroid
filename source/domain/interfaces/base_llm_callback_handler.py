from typing import Any, Union


class BaseCallbackHandler:
    """Base callback handler that can be used to handle callbacks from langchain."""

    def on_llm_start(
            self, prompt: str
    ) -> Any:
        """Run when LLM starts running."""

    def on_llm_new_token(self, token: str) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""

    def on_llm_end(self, text: str) -> Any:
        """Run when LLM ends running."""

    def on_llm_error(
            self,
            error: Union[Exception, KeyboardInterrupt],
            last_token: Union[str, None],
            text: Union[str, None]
    ) -> Any:
        """Run when LLM errors."""


class BaseAsyncCallbackHandler:
    """Base callback handler that can be used to handle callbacks from langchain."""

    async def on_llm_start(
            self, prompt: str
    ) -> Any:
        """Run when LLM starts running."""

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        """Run on new LLM token. Only available when streaming is enabled."""

    async def on_llm_end(self,
                         error: Union[Exception, KeyboardInterrupt],
                         last_token: Union[str, None],
                         text: Union[str, None]) -> Any:
        """Run when LLM ends running."""

    async def on_llm_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""

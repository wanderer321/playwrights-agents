"""Base provider interface."""

from abc import ABC, abstractmethod
from typing import AsyncIterator


class LLMProvider(ABC):
    """Abstract base for all LLM providers."""

    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        stream: bool = False,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str | AsyncIterator[str]:
        """Send a chat completion request.

        Returns:
            If stream=False: the full response text as a string.
            If stream=True: an async iterator yielding text chunks.
        """
        ...

    @abstractmethod
    async def list_models(self) -> list[str]:
        """Return available model names."""
        ...

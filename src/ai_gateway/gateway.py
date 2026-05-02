"""AI Gateway — unified entry point for all LLM calls."""

from typing import AsyncIterator

from src.ai_gateway.providers.aliyun import AliyunProvider
from src.ai_gateway.providers.anthropic import AnthropicProvider
from src.ai_gateway.providers.base import LLMProvider
from src.ai_gateway.providers.openai_compat import OpenAICompatProvider


class AIGateway:
    """Singleton-style gateway that dispatches to the configured provider."""

    def __init__(self, config: dict):
        self.config = config
        self._provider: LLMProvider | None = None

    def _get_provider(self) -> LLMProvider:
        if self._provider is not None:
            return self._provider

        ai_cfg = self.config.get("ai", {})
        provider_name = ai_cfg.get("provider", "aliyun")
        model = ai_cfg.get("model", "glm-5")
        api_key = ai_cfg.get("api_key", "")
        base_url = ai_cfg.get("base_url", "")

        if provider_name == "aliyun":
            self._provider = AliyunProvider(api_key=api_key or "", model=model)
        elif provider_name == "anthropic":
            base = base_url or "https://api.anthropic.com"
            self._provider = AnthropicProvider(api_key=api_key or "", base_url=base, model=model)
        elif provider_name == "openai_compat":
            base = base_url or "https://api.openai.com/v1"
            self._provider = OpenAICompatProvider(api_key=api_key or "", base_url=base, model=model)
        else:
            raise ValueError(f"Unknown AI provider: {provider_name}")

        return self._provider

    async def chat(
        self,
        messages: list[dict],
        stream: bool = False,
        max_tokens: int | None = None,
    ) -> str | AsyncIterator[str]:
        provider = self._get_provider()
        ai_cfg = self.config.get("ai", {})
        return await provider.chat(
            messages=messages,
            stream=stream,
            temperature=ai_cfg.get("temperature", 0.3),
            max_tokens=max_tokens or ai_cfg.get("max_tokens", 4096),
        )

    async def chat_str(self, messages: list[dict], max_tokens: int | None = None) -> str:
        """Convenience: non-streaming, returns a string."""
        result = await self.chat(messages, stream=False, max_tokens=max_tokens)
        assert isinstance(result, str)
        return result

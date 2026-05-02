"""Anthropic-compatible provider (works with DashScope Anthropic proxy)."""

import json
from typing import AsyncIterator

import httpx

from .base import LLMProvider


class AnthropicProvider(LLMProvider):
    """Provider for Anthropic-compatible APIs (including DashScope proxy)."""

    def __init__(self, api_key: str, base_url: str, model: str = "claude-sonnet-4-20250515"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=180)

    async def chat(
        self,
        messages: list[dict],
        stream: bool = False,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str | AsyncIterator[str]:
        # Convert OpenAI-format messages to Anthropic format
        system_msg = None
        anthropic_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system_msg = msg["content"]
            else:
                role = "assistant" if msg["role"] == "assistant" else "user"
                content = []
                if isinstance(msg["content"], str):
                    content = [{"type": "text", "text": msg["content"]}]
                elif isinstance(msg["content"], list):
                    content = msg["content"]
                anthropic_messages.append({"role": role, "content": content})

        payload = {
            "model": self.model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens or 4096,
        }
        if system_msg:
            payload["system"] = system_msg
        if temperature is not None:
            payload["temperature"] = temperature

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }

        if stream:
            return self._stream_chat(payload, headers)

        resp = await self._client.post("/v1/messages", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        # Extract text from Anthropic response
        content = data.get("content", [])
        if content and isinstance(content, list):
            return "".join(block.get("text", "") for block in content if block.get("type") == "text")
        return data.get("content", [{}])[0].get("text", "")

    async def _stream_chat(self, payload: dict, headers: dict) -> AsyncIterator[str]:
        async with self._client.stream(
            "POST", "/v1/messages", json=payload, headers=headers
        ) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        if chunk.get("type") == "content_block_delta":
                            delta = chunk.get("delta", {}).get("text", "")
                            if delta:
                                yield delta
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue

    async def list_models(self) -> list[str]:
        return [self.model]

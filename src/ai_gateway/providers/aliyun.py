"""阿里云百炼 (DashScope) provider implementation."""

import json
from typing import AsyncIterator

import httpx

from .base import LLMProvider


ALIYUN_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"


class AliyunProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "glm-5"):
        self.api_key = api_key
        self.model = model
        self._client = httpx.AsyncClient(base_url=ALIYUN_BASE, timeout=120)

    async def chat(
        self,
        messages: list[dict],
        stream: bool = False,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str | AsyncIterator[str]:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
        }
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        if stream:
            return self._stream_chat(payload, headers)

        resp = await self._client.post("/chat/completions", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    async def _stream_chat(self, payload: dict, headers: dict) -> AsyncIterator[str]:
        async with self._client.stream(
            "POST", "/chat/completions", json=payload, headers=headers
        ) as resp:
            resp.raise_for_status()
            async for line in resp.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        delta = chunk["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue

    async def list_models(self) -> list[str]:
        return [self.model]

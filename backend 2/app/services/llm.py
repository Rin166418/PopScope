from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import httpx

from app.core.config import Settings


@dataclass(slots=True)
class LLMResult:
    provider: str
    model_name: str | None
    text: str


class LLMClient(Protocol):
    async def generate(self, prompt: str) -> LLMResult:
        ...


class StubLLMClient:
    async def generate(self, prompt: str) -> LLMResult:
        text = (
            'Аналитический отчет сформирован в stub-режиме. '\
            'Подключите LLM-провайдер для расширенного текста.'
        )
        return LLMResult(provider='stub', model_name='stub-v1', text=text)


class YandexGPTClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def generate(self, prompt: str) -> LLMResult:
        if not self.settings.yandex_gpt_api_key or not self.settings.yandex_gpt_folder_id:
            raise ValueError('YandexGPT credentials are missing')

        model_uri = self.settings.yandex_gpt_model_uri_template.format(
            folder_id=self.settings.yandex_gpt_folder_id,
        )

        payload = {
            'modelUri': model_uri,
            'completionOptions': {
                'stream': False,
                'temperature': self.settings.yandex_gpt_temperature,
                'maxTokens': str(self.settings.yandex_gpt_max_tokens),
            },
            'messages': [{'role': 'user', 'text': prompt}],
        }

        headers = {
            'Authorization': f'Api-Key {self.settings.yandex_gpt_api_key}',
            'Content-Type': 'application/json',
        }

        async with httpx.AsyncClient(timeout=self.settings.yandex_gpt_timeout_seconds) as client:
            response = await client.post(
                self.settings.yandex_gpt_base_url,
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()

        alternatives = data.get('result', {}).get('alternatives', [])
        if not alternatives:
            raise ValueError('YandexGPT response does not contain alternatives')

        message_text = alternatives[0].get('message', {}).get('text', '').strip()
        if not message_text:
            raise ValueError('YandexGPT response message is empty')

        return LLMResult(
            provider='yandex',
            model_name=model_uri,
            text=message_text,
        )


def build_llm_client(settings: Settings) -> LLMClient:
    if not settings.report_use_llm:
        return StubLLMClient()
    if settings.llm_provider == 'yandex':
        return YandexGPTClient(settings)
    return StubLLMClient()

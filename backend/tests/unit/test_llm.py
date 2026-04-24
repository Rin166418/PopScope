from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.core.config import Settings
from app.services.llm import StubLLMClient, YandexGPTClient


@pytest.mark.asyncio
async def test_stub_llm_generate() -> None:
    client = StubLLMClient()
    result = await client.generate('prompt')

    assert result.provider == 'stub'
    assert 'stub' in result.model_name
    assert 'stub-режиме' in result.text


@pytest.mark.asyncio
async def test_yandex_llm_generate_parses_response() -> None:
    settings = Settings(
        YANDEX_GPT_API_KEY='token',
        YANDEX_GPT_FOLDER_ID='folder-id',
        LLM_PROVIDER='yandex',
    )
    client = YandexGPTClient(settings)

    mock_response = Mock()
    mock_response.json.return_value = {
        'result': {
            'alternatives': [
                {'message': {'text': 'Готовый отчет'}},
            ],
        },
    }
    mock_response.raise_for_status = Mock()

    with patch('httpx.AsyncClient.post', new=AsyncMock(return_value=mock_response)):
        result = await client.generate('prompt')

    assert result.provider == 'yandex'
    assert 'yandexgpt' in (result.model_name or '')
    assert result.text == 'Готовый отчет'


@pytest.mark.asyncio
async def test_yandex_llm_generate_raises_without_credentials() -> None:
    settings = Settings(LLM_PROVIDER='yandex')
    client = YandexGPTClient(settings)

    with pytest.raises(ValueError, match='credentials'):
        await client.generate('prompt')

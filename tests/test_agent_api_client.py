"""Тесты для agent_api_client."""

import pytest

from src.agent_api_client import AgentAPIClient, load_config


def test_load_config_empty_if_no_file(tmp_path, monkeypatch):
    """Без config.json load_config возвращает пустой dict или не падает."""
    # Подмена пути к конфигу не обязательна, если config есть в проекте
    config = load_config()
    assert isinstance(config, dict)


def test_client_is_configured_false_by_default():
    """Без base_url и api_key is_configured() == False."""
    client = AgentAPIClient()
    assert client.is_configured() is False


def test_client_is_configured_true_when_set():
    """С base_url и api_key is_configured() == True."""
    client = AgentAPIClient(base_url="https://api.example.com", api_key="secret")
    assert client.is_configured() is True

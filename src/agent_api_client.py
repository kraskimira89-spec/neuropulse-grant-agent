"""
Заготовка клиента для взаимодействия с API грантового агента.
Параметры подключения задаются в config/config.json или через переменные окружения.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Корень проекта (родитель папки src)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"


def load_config() -> dict[str, Any]:
    """Загружает конфигурацию из config/config.json."""
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


class AgentAPIClient:
    """
    Клиент для вызовов API.
    После указания base_url и api_key в config — реализовать запросы (get/post).
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: int = 30,
    ) -> None:
        config = load_config().get("api", {})
        self.base_url = (base_url or config.get("base_url") or "").rstrip("/")
        self.api_key = api_key or config.get("api_key") or ""
        self.timeout = timeout or config.get("timeout_seconds", 30)

    def is_configured(self) -> bool:
        """Проверяет, заданы ли URL и ключ (для тестов и проверок)."""
        return bool(self.base_url and self.api_key)

    # TODO: добавить методы request(), get(), post() после уточнения API
    # def request(self, method: str, path: str, **kwargs) -> Any: ...
    # def get(self, path: str, **kwargs) -> Any: ...
    # def post(self, path: str, data: dict, **kwargs) -> Any: ...

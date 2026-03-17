"""
Заготовка клиента для взаимодействия с API грантового агента.
Параметры подключения задаются в config/config.json или через переменные окружения.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

# Корень проекта (родитель папки src)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"
CONFIG_EXAMPLE_PATH = PROJECT_ROOT / "config" / "config.example.json"

logger = logging.getLogger(__name__)


def load_config() -> dict[str, Any]:
    """Загружает конфигурацию из config/config.json или config/config.example.json."""
    path = CONFIG_PATH if CONFIG_PATH.exists() else CONFIG_EXAMPLE_PATH
    if not path.exists():
        logger.debug("Конфиг не найден: %s", CONFIG_PATH)
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        logger.warning("Ошибка в конфиге (строка %s): %s", e.lineno, e.msg)
        raise ValueError(
            f"Неверный JSON в {path.name} (строка {e.lineno}): {e.msg}. "
            "Проверьте: все строки в кавычках, после значений запятые, нет переводов строк внутри строк."
        ) from e
    logger.debug("Конфиг загружен из %s", path)
    return config


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
        logger.info(
            "Клиент API инициализирован: base_url=%s, timeout=%s, настроен=%s",
            self.base_url or "(не задан)",
            self.timeout,
            bool(self.base_url and self.api_key),
        )

    def is_configured(self) -> bool:
        """Проверяет, заданы ли URL и ключ (для тестов и проверок)."""
        ok = bool(self.base_url and self.api_key)
        logger.debug("is_configured=%s", ok)
        return ok

    # TODO: добавить методы request(), get(), post() после уточнения API
    # def request(self, method: str, path: str, **kwargs) -> Any: ...
    # def get(self, path: str, **kwargs) -> Any: ...
    # def post(self, path: str, data: dict, **kwargs) -> Any: ...

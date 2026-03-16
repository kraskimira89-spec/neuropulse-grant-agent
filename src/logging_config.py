"""
Настройка логирования для проекта.
Читает уровень и путь к файлу из config/config.json (секция logging).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from src.agent_api_client import load_config

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def setup_logging(
    level: str | None = None,
    log_file: str | Path | None = None,
    format_string: str | None = None,
) -> None:
    """
    Настраивает корневой логгер.
    Параметры по умолчанию берутся из config.json ["logging"].
    """
    config = load_config()
    logging_config = config.get("logging", {})
    level = level or logging_config.get("level", "INFO")
    log_file = log_file or logging_config.get("log_file")
    format_string = format_string or logging_config.get(
        "format",
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    )

    log_level = getattr(logging, level.upper(), logging.INFO)
    formatter = logging.Formatter(format_string)

    root = logging.getLogger()
    root.setLevel(log_level)
    # Убираем уже добавленные handlers, чтобы не дублировать
    for h in root.handlers[:]:
        root.removeHandler(h)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)
    root.addHandler(handler)

    if log_file:
        path = PROJECT_ROOT / log_file if isinstance(log_file, str) else Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Возвращает логгер с именем (обычно __name__)."""
    return logging.getLogger(name)

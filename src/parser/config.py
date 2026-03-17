"""
Конфигурация агента Парсер: источники (Telegram, публичные ссылки Яндекс.Диска),
куда загружать (vector_store_id), лимиты.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from src.agent_api_client import PROJECT_ROOT, load_config


def get_parser_config() -> dict[str, Any]:
    """Читает секцию parser из config и env."""
    config = load_config()
    parser_cfg = config.get("parser", {}) or {}
    try:
        from dotenv import load_dotenv
        load_dotenv(PROJECT_ROOT / "config" / ".env")
        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass
    telegram_channels_raw = parser_cfg.get("telegram_channels") or []
    if isinstance(telegram_channels_raw, str):
        telegram_channels_raw = [s.strip() for s in telegram_channels_raw.split(",") if s.strip()]
    # Каждый элемент может быть «url название» — берём только первый токен (URL) для парсера
    telegram_channels = [s.split()[0] for s in telegram_channels_raw if s.strip()]

    disk_public_links_raw = parser_cfg.get("disk_public_links") or []
    if isinstance(disk_public_links_raw, str):
        disk_public_links_raw = [s.strip() for s in disk_public_links_raw.split(",") if s.strip()]
    # Аналогично для ссылок Диска
    disk_public_links = [s.split()[0] for s in disk_public_links_raw if s.strip()]
    vector_store_id = (
        os.getenv("YANDEX_VECTOR_STORE_ID")
        or parser_cfg.get("vector_store_id")
        or config.get("yandex_ai_studio", {}).get("vector_store_id")
        or ""
    ).strip()
    return {
        "telegram_channels": list(telegram_channels),
        "telegram_api_id": os.getenv("TELEGRAM_API_ID") or parser_cfg.get("telegram_api_id") or "",
        "telegram_api_hash": os.getenv("TELEGRAM_API_HASH") or parser_cfg.get("telegram_api_hash") or "",
        "telegram_phone": os.getenv("TELEGRAM_PHONE") or parser_cfg.get("telegram_phone") or "",
        "disk_public_links": list(disk_public_links),
        "vector_store_id": vector_store_id,
        "max_telegram_posts": int(parser_cfg.get("max_telegram_posts") or 100),
        "max_disk_files": int(parser_cfg.get("max_disk_files") or 50),
        "chunk_size": int(parser_cfg.get("chunk_size") or 4000),
        "output_dir": Path(parser_cfg.get("output_dir") or str(PROJECT_ROOT / "data" / "parser_output")),
    }

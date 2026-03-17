"""
Агент Парсер: сбор контента из Telegram и Яндекс.Диска (публичные ссылки),
формирование документов и загрузка в базу знаний (Vector Store) для поиска
по мероприятиям, срокам, форматам, логотипам и т.д.
"""

from __future__ import annotations

from src.parser.config import get_parser_config
from src.parser.pipeline import run_parser_pipeline

__all__ = ["get_parser_config", "run_parser_pipeline"]

"""
Сбор постов из Telegram-каналов (и чатов), к которым есть доступ.
Требуется Telethon: API_ID, API_HASH, номер телефона (или сессия).
Посты извлекаются как текст и возвращаются для дальнейшей индексации.
"""

from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


def _extract_channel_username(link_or_username: str) -> str | None:
    """Извлекает username канала: @channel, t.me/channel, https://t.me/channel."""
    s = (link_or_username or "").strip()
    if s.startswith("@"):
        return s[1:]
    m = re.search(r"t\.me/([a-zA-Z0-9_]+)", s)
    return m.group(1) if m else s or None


def fetch_telegram_channel(
    channel: str,
    api_id: str,
    api_hash: str,
    phone: str,
    max_posts: int = 100,
    session_path: str | None = None,
) -> list[tuple[str, str]]:
    """
    Получает посты из канала Telegram через Telethon.
    Возвращает список пар (источник/дата, текст поста).
    Если Telethon не установлен или нет учётных данных — возвращает [].
    """
    try:
        from telethon import TelegramClient
        from telethon.tl.types import MessageService
    except ImportError:
        logger.debug("Telethon не установлен. pip install telethon")
        return []
    if not api_id or not api_hash:
        logger.debug("Telegram: не заданы API_ID или API_HASH")
        return []
    username = _extract_channel_username(channel)
    if not username:
        return []
    session_path = session_path or "parser_telegram_session"
    results = []
    try:
        client = TelegramClient(session_path, int(api_id), api_hash)
        client.start(phone=phone or None)
        for msg in client.iter_messages(username, limit=max_posts):
            if isinstance(msg, MessageService):
                continue
            text = (msg.text or msg.message or "").strip()
            if not text:
                continue
            date_str = msg.date.strftime("%Y-%m-%d %H:%M") if getattr(msg, "date", None) else ""
            source = f"{username} {date_str}"
            results.append((source, text))
        client.disconnect()
    except Exception as e:
        logger.warning("Ошибка получения постов из Telegram %s: %s", username, e)
    return results


def fetch_telegram_channels(
    channels: list[str],
    api_id: str,
    api_hash: str,
    phone: str,
    max_posts_per_channel: int = 100,
) -> list[tuple[str, str]]:
    """Обходит список каналов и собирает посты. Возвращает объединённый список (источник, текст)."""
    all_posts = []
    for ch in channels:
        all_posts.extend(
            fetch_telegram_channel(ch, api_id, api_hash, phone, max_posts_per_channel)
        )
    return all_posts

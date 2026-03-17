"""
Сбор текста из публичных папок Яндекс.Диска по ссылкам вида https://disk.yandex.ru/d/KEY.
Без OAuth: используется Public API для публичных ресурсов.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

import requests

logger = logging.getLogger(__name__)

PUBLIC_API = "https://cloud-api.yandex.net/v1/disk/public/resources"
DOWNLOAD_API = "https://cloud-api.yandex.net/v1/disk/public/resources/download"


def _extract_public_key(link: str) -> str | None:
    """Извлекает public_key из ссылки https://disk.yandex.ru/d/KEY или https://yadi.sk/d/KEY."""
    link = (link or "").strip()
    m = re.search(r"(?:disk\.yandex\.ru|yadi\.sk)/d/([a-zA-Z0-9_-]+)", link)
    return m.group(1) if m else None


def _list_public_folder(public_key: str) -> list[dict[str, Any]]:
    """Возвращает список элементов в корне публичной папки. Рекурсия по вложенным папкам не делаем в первой версии."""
    items = []
    try:
        r = requests.get(PUBLIC_API, params={"public_key": public_key}, timeout=30)
        r.raise_for_status()
        data = r.json()
        items = data.get("_embedded", {}).get("items") or []
    except Exception as e:
        logger.warning("Ошибка списка публичной папки %s: %s", public_key[:12], e)
    return items


def _download_file_url(public_key: str, path: str) -> str | None:
    """Получает URL для скачивания файла из публичной папки. path — путь вида /имя_файла."""
    try:
        r = requests.get(
            DOWNLOAD_API,
            params={"public_key": public_key, "path": path},
            timeout=15,
        )
        r.raise_for_status()
        return r.json().get("href")
    except Exception as e:
        logger.debug("Ошибка получения ссылки на файл %s: %s", path, e)
        return None


def _is_text_file(name: str) -> bool:
    ext = (Path(name).suffix or "").lower()
    return ext in (".txt", ".md", ".json", ".csv", ".xml", ".html", ".htm", ".rst", ".log")


def _fetch_text_from_url(url: str) -> str:
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding or "utf-8"
        return r.text
    except Exception as e:
        logger.debug("Ошибка загрузки %s: %s", url[:50], e)
        return ""


def fetch_public_disk_folder(
    public_link: str,
    max_files: int = 50,
    text_only: bool = True,
) -> list[tuple[str, str]]:
    """
    Скачивает текстовое содержимое из публичной папки на Яндекс.Диске.
    Возвращает список пар (имя_файла, текст).
    """
    key = _extract_public_key(public_link)
    if not key:
        logger.warning("Не удалось извлечь public_key из ссылки: %s", public_link[:60])
        return []
    items = _list_public_folder(key)
    results = []
    for item in items[:max_files]:
        name = item.get("name") or ""
        item_path = item.get("path", "") or name
        if item.get("type") == "dir":
            continue
        if text_only and not _is_text_file(name):
            continue
        href = _download_file_url(key, item_path)
        if not href:
            continue
        text = _fetch_text_from_url(href)
        if text.strip():
            results.append((name, text))
    return results

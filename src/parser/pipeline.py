"""
Пайплайн агента Парсер: запуск сборщиков (Telegram, Яндекс.Диск),
объединение текста, чанкинг, запись в файлы и загрузка в Vector Store.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from src.parser.config import get_parser_config
from src.parser.disk_fetcher import fetch_public_disk_folder
from src.parser.telegram_fetcher import fetch_telegram_channels

logger = logging.getLogger(__name__)


def _chunk_text(text: str, chunk_size: int) -> list[str]:
    """Разбивает текст на чанки по символам, по границам абзацев где возможно."""
    if not text or chunk_size <= 0:
        return []
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:].strip())
            break
        # Ищем конец абзаца или строки
        chunk = text[start:end]
        last_br = max(chunk.rfind("\n\n"), chunk.rfind("\n"))
        if last_br > chunk_size // 2:
            end = start + last_br + 1
            chunk = text[start:end].strip()
        else:
            chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    return chunks


def _write_chunks_to_files(
    chunks: list[str],
    prefix: str,
    out_dir: Path,
) -> list[Path]:
    """Пишет чанки в файлы prefix_001.txt, prefix_002.txt, ... Возвращает список путей."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, chunk in enumerate(chunks, 1):
        path = out_dir / f"{prefix}_{i:03d}.txt"
        path.write_text(chunk, encoding="utf-8")
        paths.append(path)
    return paths


def run_parser_pipeline(
    run_telegram: bool = True,
    run_disk: bool = True,
    vector_store_id: str | None = None,
) -> dict[str, Any]:
    """
    Запускает парсинг: Telegram + публичные папки Яндекс.Диска,
    формирует файлы и загружает их в Vector Store.
    Возвращает: { "ok": bool, "files_uploaded": int, "errors": list[str],
                  "telegram_posts": int, "disk_files": int, "details": str }
    """
    from src.vector_store_client import upload_file_to_vector_store

    cfg = get_parser_config()
    vs_id = (vector_store_id or cfg.get("vector_store_id") or "").strip()
    out_dir = Path(cfg["output_dir"])
    chunk_size = cfg["chunk_size"]
    errors = []
    all_texts: list[tuple[str, str]] = []  # (источник, текст)

    # Telegram
    telegram_posts = 0
    if run_telegram and cfg.get("telegram_channels"):
        try:
            posts = fetch_telegram_channels(
                cfg["telegram_channels"],
                cfg["telegram_api_id"],
                cfg["telegram_api_hash"],
                cfg["telegram_phone"],
                cfg["max_telegram_posts"],
            )
            telegram_posts = len(posts)
            all_texts.extend(posts)
        except Exception as e:
            errors.append(f"Telegram: {e}")
            logger.exception("Парсер Telegram")

    # Яндекс.Диск (публичные ссылки)
    disk_files = 0
    if run_disk and cfg.get("disk_public_links"):
        for link in cfg["disk_public_links"]:
            try:
                items = fetch_public_disk_folder(
                    link,
                    max_files=cfg["max_disk_files"],
                    text_only=True,
                )
                disk_files += len(items)
                all_texts.extend(items)
            except Exception as e:
                errors.append(f"Яндекс.Диск {link[:30]}…: {e}")
                logger.exception("Парсер Яндекс.Диск")

    # Объединяем текст и чанкуем
    full_text = "\n\n---\n\n".join(f"{src}\n{txt}" for src, txt in all_texts)
    if not full_text.strip():
        return {
            "ok": False,
            "files_uploaded": 0,
            "errors": errors or ["Нет данных для индексации (пустые источники или ошибки сбора)."],
            "telegram_posts": telegram_posts,
            "disk_files": disk_files,
            "details": "Данные не собраны.",
        }

    chunks = _chunk_text(full_text, chunk_size)
    files_uploaded = 0
    if not vs_id:
        errors.append("vector_store_id не задан — загрузка в индекс пропущена.")
    else:
        paths = _write_chunks_to_files(chunks, "parser_chunk", out_dir)
        for path in paths:
            if upload_file_to_vector_store(path, vs_id):
                files_uploaded += 1
            else:
                errors.append(f"Не удалось загрузить {path.name}")

    details = f"Постов Telegram: {telegram_posts}, файлов с Диска: {disk_files}. Загружено в индекс: {files_uploaded} файлов."
    has_data = telegram_posts + disk_files > 0
    return {
        "ok": len(errors) == 0 and (files_uploaded > 0 or not has_data),
        "files_uploaded": files_uploaded,
        "errors": errors,
        "telegram_posts": telegram_posts,
        "disk_files": disk_files,
        "details": details,
    }

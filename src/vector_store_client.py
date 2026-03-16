"""
Клиент для работы с Vector Store API Yandex AI Studio (поисковые индексы).
Список индексов, список файлов в индексе, проверка содержимого.
Требуется: api_key, folder_id; для операций с конкретным индексом — vector_store_id.
Права: ai.assistants.editor (или роли с доступом к Vector Store).
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from src.yandex_ai_client import get_client, get_yandex_ai_config

logger = logging.getLogger(__name__)


def _get_vector_store_client():
    """Возвращает openai-клиент для Yandex (тот же, что для Responses API)."""
    client, _ = get_client()
    return client


def list_vector_stores(limit: int = 20) -> Any:
    """
    Список поисковых индексов (vector stores) в каталоге.
    Возвращает объект с .data (список индексов).
    """
    client = _get_vector_store_client()
    # OpenAI-совместимый API: vector_stores могут быть в client.vector_stores или client.beta.vector_stores
    if hasattr(client, "vector_stores"):
        vs = client.vector_stores
    elif hasattr(client, "beta") and hasattr(client.beta, "vector_stores"):
        vs = client.beta.vector_stores
    else:
        raise AttributeError(
            "У клиента нет vector_stores. Проверьте версию openai и поддержку Vector Store API в Yandex."
        )
    return vs.list(limit=limit)


def list_vector_store_files(
    vector_store_id: str,
    limit: int = 20,
    status: str | None = None,
) -> Any:
    """
    Список файлов в указанном поисковом индексе.
    vector_store_id — идентификатор индекса (из веб-интерфейса или list_vector_stores).
    status — фильтр: None (все), "in_progress", "completed", "failed", "cancelled".
    Возвращает объект с .data (список файлов).
    """
    client = _get_vector_store_client()
    if hasattr(client, "vector_stores"):
        vs = client.vector_stores
    elif hasattr(client, "beta") and hasattr(client.beta, "vector_stores"):
        vs = client.beta.vector_stores
    else:
        raise AttributeError("У клиента нет vector_stores.")
    kwargs = {"vector_store_id": vector_store_id, "limit": limit}
    if status and status in ("in_progress", "completed", "failed", "cancelled"):
        kwargs["filter"] = status
    return vs.files.list(**kwargs)


def get_vector_store(vector_store_id: str) -> Any:
    """Получить информацию об индексе по ID."""
    client = _get_vector_store_client()
    if hasattr(client, "vector_stores"):
        vs = client.vector_stores
    elif hasattr(client, "beta") and hasattr(client.beta, "vector_stores"):
        vs = client.beta.vector_stores
    else:
        raise AttributeError("У клиента нет vector_stores.")
    return vs.retrieve(vector_store_id)


def upload_file_to_vector_store(file_path: Path, vector_store_id: str) -> bool:
    """
    Загружает файл в поисковый индекс (Vector Store) агента.
    Сначала загрузка через files.create, затем привязка к индексу.
    Возвращает True при успехе, False при ошибке (логируется).
    """
    if not vector_store_id or not file_path.exists():
        logger.warning("upload_file_to_vector_store: нет vector_store_id или файл не найден: %s", file_path)
        return False
    try:
        client = _get_vector_store_client()
        with open(file_path, "rb") as f:
            file_obj = client.files.create(file=f, purpose="assistants")
        file_id = getattr(file_obj, "id", None) or str(file_obj)
        if hasattr(client, "vector_stores"):
            vs = client.vector_stores
        elif hasattr(client, "beta") and hasattr(client.beta, "vector_stores"):
            vs = client.beta.vector_stores
        else:
            logger.warning("У клиента нет vector_stores, файл в индекс не добавлен.")
            return False
        vs.files.create(vector_store_id=vector_store_id, file_id=file_id)
        logger.info("Файл загружен в Vector Store: %s -> %s", file_path.name, vector_store_id)
        return True
    except Exception as e:
        logger.exception("Ошибка загрузки файла в Vector Store: %s", e)
        return False


def print_vector_stores(limit: int = 20) -> None:
    """Печатает в stdout список индексов (id, name, status, file_counts)."""
    try:
        r = list_vector_stores(limit=limit)
        items = getattr(r, "data", r) if not isinstance(r, list) else r
        if not items:
            print("Поисковых индексов не найдено.")
            return
        print(f"Найдено индексов: {len(items)}\n")
        for vs in items:
            vid = getattr(vs, "id", vs)
            name = getattr(vs, "name", None) or "(без имени)"
            status = getattr(vs, "status", None)
            counts = getattr(vs, "file_counts", None)
            print(f"  id: {vid}")
            print(f"  name: {name}")
            if status:
                print(f"  status: {status}")
            if counts is not None:
                print(f"  file_counts: {counts}")
            print()
    except Exception as e:
        logger.exception("Ошибка list_vector_stores")
        raise


def print_vector_store_files(vector_store_id: str, limit: int = 50) -> None:
    """Печатает в stdout список файлов в индексе (id, filename, status)."""
    try:
        r = list_vector_store_files(vector_store_id, limit=limit)
        items = getattr(r, "data", r) if not isinstance(r, list) else r
        if not items:
            print("В индексе нет файлов или индекс пуст.")
            return
        print(f"Файлов в индексе: {len(items)}\n")
        for f in items:
            fid = getattr(f, "id", f)
            filename = getattr(f, "filename", None) or getattr(f, "name", "(без имени)")
            status = getattr(f, "status", None)
            print(f"  id: {fid}  filename: {filename}  status: {status}")
    except Exception as e:
        logger.exception("Ошибка list_vector_store_files")
        raise


def main() -> None:
    """CLI: список индексов или список файлов в индексе."""
    import sys
    cfg = get_yandex_ai_config()
    vector_store_id = cfg.get("vector_store_id")

    if len(sys.argv) >= 2 and sys.argv[1] in ("--files", "-f"):
        # list files in store: --files [vector_store_id]
        vid = sys.argv[2] if len(sys.argv) > 2 else vector_store_id
        if not vid:
            print("Укажите vector_store_id: python -m src.vector_store_client --files <vector_store_id>", file=sys.stderr)
            print("Или задайте vector_store_id в config/config.json (yandex_ai_studio.vector_store_id).", file=sys.stderr)
            sys.exit(1)
        print_vector_store_files(vid)
    else:
        # list vector stores
        print_vector_stores()


if __name__ == "__main__":
    main()

"""
Клиент для загрузки файлов на Яндекс.Диск.
Требуется OAuth-токен: получить один раз на https://oauth.yandex.ru/ (тип «Веб-сервисы»),
права cloud_api:disk.read, cloud_api:disk.write. Сохранить в config/.env как YANDEX_DISK_ACCESS_TOKEN.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from src.agent_api_client import load_config, PROJECT_ROOT

logger = logging.getLogger(__name__)


def _load_env() -> None:
    try:
        from dotenv import load_dotenv
        env_path = PROJECT_ROOT / "config" / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass


def get_disk_config() -> dict:
    """Читает настройки Диска: токен и папку для загрузки документов."""
    _load_env()
    config = load_config()
    disk_cfg = config.get("yandex_disk", {}) or {}
    token = (os.getenv("YANDEX_DISK_ACCESS_TOKEN") or disk_cfg.get("access_token") or "").strip()
    folder = (disk_cfg.get("upload_folder") or os.getenv("YANDEX_DISK_UPLOAD_FOLDER") or "").strip()
    return {"token": token, "upload_folder": folder}


def is_configured() -> bool:
    """Проверяет, задан ли OAuth-токен для Диска."""
    return bool(get_disk_config()["token"])


def upload_file(local_path: Path, remote_name: str | None = None) -> bool:
    """
    Загружает файл на Яндекс.Диск в папку из конфига (yandex_disk.upload_folder или YANDEX_DISK_UPLOAD_FOLDER).
    remote_name — имя файла на Диске; по умолчанию совпадает с local_path.name.
    Возвращает True при успехе.
    """
    if not local_path.exists():
        logger.warning("Файл не найден для загрузки на Диск: %s", local_path)
        return False
    cfg = get_disk_config()
    if not cfg["token"]:
        logger.debug("YANDEX_DISK_ACCESS_TOKEN не задан, загрузка на Диск пропущена.")
        return False
    if not cfg["upload_folder"]:
        logger.debug("YANDEX_DISK_UPLOAD_FOLDER или yandex_disk.upload_folder не заданы, загрузка пропущена.")
        return False
    try:
        import yadisk
        client = yadisk.Client(token=cfg["token"])
        if not client.check_token():
            logger.warning("Токен Яндекс.Диска недействителен или истёк.")
            return False
        remote_path = (cfg["upload_folder"].strip("/").replace("\\", "/") + "/" + (remote_name or local_path.name)).replace("//", "/")
        client.upload(str(local_path), remote_path, overwrite=True)
        logger.info("Файл загружен на Яндекс.Диск: %s -> %s", local_path.name, remote_path)
        return True
    except Exception as e:
        logger.exception("Ошибка загрузки на Яндекс.Диск: %s", e)
        return False

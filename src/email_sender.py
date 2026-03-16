"""
Отправка email (уведомления по календарю гранта).
Настройки: config/.env — SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, NOTIFICATION_EMAIL.
"""

from __future__ import annotations

import logging
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from src.agent_api_client import PROJECT_ROOT

logger = logging.getLogger(__name__)


def _load_env() -> None:
    try:
        from dotenv import load_dotenv
        (PROJECT_ROOT / "config" / ".env").exists() and load_dotenv(PROJECT_ROOT / "config" / ".env")
        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass


def get_smtp_config() -> dict:
    """Читает настройки SMTP из переменных окружения."""
    _load_env()
    return {
        "host": os.getenv("SMTP_HOST", "").strip(),
        "port": int(os.getenv("SMTP_PORT", "587") or "587"),
        "user": os.getenv("SMTP_USER", "").strip(),
        "password": os.getenv("SMTP_PASSWORD", "").strip(),
        "default_to": os.getenv("NOTIFICATION_EMAIL", "").strip(),
    }


def is_configured() -> bool:
    """Проверяет, заданы ли SMTP и получатель."""
    cfg = get_smtp_config()
    return bool(cfg["host"] and cfg["user"] and cfg["default_to"])


def send_email(
    to_email: str | None = None,
    subject: str = "",
    body: str = "",
    attachments: list[Path] | None = None,
) -> bool:
    """
    Отправляет письмо через SMTP.
    to_email — если не задан, берётся NOTIFICATION_EMAIL.
    attachments — список путей к файлам (например, .docx).
    """
    cfg = get_smtp_config()
    if not cfg["host"] or not cfg["user"]:
        logger.warning("SMTP не настроен (SMTP_HOST, SMTP_USER). Письмо не отправлено.")
        return False
    to = (to_email or cfg["default_to"]).strip()
    if not to:
        logger.warning("Не указан получатель (to_email или NOTIFICATION_EMAIL).")
        return False

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = cfg["user"]
    msg["To"] = to
    msg.attach(MIMEText(body, "plain", "utf-8"))

    for path in attachments or []:
        if path.exists():
            with open(path, "rb") as f:
                part = MIMEApplication(f.read(), _subtype="vnd.openxmlformats-officedocument.wordprocessingml.document")
            part.add_header("Content-Disposition", "attachment", filename=path.name)
            msg.attach(part)

    try:
        with smtplib.SMTP(cfg["host"], cfg["port"]) as smtp:
            smtp.starttls()
            smtp.login(cfg["user"], cfg["password"])
            smtp.sendmail(cfg["user"], [to], msg.as_string())
        logger.info("Письмо отправлено: %s -> %s", subject[:50], to)
        return True
    except Exception as e:
        logger.exception("Ошибка отправки письма: %s", e)
        return False

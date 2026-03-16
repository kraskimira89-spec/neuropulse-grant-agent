"""
Напоминания по календарю гранта.
Читает data/grant_calendar.json (даты, названия событий), выводит ближайшие сроки.
За 3 дня до события отправляет на почту уведомление с предложением сформировать документ.
Запуск: из корня проекта python scripts/grant_reminders.py (или по расписанию).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

CALENDAR_PATH = PROJECT_ROOT / "data" / "grant_calendar.json"
CALENDAR_EXAMPLE = PROJECT_ROOT / "data" / "grant_calendar.example.json"


def load_calendar() -> list[dict]:
    if CALENDAR_PATH.exists():
        with open(CALENDAR_PATH, encoding="utf-8") as f:
            return json.load(f)
    if CALENDAR_EXAMPLE.exists():
        with open(CALENDAR_EXAMPLE, encoding="utf-8") as f:
            return json.load(f)
    return []


def load_notifications_config() -> dict:
    from src.agent_api_client import load_config
    cfg = load_config()
    return cfg.get("notifications", {}) or {}


def events_in_days(events: list[dict], today, days: int) -> list[dict]:
    """События, до которых ровно days дней."""
    target = today + timedelta(days=days)
    out = []
    for ev in events:
        try:
            d = datetime.fromisoformat(ev["date"].replace("Z", "")).date()
        except (KeyError, ValueError):
            continue
        if d == target:
            out.append({**ev, "_date": d})
    return out


def send_reminder_emails(events_3days: list[dict], chat_url: str) -> None:
    """Отправляет письма с предложением создать документы по событиям."""
    from src.email_sender import send_email, is_configured
    if not is_configured():
        print("Почта не настроена (SMTP_*, NOTIFICATION_EMAIL). Уведомления не отправлены.")
        return
    for ev in events_3days:
        title = ev.get("title", "Событие")
        desc = ev.get("description", "")
        date_str = ev.get("_date", ev.get("date", ""))
        body = (
            f"Напоминание по гранту.\n\n"
            f"Через 3 дня ({date_str}): {title}\n"
        )
        if desc:
            body += f"\n{desc}\n"
        body += (
            "\nМожем сформировать для этого события:\n"
            "— требуемый документ (отчёт);\n"
            "— сценарий проводимого мероприятия;\n"
            "— алгоритм действий или структуру.\n\n"
            "Чтобы создать документы, откройте чат Грантового контролёра НейроПульс и напишите:\n"
            f"Создать документы по событию «{title}»\n\n"
        )
        if chat_url:
            body += f"Ссылка на чат: {chat_url}\n\n"
        body += "После подтверждения документ будет сформирован в Word, отправлен на почту и добавлен в базу знаний агента."
        send_email(subject=f"Грант: через 3 дня — {title}", body=body)
        print(f"Отправлено уведомление: {title}")


def main() -> None:
    events = load_calendar()
    if not events:
        print("Календарь гранта пуст. Скопируйте data/grant_calendar.example.json в data/grant_calendar.json и заполните даты.")
        sys.exit(0)

    today = datetime.utcnow().date()
    notif_cfg = load_notifications_config()
    days_before = int(notif_cfg.get("days_before_event", 3))
    chat_url = (notif_cfg.get("chat_url") or "").strip()

    events_3days = events_in_days(events, today, days_before)
    if events_3days:
        print(f"События через {days_before} дн.: отправка уведомлений на почту...")
        send_reminder_emails(events_3days, chat_url)

    window_days = 30
    upcoming = []
    for ev in events:
        try:
            d = datetime.fromisoformat(ev["date"].replace("Z", "")).date()
        except (KeyError, ValueError):
            continue
        if today <= d <= today + timedelta(days=window_days):
            upcoming.append((d, ev.get("title", ""), ev.get("description", "")))

    upcoming.sort(key=lambda x: x[0])

    if not upcoming:
        print("Ближайшие 30 дней: событий по календарю гранта нет.")
        return

    print("\nБлижайшие сроки по гранту:\n")
    for d, title, desc in upcoming:
        days_left = (d - today).days
        print(f"  {d} ({days_left} дн.) — {title}")
        if desc:
            print(f"    {desc}")
        print()


if __name__ == "__main__":
    main()

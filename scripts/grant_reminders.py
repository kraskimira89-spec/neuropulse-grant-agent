"""
Напоминания по календарю гранта.
Читает data/grant_calendar.json (даты, названия событий) и выводит ближайшие сроки.
Запуск вручную или по расписанию (cron / Task Scheduler).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
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


def main() -> None:
    events = load_calendar()
    if not events:
        print("Календарь гранта пуст. Скопируйте data/grant_calendar.example.json в data/grant_calendar.json и заполните даты.")
        sys.exit(0)

    today = datetime.utcnow().date()
    window_days = 30  # показывать события на 30 дней вперёд
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

    print("Ближайшие сроки по гранту:\n")
    for d, title, desc in upcoming:
        days_left = (d - today).days
        print(f"  {d} ({days_left} дн.) — {title}")
        if desc:
            print(f"    {desc}")
        print()


if __name__ == "__main__":
    main()

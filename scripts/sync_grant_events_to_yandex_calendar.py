"""
Выгрузка событий гранта и ККТ в Яндекс.Календарь.
Читает data/grant_calendar.json и data/grant_kkt.json (события с 2026 года),
создаёт их в календаре по CalDAV.
Запуск: python scripts/sync_grant_events_to_yandex_calendar.py
Календарь берётся из YANDEX_CALENDAR_URL или YANDEX_CALENDAR_NEUROPULSE_URL в config/.env.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.yandex_calendar_client import push_grant_and_kkt_to_yandex_calendar, get_yandex_calendar_config


def main() -> None:
    cfg = get_yandex_calendar_config()
    url = cfg.get("calendar_url") or cfg.get("neuropulse_calendar_url") or ""
    if not url:
        print(
            "Задайте URL календаря в config/.env: YANDEX_CALENDAR_URL или YANDEX_CALENDAR_NEUROPULSE_URL "
            "(скопируйте из Экспорт в calendar.yandex.ru).",
            file=sys.stderr,
        )
        sys.exit(1)
    if not cfg["user"] or not cfg["password"]:
        print("Задайте YANDEX_CALENDAR_USER и YANDEX_CALENDAR_APP_PASSWORD в config/.env.", file=sys.stderr)
        sys.exit(1)
    created, errors = push_grant_and_kkt_to_yandex_calendar(calendar_url=url)
    print(f"Создано событий: {created}, ошибок: {errors}")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()

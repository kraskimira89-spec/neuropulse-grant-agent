"""
Клиент для получения событий из Яндекс Календаря по протоколу CalDAV.
Требуется: пароль приложения (Calendar) из https://id.yandex.ru/security/app-passwords
Сервер: caldav.yandex.ru
"""

from __future__ import annotations

import logging
import os
from datetime import date, datetime
from typing import Any

from src.agent_api_client import load_config

logger = logging.getLogger(__name__)

YANDEX_CALDAV_URL = "https://caldav.yandex.ru"


def get_yandex_calendar_config() -> dict[str, str]:
    """Читает настройки Яндекс Календаря из config и env."""
    config = load_config()
    cal_cfg = config.get("yandex_calendar", {}) or {}
    return {
        "user": os.getenv("YANDEX_CALENDAR_USER") or cal_cfg.get("user") or "",
        "password": os.getenv("YANDEX_CALENDAR_APP_PASSWORD") or cal_cfg.get("app_password") or "",
        "calendar_url": (os.getenv("YANDEX_CALENDAR_URL") or cal_cfg.get("calendar_url") or "").strip(),
        "neuropulse_calendar_url": (
            os.getenv("YANDEX_CALENDAR_NEUROPULSE_URL") or cal_cfg.get("neuropulse_calendar_url") or ""
        ).strip(),
        "neuropulse_embed_url": (
            os.getenv("YANDEX_CALENDAR_NEUROPULSE_EMBED_URL") or cal_cfg.get("neuropulse_embed_url") or ""
        ).strip(),
    }


def is_configured() -> bool:
    """Проверяет, заданы ли логин и пароль приложения для CalDAV."""
    cfg = get_yandex_calendar_config()
    return bool(cfg["user"] and cfg["password"])


def _event_to_dict(ev: Any) -> dict[str, Any] | None:
    """Преобразует событие CalDAV в формат {date, title, description} для дашборда."""
    try:
        comp = getattr(ev, "icalendar_component", None)
        if comp is None:
            return None
        # Ищем VEVENT (comp может быть VCALENDAR с subcomponents)
        vevent = comp
        if hasattr(comp, "subcomponents"):
            for sub in comp.subcomponents:
                if getattr(sub, "name", "") == "VEVENT":
                    vevent = sub
                    break
        dt = None
        summary = ""
        description = ""
        for part in (getattr(vevent, "walk", lambda: [])() or [vevent]):
            name = getattr(part, "name", "")
            if name == "DTSTART":
                v = getattr(part, "decoded", None) or getattr(part, "value", None)
                if isinstance(v, datetime):
                    dt = v.date()
                elif isinstance(v, date):
                    dt = v
                break
        for part in (getattr(vevent, "walk", lambda: [])() or [vevent]):
            name = getattr(part, "name", "")
            if name == "SUMMARY":
                summary = getattr(part, "decoded", None) or getattr(part, "value", "") or ""
                if isinstance(summary, bytes):
                    summary = summary.decode("utf-8", errors="replace")
                summary = str(summary)
                break
        for part in (getattr(vevent, "walk", lambda: [])() or [vevent]):
            name = getattr(part, "name", "")
            if name == "DESCRIPTION":
                description = getattr(part, "decoded", None) or getattr(part, "value", "") or ""
                if isinstance(description, bytes):
                    description = description.decode("utf-8", errors="replace")
                description = str(description)
                break
        address = ""
        for part in (getattr(vevent, "walk", lambda: [])() or [vevent]):
            name = getattr(part, "name", "")
            if name == "LOCATION":
                address = getattr(part, "decoded", None) or getattr(part, "value", "") or ""
                if isinstance(address, bytes):
                    address = address.decode("utf-8", errors="replace")
                address = str(address).strip()
                break
        if dt is None:
            return None
        return {
            "date": dt.isoformat(),
            "title": summary.strip() or "(без названия)",
            "description": description.strip(),
            "address": address,
        }
    except Exception as e:
        logger.debug("Ошибка разбора события CalDAV: %s", e)
        return None


def fetch_events(from_date: date, to_date: date) -> list[dict[str, Any]]:
    """
    Загружает события из Яндекс Календаря за указанный период.
    Возвращает список словарей: [{"date": "YYYY-MM-DD", "title": "...", "description": "..."}, ...].
    При ошибке подключения возвращает пустой список и пишет в лог.
    """
    cfg = get_yandex_calendar_config()
    if not cfg["user"] or not cfg["password"]:
        logger.warning("Яндекс Календарь: не заданы user или app_password")
        return []

    try:
        import caldav
    except ImportError:
        logger.warning("Библиотека caldav не установлена: pip install caldav")
        return []

    start_dt = datetime.combine(from_date, datetime.min.time())
    end_dt = datetime.combine(to_date, datetime.max.time())

    try:
        client = caldav.DAVClient(
            url=YANDEX_CALDAV_URL,
            username=cfg["user"],
            password=cfg["password"],
        )
        principal = client.principal()
        events_flat = []

        if cfg["calendar_url"]:
            try:
                calendar = caldav.Calendar(client=client, url=cfg["calendar_url"])
                raw_events = calendar.date_search(start=start_dt, end=end_dt)
                events_flat.extend(raw_events)
            except Exception as e:
                logger.warning("Ошибка доступа к календарю по URL %s: %s", cfg["calendar_url"][:50], e)
        else:
            calendars = principal.calendars()
            for cal in calendars:
                try:
                    raw_events = cal.date_search(start=start_dt, end=end_dt)
                    events_flat.extend(raw_events)
                except Exception as e:
                    logger.debug("Ошибка календаря %s: %s", getattr(cal, "url", ""), e)

        out = []
        for ev in events_flat:
            d = _event_to_dict(ev)
            if d:
                out.append(d)
        out.sort(key=lambda x: (x["date"], x["title"]))
        return out
    except Exception as e:
        logger.exception("Ошибка CalDAV Яндекс Календарь: %s", e)
        return []


def fetch_neuropulse_events(from_date: date, to_date: date) -> list[dict[str, Any]]:
    """
    Загружает события только из календаря «Нейропульс» за указанный период.
    Требуется neuropulse_calendar_url в конфиге (YANDEX_CALENDAR_NEUROPULSE_URL или yandex_calendar.neuropulse_calendar_url).
    """
    cfg = get_yandex_calendar_config()
    url = cfg.get("neuropulse_calendar_url") or ""
    if not url or not cfg["user"] or not cfg["password"]:
        return []
    try:
        import caldav
    except ImportError:
        return []
    start_dt = datetime.combine(from_date, datetime.min.time())
    end_dt = datetime.combine(to_date, datetime.max.time())
    try:
        client = caldav.DAVClient(
            url=YANDEX_CALDAV_URL,
            username=cfg["user"],
            password=cfg["password"],
        )
        calendar = caldav.Calendar(client=client, url=url)
        raw_events = calendar.date_search(start=start_dt, end=end_dt)
        out = []
        for ev in raw_events:
            d = _event_to_dict(ev)
            if d:
                out.append(d)
        out.sort(key=lambda x: (x["date"], x["title"]))
        return out
    except Exception as e:
        logger.warning("Ошибка календарь Нейропульс %s: %s", url[:50], e)
        return []

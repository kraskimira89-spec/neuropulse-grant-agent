"""
Клиент для получения событий из Яндекс Календаря по протоколу CalDAV.
Требуется: пароль приложения (Calendar) из https://id.yandex.ru/security/app-passwords
Сервер: caldav.yandex.ru
"""

from __future__ import annotations

import logging
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any

from src.agent_api_client import load_config, PROJECT_ROOT

logger = logging.getLogger(__name__)

YANDEX_CALDAV_URL = "https://caldav.yandex.ru"


def _load_dotenv() -> None:
    """Подгружает config/.env и .env, чтобы YANDEX_CALENDAR_* были доступны."""
    try:
        from dotenv import load_dotenv
        env_path = PROJECT_ROOT / "config" / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass


def get_yandex_calendar_config() -> dict[str, str]:
    """Читает настройки Яндекс Календаря из config и env."""
    _load_dotenv()
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


def _make_ical_event(start_date: date, title: str, description: str = "", location: str = "", uid: str | None = None) -> str:
    """Формирует iCalendar-строку (VCALENDAR с одним VEVENT) для полнодневного события."""
    import uuid
    uid = uid or str(uuid.uuid4())
    dt_start = start_date.strftime("%Y%m%d")
    # полнодневное событие: DTEND — следующий день (по спецификации exclusive)
    from datetime import timedelta
    end_date = start_date + timedelta(days=1)
    dt_end = end_date.strftime("%Y%m%d")
    summary = (title or "").replace("\r", "").replace("\n", " ").strip() or "Событие"
    desc = (description or "").replace("\r", " ").strip()
    loc = (location or "").replace("\r", " ").strip()
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//neuropulse-grant-agent//EN",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTART;VALUE=DATE:{dt_start}",
        f"DTEND;VALUE=DATE:{dt_end}",
        f"SUMMARY:{summary}",
        "END:VEVENT",
        "END:VCALENDAR",
    ]
    if desc:
        # DESCRIPTION может содержать запятые — экранируем
        escaped_desc = desc.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")
        lines.insert(-2, f"DESCRIPTION:{escaped_desc}")
    if loc:
        lines.insert(-2, f"LOCATION:{loc}")
    return "\r\n".join(lines)


def create_event(
    calendar_url: str,
    start_date: date,
    title: str,
    description: str = "",
    location: str = "",
) -> bool:
    """
    Создаёт полнодневное событие в календаре Яндекса по CalDAV.
    calendar_url — URL календаря (из экспорта в calendar.yandex.ru).
    Возвращает True при успехе.
    """
    cfg = get_yandex_calendar_config()
    if not cfg["user"] or not cfg["password"]:
        logger.warning("Яндекс Календарь: не заданы user или app_password")
        return False
    if not calendar_url:
        logger.warning("create_event: не указан calendar_url")
        return False
    try:
        import caldav
    except ImportError:
        logger.warning("Библиотека caldav не установлена: pip install caldav")
        return False
    ical = _make_ical_event(start_date, title, description, location)
    try:
        client = caldav.DAVClient(
            url=YANDEX_CALDAV_URL,
            username=cfg["user"],
            password=cfg["password"],
        )
        calendar = caldav.Calendar(client=client, url=calendar_url)
        try:
            calendar.save_event(ical)
        except AttributeError:
            calendar.add_event(ical)
        logger.info("Событие создано в календаре: %s на %s", title[:50], start_date)
        return True
    except Exception as e:
        logger.exception("Ошибка создания события в календаре: %s", e)
        return False


def push_grant_and_kkt_to_yandex_calendar(calendar_url: str | None = None) -> tuple[int, int]:
    """
    Загружает события из data/grant_calendar.json и data/grant_kkt.json (с 2026 года)
    и создаёт их в Яндекс.Календаре. Возвращает (создано, ошибок).
    calendar_url — URL календаря; если не задан, берётся из конфига (YANDEX_CALENDAR_URL или YANDEX_CALENDAR_NEUROPULSE_URL).
    """
    import json
    cfg = get_yandex_calendar_config()
    url = (calendar_url or "").strip() or cfg.get("calendar_url") or cfg.get("neuropulse_calendar_url") or ""
    if not url:
        logger.warning("push_grant_and_kkt_to_yandex_calendar: не задан calendar_url")
        return 0, 0
    if not cfg["user"] or not cfg["password"]:
        logger.warning("Яндекс Календарь: не заданы user или app_password")
        return 0, 0
    cutoff = date(2026, 1, 1)
    events_to_create: list[tuple[date, str, str, str]] = []
    # grant_calendar.json
    for path in (PROJECT_ROOT / "data" / "grant_calendar.json", PROJECT_ROOT / "data" / "grant_calendar.example.json"):
        if not path.exists():
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for ev in (data if isinstance(data, list) else []):
                d_str = ev.get("date", "")[:10]
                if not d_str:
                    continue
                d = datetime.strptime(d_str, "%Y-%m-%d").date()
                if d < cutoff:
                    continue
                title = (ev.get("title") or "Событие").strip()
                desc = (ev.get("description") or "").strip()
                addr = (ev.get("address") or "").strip()
                events_to_create.append((d, title, desc, addr))
        except Exception as e:
            logger.warning("Ошибка чтения %s: %s", path.name, e)
        break
    # grant_kkt.json
    for path in (PROJECT_ROOT / "data" / "grant_kkt.json", PROJECT_ROOT / "data" / "grant_kkt.example.json"):
        if not path.exists():
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            points = data.get("points", data) if isinstance(data, dict) else (data if isinstance(data, list) else [])
            for p in points:
                d_str = (p.get("date_end") or "")[:10]
                if not d_str:
                    continue
                d = datetime.strptime(d_str, "%Y-%m-%d").date()
                if d < cutoff:
                    continue
                desc = (p.get("description") or "").strip()
                expected = (p.get("expected_result") or "").strip()
                title = f"ККТ: {desc}" if desc else "ККТ"
                body = f"Ожидаемый результат: {expected}" if expected else ""
                events_to_create.append((d, title, body, ""))
        except Exception as e:
            logger.warning("Ошибка чтения %s: %s", path.name, e)
        break
    created, errors = 0, 0
    for d, title, desc, loc in events_to_create:
        if create_event(url, d, title, desc, loc):
            created += 1
        else:
            errors += 1
    return created, errors

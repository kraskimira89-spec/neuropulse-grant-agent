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
        uid_val = ""
        for part in (getattr(vevent, "walk", lambda: [])() or [vevent]):
            name = getattr(part, "name", "")
            if name == "UID":
                uid_val = getattr(part, "decoded", None) or getattr(part, "value", "") or ""
                if isinstance(uid_val, bytes):
                    uid_val = uid_val.decode("utf-8", errors="replace")
                uid_val = str(uid_val).strip()
                break
        rrule_val = ""
        for part in (getattr(vevent, "walk", lambda: [])() or [vevent]):
            name = getattr(part, "name", "")
            if name == "RRULE":
                rrule_val = getattr(part, "decoded", None) or getattr(part, "value", "") or ""
                if isinstance(rrule_val, bytes):
                    rrule_val = rrule_val.decode("utf-8", errors="replace")
                rrule_val = str(rrule_val).strip()
                break
        end_dt = None
        for part in (getattr(vevent, "walk", lambda: [])() or [vevent]):
            name = getattr(part, "name", "")
            if name == "DTEND":
                v = getattr(part, "decoded", None) or getattr(part, "value", None)
                if isinstance(v, datetime):
                    end_dt = v.date()
                elif isinstance(v, date):
                    end_dt = v
                break
        if dt is None:
            return None
        out = {
            "date": dt.isoformat(),
            "title": summary.strip() or "(без названия)",
            "description": description.strip(),
            "address": address,
        }
        if uid_val:
            out["uid"] = uid_val
        if rrule_val:
            out["rrule"] = rrule_val
        if end_dt is not None:
            out["end"] = end_dt.isoformat()
        return out
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
    items = fetch_calendar_events_with_urls(
        url=None, from_date=from_date, to_date=to_date, use_neuropulse_url=True
    )
    return [
        {"date": x["date"], "title": x["title"], "description": x.get("description", ""), "address": x.get("address", "")}
        for x in items
    ]


def fetch_calendar_events_with_urls(
    url: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    use_neuropulse_url: bool = False,
) -> list[dict[str, Any]]:
    """
    Загружает события из календаря CalDAV с полями date, title, description, address, url (для удаления).
    url — URL календаря; если use_neuropulse_url=True, берётся neuropulse_calendar_url из конфига.
    """
    cfg = get_yandex_calendar_config()
    cal_url = (url or "").strip() or (
        cfg.get("neuropulse_calendar_url") if use_neuropulse_url else cfg.get("calendar_url")
    ) or ""
    if not cal_url or not cfg["user"] or not cfg["password"]:
        return []
    try:
        import caldav
    except ImportError:
        return []
    today_val = date.today()
    start = from_date or today_val
    end = to_date or today_val
    start_dt = datetime.combine(start, datetime.min.time())
    end_dt = datetime.combine(end, datetime.max.time())
    try:
        client = caldav.DAVClient(
            url=YANDEX_CALDAV_URL,
            username=cfg["user"],
            password=cfg["password"],
        )
        calendar = caldav.Calendar(client=client, url=cal_url)
        raw_events = calendar.date_search(start=start_dt, end=end_dt)
        out = []
        for ev in raw_events:
            d = _event_to_dict(ev)
            if d:
                d["url"] = getattr(ev, "url", "") or ""
                out.append(d)
        out.sort(key=lambda x: (x["date"], x["title"]))
        return out
    except Exception as e:
        logger.warning("Ошибка загрузки событий CalDAV %s: %s", cal_url[:50], e)
        return []


def _normalize_key(d: date, title: str) -> tuple[str, str]:
    """Ключ для сравнения: дата и нормализованное название (без лишних пробелов, нижний регистр)."""
    return (d.isoformat(), (title or "").strip().lower().replace("\n", " ").replace("  ", " ") or " ")


def fetch_existing_event_keys(
    calendar_url: str,
    from_date: date,
    to_date: date,
) -> set[tuple[str, str]]:
    """
    Загружает события из календаря за период и возвращает множество ключей (date_iso, title_normalized)
    для проверки дубликатов перед созданием.
    """
    items = fetch_calendar_events_with_urls(url=calendar_url, from_date=from_date, to_date=to_date)
    out = set()
    for x in items:
        d_str = (x.get("date") or "")[:10]
        title = (x.get("title") or "").strip()
        if d_str and title:
            try:
                d = datetime.strptime(d_str, "%Y-%m-%d").date()
                out.add(_normalize_key(d, title))
            except ValueError:
                pass
    return out


def delete_event(calendar_url: str, event_url: str) -> bool:
    """
    Удаляет событие из календаря по его CalDAV URL.
    Возвращает True при успехе.
    """
    cfg = get_yandex_calendar_config()
    if not cfg["user"] or not cfg["password"] or not calendar_url or not event_url:
        return False
    try:
        import caldav
    except ImportError:
        return False
    try:
        client = caldav.DAVClient(
            url=YANDEX_CALDAV_URL,
            username=cfg["user"],
            password=cfg["password"],
        )
        calendar = caldav.Calendar(client=client, url=calendar_url)
        event = calendar.event_by_url(event_url)
        event.delete()
        logger.info("Событие удалено из календаря: %s", event_url[:60])
        return True
    except Exception as e:
        logger.exception("Ошибка удаления события: %s", e)
        return False


def _make_ical_event(
    start_date: date,
    title: str,
    description: str = "",
    location: str = "",
    uid: str | None = None,
    rrule: str | None = None,
    end_date: date | None = None,
) -> str:
    """Формирует iCalendar-строку (VCALENDAR с одним VEVENT) для полнодневного события. rrule — повторение (например FREQ=WEEKLY;BYDAY=MO). end_date — дата окончания; если не задана, start_date + 1 день."""
    import uuid
    from datetime import timedelta
    uid = uid or str(uuid.uuid4())
    dt_start = start_date.strftime("%Y%m%d")
    effective_end = end_date if end_date is not None else start_date + timedelta(days=1)
    dt_end = effective_end.strftime("%Y%m%d")
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
    if rrule:
        lines.insert(-2, f"RRULE:{rrule}")
    if desc:
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
    uid: str | None = None,
    rrule: str | None = None,
    end_date: date | None = None,
) -> tuple[bool, str | None]:
    """
    Создаёт полнодневное событие в календаре Яндекса по CalDAV.
    calendar_url — URL календаря (из экспорта в calendar.yandex.ru).
    uid, rrule, end_date — опционально. Возвращает (успех, uid использованный или None).
    """
    cfg = get_yandex_calendar_config()
    if not cfg["user"] or not cfg["password"]:
        logger.warning("Яндекс Календарь: не заданы user или app_password")
        return False, None
    if not calendar_url:
        logger.warning("create_event: не указан calendar_url")
        return False, None
    try:
        import caldav
    except ImportError:
        logger.warning("Библиотека caldav не установлена: pip install caldav")
        return False, None
    import uuid
    used_uid = (uid or "").strip() or str(uuid.uuid4())
    ical = _make_ical_event(start_date, title, description, location, uid=used_uid, rrule=rrule, end_date=end_date)
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
        return True, used_uid
    except Exception as e:
        logger.exception("Ошибка создания события в календаре: %s", e)
        return False, None


def add_event_to_neuropulse_calendar(
    title: str,
    start_date: date,
    description: str = "",
    address: str = "",
    save_to_json: bool = True,
    rrule: str | None = None,
    end_date: date | None = None,
) -> tuple[bool, str]:
    """
    Создаёт полнодневное событие в календаре Нейропульс (URL из конфига) и при save_to_json=True
    дописывает его в data/grant_calendar.json. Возвращает (успех, сообщение для пользователя).
    """
    cfg = get_yandex_calendar_config()
    url = (cfg.get("neuropulse_calendar_url") or cfg.get("calendar_url") or "").strip()
    if not url:
        return False, "Не задан URL календаря (YANDEX_CALENDAR_NEUROPULSE_URL или YANDEX_CALENDAR_URL)."
    if not cfg["user"] or not cfg["password"]:
        return False, "Не заданы учётные данные календаря (YANDEX_CALENDAR_USER, YANDEX_CALENDAR_APP_PASSWORD)."
    ok, uid = create_event(
        url, start_date, title or "Событие", description, address,
        rrule=rrule, end_date=end_date,
    )
    if not ok:
        return False, "Не удалось создать событие в календаре (проверьте логи)."
    if save_to_json:
        import json
        path = PROJECT_ROOT / "data" / "grant_calendar.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            data = []
            if path.exists():
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
            if not isinstance(data, list):
                data = []
            item = {
                "date": start_date.isoformat(),
                "title": (title or "Событие").strip(),
                "description": (description or "").strip(),
                "address": (address or "").strip(),
            }
            if uid:
                item["uid"] = uid
            if rrule:
                item["rrule"] = rrule
            if end_date is not None:
                item["end"] = end_date.isoformat()
            data.append(item)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning("Не удалось дописать событие в grant_calendar.json: %s", e)
    return True, f"Событие «{title or 'Событие'}» на {start_date} создано в календаре Нейропульс."


def execute_add_calendar_event_tool(args: dict) -> str:
    """
    Выполняет добавление события по аргументам инструмента add_calendar_event.
    args: summary, dtstart, description?, dtend?, rrule?. Возвращает сообщение для пользователя.
    """
    summary = (args.get("summary") or "").strip() or "Событие"
    dtstart_s = (args.get("dtstart") or "")[:10]
    if not dtstart_s:
        return "Ошибка: не указана дата (dtstart)."
    try:
        start_date = datetime.strptime(dtstart_s, "%Y-%m-%d").date()
    except ValueError:
        return f"Ошибка: неверный формат даты {dtstart_s}, нужен YYYY-MM-DD."
    description = (args.get("description") or "").strip()
    end_date = None
    if args.get("dtend"):
        try:
            end_date = datetime.strptime((args.get("dtend") or "")[:10], "%Y-%m-%d").date()
        except ValueError:
            pass
    rrule = (args.get("rrule") or "").strip() or None
    ok, msg = add_event_to_neuropulse_calendar(
        title=summary, start_date=start_date, description=description, address="",
        save_to_json=True, rrule=rrule, end_date=end_date,
    )
    return msg if ok else f"Ошибка: {msg}"


def push_grant_and_kkt_to_yandex_calendar(
    calendar_url: str | None = None,
    skip_existing: bool = True,
) -> tuple[int, int]:
    """
    Загружает события из data/grant_calendar.json и data/grant_kkt.json (с 2026 года)
    и создаёт их в Яндекс.Календаре. Возвращает (создано, ошибок).
    calendar_url — URL календаря; если не задан, берётся из конфига.
    skip_existing — не создавать событие, если в календаре уже есть с той же датой и названием (без дубликатов).
    """
    import json
    from datetime import timedelta
    cfg = get_yandex_calendar_config()
    url = (calendar_url or "").strip() or cfg.get("calendar_url") or cfg.get("neuropulse_calendar_url") or ""
    # #region agent log
    try:
        _src = "param" if (calendar_url or "").strip() else ("cfg_calendar" if cfg.get("calendar_url") else "cfg_neuropulse")
        import json
        with open("debug-7f0fda.log", "a", encoding="utf-8") as _f:
            _f.write(json.dumps({"sessionId": "7f0fda", "hypothesisId": "C", "location": "push_grant_and_kkt_to_yandex_calendar", "message": "push URL source", "data": {"url_source": _src, "has_url": bool(url)}, "timestamp": __import__("time").time() * 1000}, ensure_ascii=False) + "\n")
    except Exception:
        pass
    # #endregion
    if not url:
        logger.warning("push_grant_and_kkt_to_yandex_calendar: не задан calendar_url")
        return 0, 0
    if not cfg["user"] or not cfg["password"]:
        logger.warning("Яндекс Календарь: не заданы user или app_password")
        return 0, 0
    cutoff = date(2026, 1, 1)
    # (start_date, title, description, location, uid|None, rrule|None, end_date|None)
    events_to_create: list[tuple[date, str, str, str, str | None, str | None, date | None]] = []
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
                uid = (ev.get("uid") or "").strip() or None
                rrule = (ev.get("rrule") or "").strip() or None
                end_str = (ev.get("end") or "")[:10]
                end_d = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else None
                events_to_create.append((d, title, desc, addr, uid, rrule, end_d))
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
                events_to_create.append((d, title, body, "", None, None, None))
        except Exception as e:
            logger.warning("Ошибка чтения %s: %s", path.name, e)
        break
    existing_keys: set[tuple[str, str]] = set()
    if skip_existing and events_to_create:
        min_d = min(e[0] for e in events_to_create)
        max_d = max(e[0] for e in events_to_create)
        end_range = max_d + timedelta(days=365)
        existing_keys = fetch_existing_event_keys(url, min_d, end_range)
    created, errors = 0, 0
    for d, title, desc, loc, uid, rrule, end_d in events_to_create:
        if skip_existing and _normalize_key(d, title) in existing_keys:
            continue
        ok, _ = create_event(url, d, title, desc, loc, uid=uid, rrule=rrule, end_date=end_d)
        if ok:
            created += 1
            existing_keys.add(_normalize_key(d, title))
        else:
            errors += 1
    return created, errors


def _load_local_events_for_sync() -> list[dict[str, Any]]:
    """
    Собирает объединённый список локальных событий из grant_calendar.json и grant_kkt.json (с 2026 года).
    Каждый элемент: date (str), title, description, address, uid?, rrule?, end? (все опциональные — только при наличии).
    """
    import json
    cutoff = date(2026, 1, 1)
    out: list[dict[str, Any]] = []
    for path in (PROJECT_ROOT / "data" / "grant_calendar.json", PROJECT_ROOT / "data" / "grant_calendar.example.json"):
        if not path.exists():
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            for ev in (data if isinstance(data, list) else []):
                d_str = (ev.get("date") or "")[:10]
                if not d_str:
                    continue
                try:
                    d = datetime.strptime(d_str, "%Y-%m-%d").date()
                except ValueError:
                    continue
                if d < cutoff:
                    continue
                item = {
                    "date": d_str,
                    "title": (ev.get("title") or "Событие").strip(),
                    "description": (ev.get("description") or "").strip(),
                    "address": (ev.get("address") or "").strip(),
                }
                if ev.get("uid"):
                    item["uid"] = (ev.get("uid") or "").strip()
                if ev.get("rrule"):
                    item["rrule"] = (ev.get("rrule") or "").strip()
                end_str = (ev.get("end") or "")[:10]
                if end_str:
                    item["end"] = end_str
                out.append(item)
        except Exception as e:
            logger.warning("Ошибка чтения %s: %s", path.name, e)
        break
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
                try:
                    d = datetime.strptime(d_str, "%Y-%m-%d").date()
                except ValueError:
                    continue
                if d < cutoff:
                    continue
                desc = (p.get("description") or "").strip()
                expected = (p.get("expected_result") or "").strip()
                title = f"ККТ: {desc}" if desc else "ККТ"
                body = f"Ожидаемый результат: {expected}" if expected else ""
                out.append({
                    "date": d_str,
                    "title": title,
                    "description": body,
                    "address": "",
                })
        except Exception as e:
            logger.warning("Ошибка чтения %s: %s", path.name, e)
        break
    return out


def sync_grant_and_kkt_with_calendar(
    calendar_url: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
) -> tuple[int, int, int]:
    """
    Двусторонняя синхронизация: локальные события (grant_calendar + ККТ) — источник истины.
    Создаёт недостающие в календаре, обновляет изменённые (удаление + создание с тем же uid), удаляет из календаря события, которых нет в локальном списке.
    Возвращает (создано, обновлено, удалено).
    """
    from datetime import timedelta
    cfg = get_yandex_calendar_config()
    url = (calendar_url or "").strip() or cfg.get("calendar_url") or cfg.get("neuropulse_calendar_url") or ""
    # #region agent log
    try:
        _src = "param" if (calendar_url or "").strip() else ("cfg_calendar" if cfg.get("calendar_url") else "cfg_neuropulse")
        import json
        with open("debug-7f0fda.log", "a", encoding="utf-8") as _f:
            _f.write(json.dumps({"sessionId": "7f0fda", "hypothesisId": "C", "location": "sync_grant_and_kkt_with_calendar", "message": "sync URL source", "data": {"url_source": _src, "has_url": bool(url)}, "timestamp": __import__("time").time() * 1000}, ensure_ascii=False) + "\n")
    except Exception:
        pass
    # #endregion
    if not url or not cfg["user"] or not cfg["password"]:
        logger.warning("sync_grant_and_kkt_with_calendar: не задан calendar_url или учётные данные")
        return 0, 0, 0
    local_list = _load_local_events_for_sync()
    if not local_list:
        logger.info("sync_grant_and_kkt_with_calendar: нет локальных событий")
        return 0, 0, 0
    min_d = min(datetime.strptime(ev["date"][:10], "%Y-%m-%d").date() for ev in local_list)
    max_d = max(datetime.strptime(ev["date"][:10], "%Y-%m-%d").date() for ev in local_list)
    range_start = from_date or min_d
    range_end = to_date or (max_d + timedelta(days=365))
    cal_events = fetch_calendar_events_with_urls(url=url, from_date=range_start, to_date=range_end)
    local_by_key: dict[tuple[str, str], dict] = {}
    local_by_uid: dict[str, dict] = {}
    for ev in local_list:
        d = datetime.strptime(ev["date"][:10], "%Y-%m-%d").date()
        key = _normalize_key(d, ev["title"])
        local_by_key[key] = ev
        if ev.get("uid"):
            local_by_uid[ev["uid"]] = ev
    cal_by_key: dict[tuple[str, str], dict] = {}
    cal_by_uid: dict[str, dict] = {}
    for c in cal_events:
        d_str = (c.get("date") or "")[:10]
        if not d_str:
            continue
        try:
            d = datetime.strptime(d_str, "%Y-%m-%d").date()
        except ValueError:
            continue
        key = _normalize_key(d, c.get("title") or "")
        cal_by_key[key] = c
        if c.get("uid"):
            cal_by_uid[c["uid"]] = c
    created, updated, deleted = 0, 0, 0
    matched_cal_urls: set[str] = set()
    for ev in local_list:
        d = datetime.strptime(ev["date"][:10], "%Y-%m-%d").date()
        key = _normalize_key(d, ev["title"])
        cal_ev = None
        if ev.get("uid") and ev["uid"] in cal_by_uid:
            cal_ev = cal_by_uid[ev["uid"]]
        elif key in cal_by_key:
            cal_ev = cal_by_key[key]
        if cal_ev:
            matched_cal_urls.add(cal_ev["url"])
            # Сравнение: description, address, end, rrule (достаточно для решения об обновлении)
            cal_desc = (cal_ev.get("description") or "").strip()
            cal_addr = (cal_ev.get("address") or "").strip()
            cal_rrule = (cal_ev.get("rrule") or "").strip()
            loc_desc = (ev.get("description") or "").strip()
            loc_addr = (ev.get("address") or "").strip()
            loc_rrule = (ev.get("rrule") or "").strip()
            loc_end = (ev.get("end") or "")[:10]
            same = (
                cal_desc == loc_desc and cal_addr == loc_addr and cal_rrule == loc_rrule
                and (not loc_end or _event_end_from_cal(cal_ev) == loc_end)
            )
            if same:
                continue
            delete_event(url, cal_ev["url"])
            use_uid = cal_ev.get("uid") or ev.get("uid")
            end_d = None
            if ev.get("end"):
                try:
                    end_d = datetime.strptime(ev["end"][:10], "%Y-%m-%d").date()
                except ValueError:
                    pass
            ok, _ = create_event(
                url, d, ev["title"], ev.get("description") or "", ev.get("address") or "",
                uid=use_uid, rrule=ev.get("rrule") or None, end_date=end_d,
            )
            if ok:
                updated += 1
            continue
        end_d = None
        if ev.get("end"):
            try:
                end_d = datetime.strptime(ev["end"][:10], "%Y-%m-%d").date()
            except ValueError:
                pass
        ok, _ = create_event(
            url, d, ev["title"], ev.get("description") or "", ev.get("address") or "",
            uid=ev.get("uid") or None, rrule=ev.get("rrule") or None, end_date=end_d,
        )
        if ok:
            created += 1
    for c in cal_events:
        if c.get("url") and c["url"] in matched_cal_urls:
            continue
        d_str = (c.get("date") or "")[:10]
        if not d_str:
            continue
        try:
            d = datetime.strptime(d_str, "%Y-%m-%d").date()
        except ValueError:
            continue
        key = _normalize_key(d, c.get("title") or "")
        uid = c.get("uid") or ""
        if key in local_by_key or uid in local_by_uid:
            continue
        if delete_event(url, c["url"]):
            deleted += 1
    return created, updated, deleted


def _event_end_from_cal(cal_ev: dict) -> str:
    """Возвращает дату окончания события из календарного события (DTEND) в формате YYYY-MM-DD или пустую строку."""
    end_str = (cal_ev.get("end") or "")[:10]
    if end_str:
        return end_str
    d_str = (cal_ev.get("date") or "")[:10]
    if d_str:
        try:
            from datetime import timedelta
            d = datetime.strptime(d_str, "%Y-%m-%d").date()
            return (d + timedelta(days=1)).isoformat()
        except ValueError:
            pass
    return ""

"""
Дашборд проекта neuropulse-grant-agent.
Блоки: диалог с агентом, ближайшие сроки, аудит чата, статус агента, быстрые действия, Vector Store, ссылки.
При нажатии на быстрые действия формулировка уходит в диалог с агентом.
"""

from __future__ import annotations

import hashlib
from typing import Any
import sys
from pathlib import Path
from datetime import datetime, timedelta

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import json
import logging
import os

import streamlit as st

from src.agent_api_client import load_config, PROJECT_ROOT

# Чтобы дашборд видел YANDEX_VECTOR_STORE_ID из config/.env
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / "config" / ".env")
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass
from src.git_auto_push import git_push_if_changes, _register_atexit

logger = logging.getLogger(__name__)

AUDIT_LOG = PROJECT_ROOT / "data" / "chat_audit.jsonl"
CALENDAR_PATH = PROJECT_ROOT / "data" / "grant_calendar.json"
CALENDAR_EXAMPLE = PROJECT_ROOT / "data" / "grant_calendar.example.json"
CONTACTS_PATH = PROJECT_ROOT / "data" / "grant_contacts.json"
CONTACTS_EXAMPLE = PROJECT_ROOT / "data" / "grant_contacts.example.json"
GRANT_DASHBOARD_PATH = PROJECT_ROOT / "data" / "grant_project_dashboard.json"
GRANT_DASHBOARD_EXAMPLE = PROJECT_ROOT / "data" / "grant_project_dashboard.example.json"
KKT_PATH = PROJECT_ROOT / "data" / "grant_kkt.json"
KKT_EXAMPLE = PROJECT_ROOT / "data" / "grant_kkt.example.json"
RISKS_PATH = PROJECT_ROOT / "data" / "grant_risks.json"
RISKS_EXAMPLE = PROJECT_ROOT / "data" / "grant_risks.example.json"
COMMUNICATIONS_PATH = PROJECT_ROOT / "data" / "grant_communications.json"
COMMUNICATIONS_EXAMPLE = PROJECT_ROOT / "data" / "grant_communications.example.json"
DOCUMENTS_ARCHIVE_PATH = PROJECT_ROOT / "data" / "grant_documents_archive.json"
DOCUMENTS_ARCHIVE_EXAMPLE = PROJECT_ROOT / "data" / "grant_documents_archive.example.json"
NOTIFICATION_SETTINGS_PATH = PROJECT_ROOT / "data" / "notification_settings.json"
NOTIFICATION_SETTINGS_EXAMPLE = PROJECT_ROOT / "data" / "notification_settings.example.json"
DASHBOARD_LAYOUT_PATH = PROJECT_ROOT / "data" / "dashboard_layout.json"

# Папка «Паспорт»: паспорт проекта и краткая история диалогов (автосохранение раз в 15 мин)
PASSPORT_DIR = PROJECT_ROOT / "Паспорт"
PASSPORT_PROJECT_FILE = PASSPORT_DIR / "паспорт_проекта.md"
PASSPORT_HISTORY_FILE = PASSPORT_DIR / "история_диалогов.md"
PASSPORT_LAST_SAVE_FILE = PASSPORT_DIR / ".last_passport_save"
PASSPORT_INTERVAL_MINUTES = 15

STATUS_LABELS = {"not_started": "⚪ Не начато", "in_progress": "🟡 В работе", "done": "🟢 Выполнено", "overdue": "🔴 Просрочено"}
STATUS_COLORS = {"not_started": "#888", "in_progress": "#d4a017", "done": "#28a745", "overdue": "#dc3545"}


def _block_header(title: str, block_id: str) -> bool:
    """Заголовок блока: название и шестерёнка. Если контекст раскладки задан, показываем только шестерёнку (название и стрелки уже в заголовке блока)."""
    key_open = f"dashboard_settings_{block_id}"
    if key_open not in st.session_state:
        st.session_state[key_open] = False

    has_layout_context = "dashboard_current_block" in st.session_state
    if has_layout_context:
        if st.button("⚙️", key=f"gear_{block_id}", help="Настройки блока"):
            st.session_state[key_open] = not st.session_state[key_open]
            st.rerun()
    else:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.subheader(title)
        with col2:
            if st.button("⚙️", key=f"gear_{block_id}", help="Настройки блока"):
                st.session_state[key_open] = not st.session_state[key_open]
                st.rerun()
    return st.session_state[key_open]


def _block_with_settings(title: str, block_id: str, render_content, render_settings):
    """Рендер блока: заголовок + шестерёнка, при открытых настройках — экспандер, затем контент."""
    with st.container():
        settings_open = _block_header(title, block_id)
        if settings_open:
            with st.expander("Настройки блока", expanded=True):
                render_settings(block_id)
                if st.button("Закрыть настройки", key=f"close_{block_id}"):
                    st.session_state[f"dashboard_settings_{block_id}"] = False
                    st.rerun()
        render_content(block_id)


def _apply_block_move(
    action: str, bid: str, side: str, index: int, total: int,
    left_ids: list[str], right_ids: list[str],
) -> None:
    """Перемещает блок: action in ('left','right','up','down')."""
    if action == "left" and side == "right" and bid in right_ids:
        right_ids.remove(bid)
        left_ids.append(bid)
    elif action == "right" and side == "left" and bid in left_ids:
        left_ids.remove(bid)
        right_ids.append(bid)
    elif action == "up" and index > 0:
        if side == "left":
            left_ids[index], left_ids[index - 1] = left_ids[index - 1], left_ids[index]
        else:
            right_ids[index], right_ids[index - 1] = right_ids[index - 1], right_ids[index]
    elif action == "down" and index < total - 1:
        if side == "left":
            left_ids[index], left_ids[index + 1] = left_ids[index + 1], left_ids[index]
        else:
            right_ids[index], right_ids[index + 1] = right_ids[index + 1], right_ids[index]


def _render_move_arrows(bid: str, side: str, index: int, total: int, left_ids: list[str], right_ids: list[str]) -> None:
    """Рендерит строку с кнопками ← ↑ ↓ → для переноса блока."""
    c0, c1, c2, c3 = st.columns(4)
    with c0:
        if st.button("←", key=f"arr_l_{bid}", help="В левую колонку", disabled=(side != "right")):
            _apply_block_move("left", bid, side, index, total, left_ids, right_ids)
            _save_dashboard_layout(left_ids, right_ids)
            st.rerun()
    with c1:
        if st.button("↑", key=f"arr_u_{bid}", help="Выше", disabled=(index <= 0)):
            _apply_block_move("up", bid, side, index, total, left_ids, right_ids)
            _save_dashboard_layout(left_ids, right_ids)
            st.rerun()
    with c2:
        if st.button("↓", key=f"arr_d_{bid}", help="Ниже", disabled=(index >= total - 1)):
            _apply_block_move("down", bid, side, index, total, left_ids, right_ids)
            _save_dashboard_layout(left_ids, right_ids)
            st.rerun()
    with c3:
        if st.button("→", key=f"arr_r_{bid}", help="В правую колонку", disabled=(side != "left")):
            _apply_block_move("right", bid, side, index, total, left_ids, right_ids)
            _save_dashboard_layout(left_ids, right_ids)
            st.rerun()


def _block_header_with_arrows(
    title: str, bid: str, side: str, index: int, total: int,
    left_ids: list[str], right_ids: list[str],
) -> None:
    """Заголовок блока: название и стрелки ← ↑ ↓ → для переноса."""
    col_title, c0, c1, c2, c3 = st.columns([3, 1, 1, 1, 1])
    with col_title:
        st.subheader(title)
    with c0:
        if st.button("←", key=f"arr_l_{bid}", help="В левую колонку", disabled=(side != "right")):
            _apply_block_move("left", bid, side, index, total, left_ids, right_ids)
            _save_dashboard_layout(left_ids, right_ids)
            st.rerun()
    with c1:
        if st.button("↑", key=f"arr_u_{bid}", help="Выше", disabled=(index <= 0)):
            _apply_block_move("up", bid, side, index, total, left_ids, right_ids)
            _save_dashboard_layout(left_ids, right_ids)
            st.rerun()
    with c2:
        if st.button("↓", key=f"arr_d_{bid}", help="Ниже", disabled=(index >= total - 1)):
            _apply_block_move("down", bid, side, index, total, left_ids, right_ids)
            _save_dashboard_layout(left_ids, right_ids)
            st.rerun()
    with c3:
        if st.button("→", key=f"arr_r_{bid}", help="В правую колонку", disabled=(side != "left")):
            _apply_block_move("right", bid, side, index, total, left_ids, right_ids)
            _save_dashboard_layout(left_ids, right_ids)
            st.rerun()


def _get(key: str, default):
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]


def _load_grant_dashboard_data() -> dict:
    """Загружает данные мониторинга гранта из JSON."""
    for path in (GRANT_DASHBOARD_PATH, GRANT_DASHBOARD_EXAMPLE):
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning("Ошибка чтения %s: %s", path.name, e)
    return {}


# ---------- Диалог с агентом (сессия и аудит) ----------
def _ensure_conversation() -> str | None:
    """Возвращает conversation_id для диалога с агентом; при необходимости создаёт или загружает из файла. None если API не настроен."""
    try:
        from dotenv import load_dotenv
        load_dotenv(PROJECT_ROOT / "config" / ".env")
        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass
    try:
        from src.yandex_ai_client import load_session_id, create_conversation, save_session_id
        conv_id = load_session_id()
        if conv_id:
            return conv_id
        new_id = create_conversation()
        save_session_id(new_id)
        return new_id
    except Exception as e:
        logger.warning("Агент не настроен для диалога: %s", e)
        return None


def _log_audit(conversation_id: str, prompt_len: int, reply_len: int) -> None:
    """Запись в data/chat_audit.jsonl для аудита."""
    try:
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        conv_hash = hashlib.sha256(conversation_id.encode()).hexdigest()[:16]
        record = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "conv_id_hash": conv_hash,
            "prompt_len": prompt_len,
            "reply_len": reply_len,
        }
        with open(AUDIT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.warning("Ошибка записи аудит-лога: %s", e)


def _agent_config_hint() -> str:
    """Краткая подсказка, что не задано (без вывода секретов)."""
    try:
        from dotenv import load_dotenv
        load_dotenv(PROJECT_ROOT / "config" / ".env")
        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass
    env_path = PROJECT_ROOT / "config" / ".env"
    parts = ["Проверьте **config/.env** (или корневой .env)."]
    if not env_path.exists():
        parts.append(f"Файл `config/.env` не найден по пути `{env_path}`.")
    key_ok = bool(os.environ.get("YANDEX_API_KEY", "").strip())
    folder_ok = bool(os.environ.get("YANDEX_FOLDER_ID", "").strip())
    if not key_ok:
        parts.append("**YANDEX_API_KEY** не задан или пуст.")
    if not folder_ok:
        parts.append("**YANDEX_FOLDER_ID** не задан или пуст (нужен идентификатор каталога, обычно b1g...).")
    if key_ok and folder_ok:
        parts.append("Ключ и каталог заданы — возможна ошибка сети или прав API (см. логи дашборда).")
    return " ".join(parts)


def _send_to_agent(prompt: str) -> str | None:
    """Отправляет сообщение агенту, возвращает ответ или строку с описанием ошибки."""
    conv_id = _ensure_conversation()
    if not conv_id:
        return "Не удалось подключиться к агенту. " + _agent_config_hint()
    try:
        from src.yandex_ai_client import ask, ask_in_conversation
        reply = ask_in_conversation(conv_id, prompt)
        if reply and "API вернул пустой ответ" in reply:
            try:
                fallback = ask(prompt)
                if fallback and fallback.strip():
                    return fallback + "\n\n_(Ответ получен одним запросом без сессии — при проблемах с диалогом.)_"
            except Exception as e:
                logger.debug("Fallback ask() не удался: %s", e)
        _log_audit(conv_id, len(prompt), len(reply or ""))
        return reply
    except Exception as e:
        logger.exception("Ошибка запроса к агенту: %s", e)
        return f"**Ошибка запроса:** {e}"


# ---------- Блок 1: Ближайшие сроки по гранту ----------
def _load_calendar_local(calendar_path: Path | None = None) -> list[dict]:
    path = calendar_path or _get("dashboard_schedule_calendar_path", "")
    if path:
        p = Path(path)
        if p.exists():
            try:
                with open(p, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    if CALENDAR_PATH.exists():
        with open(CALENDAR_PATH, encoding="utf-8") as f:
            return json.load(f)
    if CALENDAR_EXAMPLE.exists():
        with open(CALENDAR_EXAMPLE, encoding="utf-8") as f:
            return json.load(f)
    return []


def _load_schedule_events() -> list[dict]:
    """Загружает события: из Яндекс Календаря (CalDAV) или из локального JSON — по настройке блока."""
    source = _get("dashboard_schedule_source", "local")
    days = _get("dashboard_schedule_days", 30)
    today = datetime.utcnow().date()
    end = today + timedelta(days=days)

    if source == "yandex":
        try:
            from src.yandex_calendar_client import fetch_events, is_configured
            if not is_configured():
                return []
            return fetch_events(today, end)
        except Exception as e:
            logger.warning("Ошибка загрузки из Яндекс Календаря: %s", e)
            return []

    path_override = _get("dashboard_schedule_calendar_path", "")
    path = Path(path_override) if path_override else None
    return _load_calendar_local(path)


def _settings_schedule(block_id: str) -> None:
    try:
        from src.yandex_calendar_client import is_configured
        yandex_ok = is_configured()
    except Exception:
        yandex_ok = False
    source = _get("dashboard_schedule_source", "local")
    options = ["Локальный файл (grant_calendar.json)", "Яндекс Календарь (CalDAV)"]
    idx = 1 if source == "yandex" else 0
    choice = st.radio("Источник событий", options, index=idx, key=f"radio_source_{block_id}")
    st.session_state["dashboard_schedule_source"] = "yandex" if "Яндекс" in choice else "local"
    if "Яндекс" in choice and not yandex_ok:
        st.caption("Задайте YANDEX_CALENDAR_USER и YANDEX_CALENDAR_APP_PASSWORD в .env или в config (yandex_calendar). Пароль приложения: id.yandex.ru → Безопасность → Пароли приложений → Календарь.")
    days = st.number_input("Период (дней вперёд)", min_value=1, max_value=365, value=_get("dashboard_schedule_days", 30), key=f"ni_days_{block_id}")
    st.session_state["dashboard_schedule_days"] = days
    min_year = st.number_input("Показывать события не раньше года", min_value=2020, max_value=2030, value=_get("dashboard_schedule_min_year", 2026), key=f"ni_min_year_schedule_{block_id}")
    st.session_state["dashboard_schedule_min_year"] = min_year
    show_desc = st.checkbox("Показывать описание события", value=_get("dashboard_schedule_show_description", True), key=f"cb_desc_{block_id}")
    st.session_state["dashboard_schedule_show_description"] = show_desc
    path_override = st.text_input("Путь к локальному календарю (только для источника «Локальный файл»)", value=_get("dashboard_schedule_calendar_path", ""), key=f"path_cal_{block_id}")
    st.session_state["dashboard_schedule_calendar_path"] = path_override.strip()


def _content_schedule(block_id: str) -> None:
    days = _get("dashboard_schedule_days", 30)
    show_desc = _get("dashboard_schedule_show_description", True)
    source = _get("dashboard_schedule_source", "local")
    events = _load_schedule_events()
    if not events:
        if source == "yandex":
            st.info("Яндекс Календарь не настроен или за период событий нет. Задайте YANDEX_CALENDAR_USER и YANDEX_CALENDAR_APP_PASSWORD (пароль приложения Календарь) в .env или в настройках блока.")
        else:
            st.info("Календарь гранта пуст. Добавьте data/grant_calendar.json или переключите источник на «Яндекс Календарь» в настройках.")
        return
    today = datetime.utcnow().date()
    end = today + timedelta(days=days)
    min_year = _get("dashboard_schedule_min_year", 2026)
    min_date = datetime(min_year, 1, 1).date()
    upcoming = []
    for ev in events:
        try:
            d = datetime.fromisoformat(ev["date"].replace("Z", "")).date()
        except (KeyError, ValueError):
            continue
        if d < min_date:
            continue
        if today <= d <= end:
            upcoming.append((d, ev.get("title", ""), ev.get("description", ""), ev.get("address", "")))
    upcoming.sort(key=lambda x: x[0])
    if not upcoming:
        st.caption(f"В ближайшие {days} дн. событий по календарю нет.")
        return
    if source == "yandex":
        st.caption("Источник: Яндекс Календарь (CalDAV)")
    for d, title, desc, address in upcoming:
        days_left = (d - today).days
        st.markdown(f"**{d}** ({days_left} дн.) — {title}")
        if show_desc and desc:
            st.caption(desc)
        if address and address.strip():
            from urllib.parse import quote
            maps_url = "https://yandex.ru/maps/?text=" + quote(address.strip())
            st.link_button("🗺️ Открыть в Яндекс.Картах", maps_url)


def block_schedule() -> None:
    _block_with_settings("📅 Ближайшие сроки по гранту", "schedule", _content_schedule, _settings_schedule)


# ---------- Блок: Предстоящие задачи / напоминания ----------
def _settings_reminders(block_id: str) -> None:
    st.caption("Те же события, что в «Ближайшие сроки», с разметкой по срочности (за 7/3/1 дн., сегодня, просрочено).")
    min_year = st.number_input("Показывать события не раньше года", min_value=2020, max_value=2030, value=_get("dashboard_reminders_min_year", 2026), key=f"ni_reminders_min_year_{block_id}")
    st.session_state["dashboard_reminders_min_year"] = min_year
    st.caption("Email-напоминания отправляет scripts/grant_reminders.py по расписанию.")


def _content_reminders(block_id: str) -> None:
    events = _load_schedule_events()
    today = datetime.utcnow().date()
    min_year = _get("dashboard_reminders_min_year", 2026)
    cutoff = datetime(min_year, 1, 1).date()
    reminders_7 = []
    reminders_3 = []
    reminders_1 = []
    today_ev = []
    overdue = []
    for ev in events:
        try:
            d = datetime.fromisoformat(ev["date"].replace("Z", "")).date()
        except (KeyError, ValueError):
            continue
        if d < cutoff:
            continue
        days_left = (d - today).days
        title = ev.get("title", "Событие")
        if days_left < 0:
            overdue.append((d, title, days_left))
        elif days_left == 0:
            today_ev.append((d, title))
        elif days_left == 1:
            reminders_1.append((d, title))
        elif days_left == 3:
            reminders_3.append((d, title))
        elif days_left == 7:
            reminders_7.append((d, title))
    if not (reminders_7 or reminders_3 or reminders_1 or today_ev or overdue):
        st.caption("Нет событий в зоне напоминаний (за 7/3/1 дн., сегодня, просрочено). Добавьте события в календарь.")
        return
    for d, title, days_over in overdue:
        st.markdown(f"🔴 **Просрочено** ({abs(days_over)} дн.) — {title} (*{d}*)")
    for d, title in today_ev:
        st.markdown(f"🔥 **Сегодня** — {title}")
    for d, title in reminders_1:
        st.markdown(f"❗ **За 1 дн.** — {title} (*{d}*)")
    for d, title in reminders_3:
        st.markdown(f"🔔 **За 3 дн.** — {title} (*{d}*)")
    for d, title in reminders_7:
        st.markdown(f"⚠️ **За 7 дн.** — {title} (*{d}*)")


def block_reminders() -> None:
    _block_with_settings("🔔 Предстоящие задачи / напоминания", "reminders", _content_reminders, _settings_reminders)


# ---------- Блок: Ключевые контрольные точки (ККТ), АНО «Гранты Ямала» ----------
def _load_kkt() -> list[dict]:
    """Загружает ККТ из data/grant_kkt.json или из примера."""
    for path in (KKT_PATH, KKT_EXAMPLE):
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                return data.get("points", data) if isinstance(data, dict) else data
            except Exception as e:
                logger.warning("Ошибка чтения ККТ %s: %s", path.name, e)
    return []


def _settings_kkt(block_id: str) -> None:
    min_year = st.number_input("Показывать ККТ с года", min_value=2020, max_value=2030, value=_get("dashboard_kkt_min_year", 2026), key=f"ni_kkt_min_year_{block_id}")
    st.session_state["dashboard_kkt_min_year"] = min_year
    st.caption(
        "ККТ создаются и редактируются в личном кабинете АНО «Гранты Ямала». "
        "На дашборде — локальная копия из data/grant_kkt.json."
    )


def _content_kkt(block_id: str) -> None:
    points = _load_kkt()
    if not points:
        st.info("Добавьте данные в data/grant_kkt.json (можно скопировать из data/grant_kkt.example.json).")
        return
    min_year = _get("dashboard_kkt_min_year", 2026)
    try:
        filtered = [p for p in points if not (p.get("date_end") or "").strip() or int(((p.get("date_end") or "").strip())[:4]) >= min_year]
    except ValueError:
        filtered = points
    if not filtered:
        st.caption(f"Нет ККТ с годом срока не раньше {min_year}. Измените фильтр в настройках блока.")
        return
    today = datetime.utcnow().date()
    rows = []
    for i, p in enumerate(filtered, 1):
        date_end = (p.get("date_end") or "").strip()
        desc = p.get("description", "")
        expected = (p.get("expected_result") or "").strip()
        status = p.get("status", "not_started")
        st_label = STATUS_LABELS.get(status, status)
        overdue = ""
        if date_end:
            try:
                d = datetime.strptime(date_end[:10], "%Y-%m-%d").date()
                if d < today and status != "done":
                    overdue = " (просрочено)"
            except ValueError:
                pass
        rows.append({"№": i, "Контрольная точка": desc, "Срок": date_end, "Ожидаемый результат": expected, "Статус": st_label + overdue})
    st.dataframe(rows, width="stretch", hide_index=True, column_config={"Контрольная точка": st.column_config.TextColumn("Контрольная точка", width="medium")})
    st.caption("Источник: АНО «Гранты Ямала». Редактирование — в личном кабинете информационной системы грантодателя.")


def block_kkt() -> None:
    _block_with_settings("🎯 Ключевые контрольные точки", "kkt", _content_kkt, _settings_kkt)


def _load_all_grant_and_kkt_events(days_ahead: int = 365, min_year: int = 2026) -> list[dict]:
    """Объединяет события из календаря гранта (Яндекс или grant_calendar.json) и ККТ. Фильтр: дата не раньше min_year. Формат: {date, title, description, address}."""
    today = datetime.utcnow().date()
    end = today + timedelta(days=days_ahead)
    cutoff = datetime(min_year, 1, 1).date()
    out = []
    for ev in _load_schedule_events():
        try:
            d = datetime.fromisoformat(ev["date"].replace("Z", "")).date()
        except (KeyError, ValueError):
            continue
        if d < cutoff:
            continue
        if today <= d <= end:
            out.append({
                "date": d.isoformat(),
                "title": ev.get("title", "Событие"),
                "description": ev.get("description", ""),
                "address": ev.get("address", ""),
            })
    for p in _load_kkt():
        date_end = (p.get("date_end") or "").strip()
        if not date_end:
            continue
        try:
            d = datetime.strptime(date_end[:10], "%Y-%m-%d").date()
        except ValueError:
            continue
        if d < cutoff:
            continue
        if today <= d <= end:
            desc = p.get("description", "")
            expected = (p.get("expected_result") or "").strip()
            out.append({
                "date": d.isoformat(),
                "title": f"ККТ: {desc}" if desc else "ККТ",
                "description": f"Ожидаемый результат: {expected}" if expected else "",
                "address": "",
            })
    out.sort(key=lambda x: (x["date"], x["title"]))
    return out


# ---------- Блок 2: Аудит чата ----------
def _settings_audit(block_id: str) -> None:
    days = st.number_input("Период (дней назад)", min_value=1, max_value=365, value=_get("dashboard_audit_days", 7), key=f"ni_audit_days_{block_id}")
    st.session_state["dashboard_audit_days"] = days
    group = st.radio("Группировка", ["По дням", "По сессиям"], index=0 if _get("dashboard_audit_group", "day") == "day" else 1, key=f"radio_audit_{block_id}")
    st.session_state["dashboard_audit_group"] = "day" if "дням" in group else "session"
    limit = st.number_input("Макс. записей в таблице", min_value=10, max_value=1000, value=_get("dashboard_audit_limit", 100), key=f"ni_audit_lim_{block_id}")
    st.session_state["dashboard_audit_limit"] = limit


def _content_audit(block_id: str) -> None:
    days = _get("dashboard_audit_days", 7)
    limit = _get("dashboard_audit_limit", 100)
    group = _get("dashboard_audit_group", "day")
    if not AUDIT_LOG.exists():
        st.caption("Файл аудита чата пока пуст (data/chat_audit.jsonl).")
        return
    records = []
    try:
        with open(AUDIT_LOG, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        st.error(f"Ошибка чтения аудита: {e}")
        return
    if not records:
        st.caption("Записей в аудите нет.")
        return
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
    records = [r for r in records if (r.get("ts") or "") >= cutoff][-limit:]
    if not records:
        st.caption(f"За последние {days} дн. записей нет.")
        return
    if group == "day":
        by_day = {}
        for r in records:
            ts = (r.get("ts") or "")[:10]
            by_day.setdefault(ts, {"count": 0, "prompt_len": 0, "reply_len": 0})
            by_day[ts]["count"] += 1
            by_day[ts]["prompt_len"] += r.get("prompt_len", 0)
            by_day[ts]["reply_len"] += r.get("reply_len", 0)
        rows = [{"Дата": k, "Запросов": v["count"], "Символов запрос": v["prompt_len"], "Символов ответ": v["reply_len"]} for k, v in sorted(by_day.items(), reverse=True)]
    else:
        rows = [{"Время": r.get("ts", ""), "Хеш сессии": r.get("conv_id_hash", ""), "Длина запроса": r.get("prompt_len", 0), "Длина ответа": r.get("reply_len", 0)} for r in reversed(records)]
    st.dataframe(rows, width="stretch", hide_index=True)


def block_audit() -> None:
    _block_with_settings("📊 Аудит чата", "audit", _content_audit, _settings_audit)


# ---------- Блок 3: Статус агента и API ----------
def _settings_status(block_id: str) -> None:
    check_vs = st.checkbox("Проверять доступность Vector Store", value=_get("dashboard_status_check_vs", True), key=f"cb_vs_{block_id}")
    st.session_state["dashboard_status_check_vs"] = check_vs


def _content_status(block_id: str) -> None:
    config = load_config()
    project_cfg = config.get("project", {})
    ya_cfg = config.get("yandex_ai_studio", {})
    agent_name = ya_cfg.get("agent_name") or "—"
    version = project_cfg.get("version") or "—"

    try:
        from src.yandex_ai_client import get_yandex_ai_config
        ya = get_yandex_ai_config()
        has_key = bool((ya.get("api_key") or "").strip())
        folder_id = (ya.get("folder_id") or "").strip()
        model_spec = ya.get("agent_id") or ya.get("model") or "—"
    except Exception:
        has_key = False
        folder_id = ""
        model_spec = "—"

    st.markdown(f"**Проект:** {project_cfg.get('name', '—')} v{version}")
    st.markdown(f"**Агент:** {agent_name}")
    st.markdown(f"**Модель/агент в запросах:** {model_spec}")
    st.caption(f"API ключ: {'задан' if has_key else 'не задан'} | Folder ID: {'задан' if folder_id else 'не задан'}")

    configured = has_key and folder_id
    if not configured:
        st.warning("Настройте YANDEX_API_KEY и YANDEX_FOLDER_ID в .env (см. .env.example) для проверки API.")
        return

    try:
        from src.yandex_ai_client import get_client
        get_client()
        st.success("Подключение к Yandex AI Studio: OK")
    except Exception as e:
        st.error(f"Ошибка подключения: {e}")
        return

    if _get("dashboard_status_check_vs", True):
        try:
            from src.vector_store_client import list_vector_stores
            r = list_vector_stores(limit=5)
            items = getattr(r, "data", r) if not isinstance(r, list) else r or []
            st.caption(f"Vector Store: найдено индексов: {len(items)}")
        except Exception as e:
            err_str = str(e).lower()
            if "403" in err_str and ("permission" in err_str or "folder" in err_str):
                st.caption("Vector Store: 403. Проверьте, что в config/.env указан **YANDEX_FOLDER_ID** — идентификатор **каталога** (обычно b1g...), а не идентификатор агента.")
            else:
                st.caption(f"Vector Store: ошибка — {e}")


def block_status() -> None:
    _block_with_settings("🟢 Статус агента и API", "status", _content_status, _settings_status)


# ---------- Блок 4: Быстрые действия (grant_tools) — кнопки отправляют формулировки в диалог с агентом ----------
def _settings_tools(block_id: str) -> None:
    sort_by = st.radio("Сортировка", ["По id", "По названию"], index=1 if _get("dashboard_tools_sort", "title") == "title" else 0, key=f"radio_tools_{block_id}")
    st.session_state["dashboard_tools_sort"] = "title" if "названию" in sort_by else "id"


def _content_tools(block_id: str) -> None:
    config = load_config()
    tools = config.get("grant_tools", [])
    sort = _get("dashboard_tools_sort", "title")
    if sort == "title":
        tools = sorted(tools, key=lambda t: (t.get("title") or t.get("id") or ""))
    else:
        tools = sorted(tools, key=lambda t: (t.get("id") or t.get("title") or ""))
    if not tools:
        st.caption("В config нет grant_tools. Добавьте кнопки в config.json.")
        return
    st.caption("Нажмите — формулировка уйдёт в диалог слева.")
    for t in tools:
        title = t.get("title") or t.get("id") or "—"
        prompt = (t.get("prompt") or "").strip()
        if st.button(title, key=f"tool_btn_{t.get('id', title)}", width="stretch"):
            if "dashboard_prompt_to_send" not in st.session_state:
                st.session_state.dashboard_prompt_to_send = []
            st.session_state.dashboard_prompt_to_send.append(prompt)
            st.rerun()


def block_tools() -> None:
    _block_with_settings("🔘 Быстрые действия по гранту", "tools", _content_tools, _settings_tools)


# ---------- Блок 5: База знаний (Vector Store) ----------
def _settings_vs(block_id: str) -> None:
    limit = st.number_input("Макс. файлов для сводки", min_value=5, max_value=200, value=_get("dashboard_vs_files_limit", 50), key=f"ni_vs_lim_{block_id}")
    st.session_state["dashboard_vs_files_limit"] = limit
    st.caption("Сводка строится по первым N файлам индекса.")


def _content_vs(block_id: str) -> None:
    config = load_config()
    vs_id = (
        os.environ.get("YANDEX_VECTOR_STORE_ID", "").strip()
        or (config.get("yandex_ai_studio", {}) or {}).get("vector_store_id") or ""
    ).strip()
    if not vs_id:
        st.info(
            "Задайте **vector_store_id**: в `config/config.json` — `yandex_ai_studio.vector_store_id` "
            "или в `config/.env` — `YANDEX_VECTOR_STORE_ID` (ID поискового индекса в Yandex AI Studio)."
        )
        return
    limit = _get("dashboard_vs_files_limit", 20)
    try:
        from src.vector_store_client import get_vector_store, list_vector_store_files
        vs = get_vector_store(vs_id)
        name = getattr(vs, "name", None) or vs_id
        r = list_vector_store_files(vs_id, limit=limit, status=None)
        items = getattr(r, "data", r) if not isinstance(r, list) else r or []
        # Сводные данные
        total_bytes = 0
        by_status = {}
        for f in items:
            size = getattr(f, "bytes", None)
            if size is not None:
                total_bytes += int(size)
            stt = getattr(f, "status", None) or "—"
            by_status[stt] = by_status.get(stt, 0) + 1
        def _fmt_size(b: int) -> str:
            if b < 1024:
                return f"{b} B"
            if b < 1024 * 1024:
                return f"{b / 1024:.1f} KB"
            return f"{b / (1024 * 1024):.1f} MB"
        st.caption(f"**Индекс:** {name}")
        st.metric("Файлов", len(items))
        st.metric("Общий размер", _fmt_size(total_bytes) if total_bytes else "—")
        if by_status:
            st.caption("По статусам: " + ", ".join(f"{s}: {n}" for s, n in sorted(by_status.items())))
        if not items:
            st.caption("В индексе пока нет файлов.")
    except Exception as e:
        st.error(f"Ошибка Vector Store: {e}")


def block_vector_store() -> None:
    _block_with_settings("📚 База знаний (Vector Store)", "vector_store", _content_vs, _settings_vs)


# ---------- Блок: Управление рисками ----------
def _load_risks() -> list[dict]:
    for path in (RISKS_PATH, RISKS_EXAMPLE):
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                return data if isinstance(data, list) else data.get("risks", [])
            except Exception as e:
                logger.warning("Ошибка чтения рисков %s: %s", path.name, e)
    return []


def _settings_risks(block_id: str) -> None:
    st.caption("Данные из data/grant_risks.json (скопируйте из grant_risks.example.json). Редактирование — вручную в файле или добавьте форму в настройках.")


def _content_risks(block_id: str) -> None:
    items = _load_risks()
    if not items:
        st.info("Добавьте данные в data/grant_risks.json (пример: data/grant_risks.example.json).")
        return
    rows = []
    for r in items:
        rows.append({
            "Описание": r.get("description", ""),
            "Вероятность": r.get("probability", ""),
            "Влияние": r.get("impact", ""),
            "Митигация": r.get("mitigation", ""),
            "Статус": r.get("status", ""),
        })
    st.dataframe(rows, width="stretch", hide_index=True, column_config={"Описание": st.column_config.TextColumn("Описание", width="medium"), "Митигация": st.column_config.TextColumn("Митигация", width="medium")})


def block_risks() -> None:
    _block_with_settings("⚠️ Управление рисками", "risks", _content_risks, _settings_risks)


# ---------- Блок: Статистика использования агента ----------
def _settings_agent_stats(block_id: str) -> None:
    days = st.number_input("Период (дней назад)", min_value=1, max_value=365, value=_get("dashboard_agent_stats_days", 30), key=f"ni_agent_stats_days_{block_id}")
    st.session_state["dashboard_agent_stats_days"] = days


def _content_agent_stats(block_id: str) -> None:
    days = _get("dashboard_agent_stats_days", 30)
    cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
    if not AUDIT_LOG.exists():
        st.caption("Файл аудита чата пуст (data/chat_audit.jsonl).")
        return
    records = []
    try:
        with open(AUDIT_LOG, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    if (r.get("ts") or "") >= cutoff:
                        records.append(r)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        st.error(f"Ошибка чтения аудита: {e}")
        return
    if not records:
        st.caption(f"За последние {days} дн. записей нет.")
        return
    by_day: dict[str, dict[str, Any]] = {}
    for r in records:
        ts = (r.get("ts") or "")[:10]
        if ts not in by_day:
            by_day[ts] = {"count": 0, "prompt_len": 0, "reply_len": 0}
        by_day[ts]["count"] += 1
        by_day[ts]["prompt_len"] += r.get("prompt_len", 0)
        by_day[ts]["reply_len"] += r.get("reply_len", 0)
    total_requests = sum(d["count"] for d in by_day.values())
    total_prompt = sum(d["prompt_len"] for d in by_day.values())
    total_reply = sum(d["reply_len"] for d in by_day.values())
    st.metric("Запросов к агенту", total_requests)
    st.metric("Символов (запросы)", total_prompt)
    st.metric("Символов (ответы)", total_reply)
    sorted_days = sorted(by_day.items(), key=lambda x: x[0])
    if sorted_days:
        chart_data = [{"Дата": d, "Запросов": v["count"]} for d, v in sorted_days]
        st.bar_chart(chart_data, x="Дата", y="Запросов", height=200)


def block_agent_stats() -> None:
    _block_with_settings("📈 Статистика использования агента", "agent_stats", _content_agent_stats, _settings_agent_stats)


# ---------- Блок: Настройки уведомлений ----------
def _load_notification_settings() -> dict:
    for path in (NOTIFICATION_SETTINGS_PATH, NOTIFICATION_SETTINGS_EXAMPLE):
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning("Ошибка чтения notification_settings %s: %s", path.name, e)
    return {"email": "", "reminders_enabled": True, "days_before": [7, 3, 1]}


def _save_notification_settings(data: dict) -> bool:
    try:
        NOTIFICATION_SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(NOTIFICATION_SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.warning("Ошибка сохранения notification_settings: %s", e)
        return False


def _settings_notifications(block_id: str) -> None:
    data = _load_notification_settings()
    email = st.text_input("Email для напоминаний", value=data.get("email", ""), key=f"notif_email_{block_id}")
    enabled = st.checkbox("Включить напоминания по срокам", value=data.get("reminders_enabled", True), key=f"notif_enabled_{block_id}")
    if st.button("Сохранить настройки", key=f"notif_save_{block_id}"):
        new_data = {"email": email.strip(), "reminders_enabled": enabled, "days_before": data.get("days_before", [7, 3, 1])}
        if _save_notification_settings(new_data):
            st.success("Сохранено. scripts/grant_reminders.py при запуске может учитывать email из data/notification_settings.json.")
        else:
            st.error("Ошибка сохранения.")
    st.caption("Получатель по умолчанию также задаётся в config/.env: NOTIFICATION_EMAIL. Отправка писем — scripts/grant_reminders.py.")


def _content_notifications(block_id: str) -> None:
    data = _load_notification_settings()
    st.caption(f"Email: {data.get('email') or '(не задан, используется NOTIFICATION_EMAIL из .env)'}")
    st.caption(f"Напоминания: {'включены' if data.get('reminders_enabled', True) else 'выключены'}.")


def block_notifications() -> None:
    _block_with_settings("🔔 Настройки уведомлений", "notifications", _content_notifications, _settings_notifications)


# ---------- Блок: Коммуникации с грантодателем ----------
def _load_communications() -> list[dict]:
    for path in (COMMUNICATIONS_PATH, COMMUNICATIONS_EXAMPLE):
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                return data if isinstance(data, list) else data.get("items", [])
            except Exception as e:
                logger.warning("Ошибка чтения communications %s: %s", path.name, e)
    return []


def _settings_communications(block_id: str) -> None:
    st.caption("Данные из data/grant_communications.json (пример: grant_communications.example.json).")


def _content_communications(block_id: str) -> None:
    items = _load_communications()
    if not items:
        st.info("Добавьте данные в data/grant_communications.json.")
        return
    rows = [{"Дата": c.get("date", ""), "Тема": c.get("topic", ""), "Тип": c.get("type", ""), "Статус": c.get("status", "")} for c in items]
    st.dataframe(rows, width="stretch", hide_index=True)


def block_communications() -> None:
    _block_with_settings("📧 Коммуникации с грантодателем", "communications", _content_communications, _settings_communications)


# ---------- Блок: Файловый архив ----------
def _load_documents_archive() -> list[dict]:
    for path in (DOCUMENTS_ARCHIVE_PATH, DOCUMENTS_ARCHIVE_EXAMPLE):
        if path.exists():
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                return data if isinstance(data, list) else data.get("documents", [])
            except Exception as e:
                logger.warning("Ошибка чтения documents_archive %s: %s", path.name, e)
    return []


def _settings_documents_archive(block_id: str) -> None:
    st.caption("Данные из data/grant_documents_archive.json (пример: grant_documents_archive.example.json).")


def _content_documents_archive(block_id: str) -> None:
    items = _load_documents_archive()
    if not items:
        st.info("Добавьте данные в data/grant_documents_archive.json.")
        return
    rows = [{"Название": d.get("name", ""), "Тип": d.get("type", ""), "Статус": d.get("status", ""), "Дата": d.get("date", "")} for d in items]
    st.dataframe(rows, width="stretch", hide_index=True)
    for i, d in enumerate(items):
        link = (d.get("link") or "").strip()
        if link:
            st.link_button(f"Открыть: {(d.get('name') or '')[:40]}", link, key=f"archive_link_{block_id}_{i}")


def block_documents_archive() -> None:
    _block_with_settings("📁 Файловый архив", "documents_archive", _content_documents_archive, _settings_documents_archive)


# ---------- Блок: Календарь (виджет месяц) ----------
def _settings_calendar_month(block_id: str) -> None:
    st.caption("Сетка месяца. Дни с событиями выделены. Источник событий — тот же, что в «Ближайшие сроки».")
    year = st.number_input("Год", min_value=2024, max_value=2030, value=_get("dashboard_calendar_month_year", datetime.utcnow().year), key=f"ni_cal_year_{block_id}")
    st.session_state["dashboard_calendar_month_year"] = year
    month = st.number_input("Месяц", min_value=1, max_value=12, value=_get("dashboard_calendar_month_month", datetime.utcnow().month), key=f"ni_cal_month_{block_id}")
    st.session_state["dashboard_calendar_month_month"] = month
    min_year = st.number_input("События не раньше года", min_value=2020, max_value=2030, value=_get("dashboard_calendar_month_min_year", 2026), key=f"ni_cal_min_year_{block_id}")
    st.session_state["dashboard_calendar_month_min_year"] = min_year


def _content_calendar_month(block_id: str) -> None:
    events = _load_schedule_events()
    today = datetime.utcnow().date()
    year = _get("dashboard_calendar_month_year", today.year)
    month = _get("dashboard_calendar_month_month", today.month)
    min_year = _get("dashboard_calendar_month_min_year", 2026)
    min_date = datetime(min_year, 1, 1).date()
    import calendar
    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdayscalendar(year, month)
    events_by_day: dict[int, list[str]] = {}
    for ev in events:
        try:
            d = datetime.fromisoformat(ev["date"].replace("Z", "")).date()
        except (KeyError, ValueError):
            continue
        if d < min_date:
            continue
        if d.year == year and d.month == month:
            events_by_day.setdefault(d.day, []).append(ev.get("title", "Событие"))
    weekdays = "Пн Вт Ср Чт Пт Сб Вс".split()
    header = " | ".join(weekdays)
    st.caption(f"**{year}, {month}**")
    lines = [header]
    for week in weeks:
        row = []
        for day in week:
            if day == 0:
                row.append("  ")
            else:
                mark = "•" if day in events_by_day else " "
                row.append(f"{day:2}{mark}")
        lines.append(" | ".join(row))
    st.text("\n".join(lines))
    st.caption("• — день с событием. Список событий по дням — в блоке «Ближайшие сроки».")


def block_calendar_month() -> None:
    _block_with_settings("📅 Календарь (месяц)", "calendar_month", _content_calendar_month, _settings_calendar_month)


# ---------- Блок: Календарь Нейропульс (отдельный фрейм) ----------
def _settings_neuropulse_cal(block_id: str) -> None:
    days = st.number_input("Период (дней вперёд)", min_value=1, max_value=365, value=_get("dashboard_neuropulse_days", 60), key=f"ni_neuropulse_days_{block_id}")
    st.session_state["dashboard_neuropulse_days"] = days
    min_year = st.number_input("События не раньше года", min_value=2020, max_value=2030, value=_get("dashboard_neuropulse_min_year", 2026), key=f"ni_neuropulse_min_year_{block_id}")
    st.session_state["dashboard_neuropulse_min_year"] = min_year
    show_desc = st.checkbox("Показывать описание", value=_get("dashboard_neuropulse_show_desc", True), key=f"cb_neuropulse_desc_{block_id}")
    st.session_state["dashboard_neuropulse_show_desc"] = show_desc
    st.caption("Показываются все события гранта (календарь + ККТ). Виджет — календарь Яндекса (YANDEX_CALENDAR_NEUROPULSE_EMBED_URL).")
    st.divider()
    st.caption("**Выгрузка в Яндекс.Календарь:** события из grant_calendar.json и ККТ из grant_kkt.json (с 2026 г.) можно создать в календаре.")
    if st.button("Выгрузить события гранта и ККТ в Яндекс.Календарь", key=f"btn_push_cal_{block_id}"):
        try:
            from src.yandex_calendar_client import push_grant_and_kkt_to_yandex_calendar, get_yandex_calendar_config
            cfg = get_yandex_calendar_config()
            url = (cfg.get("calendar_url") or cfg.get("neuropulse_calendar_url") or "").strip()
            if not url:
                st.error("Задайте YANDEX_CALENDAR_URL или YANDEX_CALENDAR_NEUROPULSE_URL в config/.env.")
            else:
                created, errors = push_grant_and_kkt_to_yandex_calendar(calendar_url=url)
                st.success(f"Создано событий в календаре: {created}. Ошибок: {errors}. Обновите календарь в calendar.yandex.ru.")
        except Exception as e:
            st.error(f"Ошибка выгрузки: {e}")


def _content_neuropulse_cal(block_id: str) -> None:
    try:
        from src.yandex_calendar_client import get_yandex_calendar_config
    except ImportError:
        st.info("Модуль Яндекс Календаря недоступен.")
        return
    cfg = get_yandex_calendar_config()
    embed_url = (cfg.get("neuropulse_embed_url") or "").strip()

    # Виджет календаря Яндекса (если задан embed URL)
    if embed_url:
        safe_url = embed_url.replace('"', "&quot;").replace("<", "").replace(">", "")
        iframe_html = (
            f'<iframe src="{safe_url}" width="800" height="450" frameborder="0" '
            'style="border: 1px solid #eee; max-width: 100%; box-sizing: border-box;"></iframe>'
        )
        st.components.v1.html(iframe_html, height=460)
    else:
        st.caption("Чтобы встроить виджет календаря, укажите **YANDEX_CALENDAR_NEUROPULSE_EMBED_URL** в config/.env (Экспорт → вставка на сайт в calendar.yandex.ru).")

    # Список: все события гранта и ККТ
    st.markdown("**Все события гранта и ККТ** (календарь + ключевые контрольные точки)")
    days = _get("dashboard_neuropulse_days", 60)
    min_year = _get("dashboard_neuropulse_min_year", 2026)
    show_desc = _get("dashboard_neuropulse_show_desc", True)
    today = datetime.utcnow().date()
    events = _load_all_grant_and_kkt_events(days_ahead=days, min_year=min_year)
    if not events:
        st.caption("За выбранный период событий гранта и ККТ нет. Добавьте данные в grant_calendar.json или grant_kkt.json (и выберите источник «Яндекс Календарь» в блоке «Ближайшие сроки»).")
        return
    # Экранирование для HTML
    def esc(s: str) -> str:
        return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    lines = []
    for ev in events:
        d = ev.get("date", "")
        title = esc(ev.get("title", "(без названия)"))
        desc = esc((ev.get("description") or "").strip())
        addr = esc((ev.get("address") or "").strip())
        days_left = (datetime.fromisoformat(d.replace("Z", "")).date() - today).days if d else 0
        lines.append(f'<div class="neuropulse-event"><strong>{d}</strong>')
        if days_left >= 0:
            lines.append(f' <span class="neuropulse-days">({days_left} дн.)</span>')
        lines.append(f' — {title}</div>')
        if show_desc and desc:
            lines.append(f'<div class="neuropulse-desc">{desc}</div>')
        if addr:
            lines.append(f'<div class="neuropulse-addr">📍 {addr}</div>')
    inner = "\n".join(lines)
    html = f"""
<style>
  .neuropulse-frame {{
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
    background: linear-gradient(180deg, #fafbfc 0%, #f0f4f8 100%);
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }}
  .neuropulse-frame .neuropulse-title {{
    font-size: 1.1rem;
    font-weight: 600;
    color: #1a237e;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #3f51b5;
  }}
  .neuropulse-event {{ margin: 0.6rem 0; color: #333; }}
  .neuropulse-days {{ color: #5c6bc0; font-weight: 500; }}
  .neuropulse-desc {{ font-size: 0.9em; color: #555; margin-left: 0.5rem; margin-bottom: 0.4rem; }}
  .neuropulse-addr {{ font-size: 0.85em; color: #666; margin-left: 0.5rem; }}
</style>
<div class="neuropulse-frame">
  <div class="neuropulse-title">📅 Все события гранта и ККТ</div>
  {inner}
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def block_neuropulse_calendar() -> None:
    _block_with_settings("📅 Календарь Нейропульс", "neuropulse_cal", _content_neuropulse_cal, _settings_neuropulse_cal)


# ---------- Блок 6: Ссылки и переходы ----------
def _settings_links(block_id: str) -> None:
    show_chat = st.checkbox("Показывать кнопку «Открыть чат»", value=_get("dashboard_links_show_chat", True), key=f"cb_chat_{block_id}")
    st.session_state["dashboard_links_show_chat"] = show_chat
    show_docs = st.checkbox("Показывать кнопку «Документация»", value=_get("dashboard_links_show_docs", True), key=f"cb_docs_{block_id}")
    st.session_state["dashboard_links_show_docs"] = show_docs
    chat_url = st.text_input("URL чата (если другой порт/хост)", value=_get("dashboard_links_chat_url", "http://localhost:8501"), key=f"url_chat_{block_id}")
    st.session_state["dashboard_links_chat_url"] = chat_url
    docs_url = st.text_input("URL документации", value=_get("dashboard_links_docs_url", ""), key=f"url_docs_{block_id}")
    st.session_state["dashboard_links_docs_url"] = docs_url


def _content_links(block_id: str) -> None:
    config = load_config()
    chat_url = _get("dashboard_links_chat_url", "http://localhost:8501")
    docs_url = _get("dashboard_links_docs_url", "")
    if _get("dashboard_links_show_chat", True):
        st.link_button("💬 Открыть чат", chat_url)
    if _get("dashboard_links_show_docs", True) and docs_url:
        st.link_button("📖 Документация", docs_url)
    elif _get("dashboard_links_show_docs", True):
        st.caption("Укажите URL документации в настройках блока.")
    disk_url = (config.get("yandex_disk") or {}).get("project_folder_url", "").strip()
    if disk_url:
        st.link_button("📁 Папка проекта на Яндекс.Диске", disk_url)


def block_links() -> None:
    _block_with_settings("🔗 Ссылки и переходы", "links", _content_links, _settings_links)


# ---------- Блок 7: Контакты по гранту ----------
def _extract_contacts_from_docx(docx_source: bytes | Path) -> list[dict]:
    """Извлекает контакты (ФИО, роль, email) из таблиц в .docx заявки на грант (команда/специалисты)."""
    import io
    from docx import Document

    if isinstance(docx_source, Path):
        doc = Document(str(docx_source))
    else:
        doc = Document(io.BytesIO(docx_source))

    # Ключевые слова для определения столбцов (нижний регистр)
    NAME_KEYS = ("фио", "ф.и.о", "имя", "фам")
    ROLE_KEYS = ("должность", "роль", "позиция", "функция", "обязанност")
    EMAIL_KEYS = ("email", "e-mail", "почта", "эл. почта", "электронная почта")

    def col_index(row_cells, keys_tuple) -> int | None:
        for i, cell in enumerate(row_cells):
            t = (cell.text or "").strip().lower()
            for k in keys_tuple:
                if k in t:
                    return i
        return None

    for table in doc.tables:
        if not table.rows:
            continue
        header = table.rows[0].cells
        texts = [(c.text or "").strip().lower() for c in header]
        i_name = col_index(header, NAME_KEYS)
        i_role = col_index(header, ROLE_KEYS)
        i_email = col_index(header, EMAIL_KEYS)
        if i_name is None and i_role is None:
            continue
        if i_name is None:
            i_name = 0
        if i_role is None:
            i_role = i_name + 1 if len(header) > i_name + 1 else i_name
        if i_email is None:
            i_email = max(i_name, i_role) + 1 if len(header) > max(i_name, i_role) + 1 else i_role

        out = []
        for row in table.rows[1:]:
            cells = row.cells
            n = len(cells)
            name = (cells[i_name].text or "").strip() if n > i_name else ""
            role = (cells[i_role].text or "").strip() if n > i_role else ""
            email = (cells[i_email].text or "").strip() if n > i_email else ""
            if name or role or email:
                out.append({"name": name or "—", "role": role or "—", "email": email or "—"})
        if out:
            return out

    return []


def _load_grant_contacts() -> list[dict]:
    """Загружает контакты из data/grant_contacts.json или из примера."""
    if CONTACTS_PATH.exists():
        try:
            with open(CONTACTS_PATH, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    if CONTACTS_EXAMPLE.exists():
        try:
            with open(CONTACTS_EXAMPLE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def _settings_contacts(block_id: str) -> None:
    st.caption("Контакты читаются из data/grant_contacts.json. Скопируйте data/grant_contacts.example.json в grant_contacts.json и заполните.")


def _content_contacts(block_id: str) -> None:
    with st.expander("📥 Заполнить из заявки на грант (.docx)", expanded=False):
        st.caption("Загрузите файл заявки с таблицей команды (столбцы: ФИО/Имя, Должность/Роль, Email). Контакты будут записаны в data/grant_contacts.json.")
        uploaded = st.file_uploader("Файл заявки .docx", type=["docx"], key="contacts_from_application_upload")
        if uploaded and st.button("Извлечь специалистов и сохранить", key="btn_fill_contacts_from_app"):
            contacts = _extract_contacts_from_docx(uploaded.getvalue())
            if not contacts:
                st.warning("В документе не найдена таблица с командой (ожидаются столбцы типа ФИО, Должность, Email).")
            else:
                try:
                    CONTACTS_PATH.parent.mkdir(parents=True, exist_ok=True)
                    with open(CONTACTS_PATH, "w", encoding="utf-8") as f:
                        json.dump(contacts, f, ensure_ascii=False, indent=2)
                    st.success(f"Сохранено контактов: {len(contacts)}. Обновите блок или перезагрузите страницу.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Ошибка записи: {e}")

    contacts = _load_grant_contacts()
    if not contacts:
        st.info("Добавьте data/grant_contacts.json (скопируйте из grant_contacts.example.json) или загрузите заявку выше.")
        return
    rows = []
    for c in contacts:
        name = c.get("name") or "—"
        role = c.get("role") or "—"
        email = c.get("email") or "—"
        rows.append({"Имя": name, "Роль": role, "Email": email})
    st.dataframe(rows, width="stretch", hide_index=True)


def block_contacts() -> None:
    _block_with_settings("👥 Контакты по гранту", "contacts", _content_contacts, _settings_contacts)


# ---------- Мониторинг гранта «НейроПульс» (этапы, бюджет, показатели) ----------
def _settings_grant_header(block_id: str) -> None:
    st.caption("Данные из data/grant_project_dashboard.json (скопируйте из grant_project_dashboard.example.json).")


def _content_grant_header(block_id: str) -> None:
    data = _load_grant_dashboard_data()
    h = data.get("header") or {}
    title = h.get("title") or "НейроПульс"
    date_start = h.get("date_start") or "—"
    date_end = h.get("date_end") or "—"
    stage = h.get("current_stage") or "—"
    responsible = h.get("responsible") or "—"
    updated = h.get("updated_at") or "—"
    st.markdown(f"**{title}**")
    st.caption(f"Сроки: {date_start} — {date_end}  |  Этап: {stage}  |  Ответственный: {responsible}  |  Обновлено: {updated}")


def block_grant_header() -> None:
    _block_with_settings("📌 Общая информация по гранту", "grant_header", _content_grant_header, _settings_grant_header)


def _settings_stages(block_id: str) -> None:
    st.caption("Таблица этапов в data/grant_project_dashboard.json → stages. Статусы: not_started, in_progress, done, overdue.")


def _content_stages(block_id: str) -> None:
    data = _load_grant_dashboard_data()
    stages = data.get("stages") or []
    if not stages:
        st.info("Добавьте данные в data/grant_project_dashboard.json (секция stages). Пример: data/grant_project_dashboard.example.json")
        return
    rows = []
    for s in stages:
        status_key = (s.get("status") or "not_started")
        status_label = STATUS_LABELS.get(status_key, status_key)
        rows.append({
            "Этап": s.get("stage", ""),
            "Мероприятие": s.get("activity", ""),
            "План: даты": f"{s.get('plan_start') or '—'} — {s.get('plan_end') or '—'}",
            "Факт: даты": f"{s.get('fact_start') or '—'} — {s.get('fact_end') or '—'}",
            "Статус": status_label,
            "%": s.get("percent", 0),
        })
    st.dataframe(rows, width="stretch", hide_index=True)


def block_stages() -> None:
    _block_with_settings("📊 Прогресс по этапам", "grant_stages", _content_stages, _settings_stages)


def _settings_budget(block_id: str) -> None:
    st.caption("Бюджет в data/grant_project_dashboard.json → budget. Обновляйте fact в items.")


def _content_budget(block_id: str) -> None:
    data = _load_grant_dashboard_data()
    budget = data.get("budget") or {}
    total_plan = budget.get("total_plan", 0)
    total_fact = budget.get("total_fact", 0)
    items = budget.get("items") or []
    if not items and not total_plan:
        st.info("Добавьте бюджет в data/grant_project_dashboard.json (секция budget).")
        return
    st.markdown(f"**Бюджет:** план {total_plan:,.0f} руб.  |  факт {total_fact:,.0f} руб.")
    pct = (total_fact / total_plan * 100) if total_plan else 0
    st.progress(min(1.0, total_fact / total_plan) if total_plan else 0)
    st.caption(f"Освоение: {pct:.1f}%")
    rows = []
    for it in items:
        plan = it.get("plan", 0)
        fact = it.get("fact", 0)
        rows.append({"Статья": it.get("name", ""), "План (руб.)": plan, "Факт (руб.)": fact, "% освоения": (fact / plan * 100) if plan else 0})
        for ch in it.get("children") or []:
            rows.append({"Статья": "  • " + (ch.get("name") or ""), "План (руб.)": ch.get("plan", 0), "Факт (руб.)": ch.get("fact", 0), "% освоения": (ch.get("fact", 0) / ch.get("plan", 1) * 100) if ch.get("plan") else 0})
    st.dataframe(rows, width="stretch", hide_index=True)


def block_budget() -> None:
    _block_with_settings("💰 Финансовый мониторинг", "grant_budget", _content_budget, _settings_budget)


def _settings_indicators(block_id: str) -> None:
    st.caption("Показатели в data/grant_project_dashboard.json → indicators.")


def _content_indicators(block_id: str) -> None:
    data = _load_grant_dashboard_data()
    indicators = data.get("indicators") or []
    if not indicators:
        st.info("Добавьте показатели в data/grant_project_dashboard.json → indicators.")
        return
    rows = []
    for ind in indicators:
        target = ind.get("target", 0)
        fact = ind.get("fact", 0)
        suffix = ind.get("suffix", "")
        pct = (fact / target * 100) if target else 0
        rows.append({
            "Показатель": ind.get("name", ""),
            "Цель": f"{target}{suffix}",
            "Факт": f"{fact}{suffix}",
            "% выполнения": round(pct, 1),
        })
    st.dataframe(rows, width="stretch", hide_index=True)


def block_indicators() -> None:
    _block_with_settings("👥 Результаты с участниками", "grant_indicators", _content_indicators, _settings_indicators)


def _settings_info_activity(block_id: str) -> None:
    st.caption("Данные в data/grant_project_dashboard.json → info_activity.")


def _content_info_activity(block_id: str) -> None:
    data = _load_grant_dashboard_data()
    ia = data.get("info_activity") or {}
    if not ia:
        st.info("Добавьте секцию info_activity в data/grant_project_dashboard.json.")
        return
    reach_t = ia.get("reach_target", 0)
    reach_f = ia.get("reach_fact", 0)
    st.metric("Охват кампании (жители ЯНАО)", f"{reach_f:,}".replace(",", " ") if isinstance(reach_f, (int, float)) else reach_f, f"цель {reach_t:,}".replace(",", " ") if reach_t else "")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Публикации в СМИ", ia.get("publications", 0), "")
    with col2:
        st.metric("Участники круглого стола", ia.get("round_table_participants", 0), "")
    with col3:
        st.metric("НейроФест: участники", ia.get("neurofest_fact", 0), f"план {ia.get('neurofest_target', 100)}")


def block_info_activity() -> None:
    _block_with_settings("📢 Информационная активность", "grant_info_activity", _content_info_activity, _settings_info_activity)


# ---------- Паспорт: паспорт проекта и краткая история диалогов (автосохранение каждые 15 мин) ----------
def _write_passport_project() -> None:
    """Формирует и записывает паспорт проекта в Паспорт/паспорт_проекта.md."""
    PASSPORT_DIR.mkdir(parents=True, exist_ok=True)
    data = _load_grant_dashboard_data()
    lines = ["# Паспорт проекта\n", f"*Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"]
    h = (data.get("header") or {})
    lines.append("## Шапка\n")
    lines.append(f"- **Название:** {h.get('title', '—')}\n")
    lines.append(f"- **Период:** {h.get('date_start', '—')} — {h.get('date_end', '—')} ({h.get('months_duration', '—')} мес.)\n")
    lines.append(f"- **Текущий этап:** {h.get('current_stage', '—')}\n")
    lines.append(f"- **Ответственный:** {h.get('responsible', '—')}\n")
    stages = data.get("stages") or []
    lines.append("\n## Этапы\n")
    for s in stages:
        st_label = STATUS_LABELS.get(s.get("status"), s.get("status", ""))
        lines.append(f"- **{s.get('stage', '')}** — {s.get('activity', '')} | {s.get('plan_start', '')}–{s.get('plan_end', '')} | {st_label}\n")
    budget = data.get("budget") or {}
    lines.append("\n## Бюджет\n")
    lines.append(f"- План всего: {budget.get('total_plan', 0):,}\n")
    lines.append(f"- Факт: {budget.get('total_fact', 0):,}\n")
    lines.append(f"- Грант: {budget.get('grant_amount', 0):,} | Собственный вклад: {budget.get('own_contribution', 0):,}\n")
    ind = data.get("indicators") or []
    lines.append("\n## Показатели\n")
    for i in ind:
        lines.append(f"- {i.get('name', '')}: цель {i.get('target', '—')}{i.get('suffix', '')} | факт {i.get('fact', 0)}\n")
    info = data.get("info_activity") or {}
    lines.append("\n## Информационная активность\n")
    lines.append(f"- Охват: цель {info.get('reach_target', 0)}, факт {info.get('reach_fact', 0)}\n")
    lines.append(f"- Публикации: {info.get('publications', 0)} | Круглый стол: {info.get('round_table_participants', 0)}\n")
    lines.append(f"- НейроФест: цель {info.get('neurofest_target', 0)}, факт {info.get('neurofest_fact', 0)}\n")
    try:
        PASSPORT_PROJECT_FILE.write_text("".join(lines), encoding="utf-8")
    except Exception as e:
        logger.warning("Ошибка записи паспорта проекта: %s", e)


def _write_dialogue_history(session_messages: list[dict]) -> None:
    """Формирует и записывает краткую историю диалогов в Паспорт/история_диалогов.md."""
    PASSPORT_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["# Краткая история диалогов\n", f"*Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"]
    # Сводка по аудит-логу
    lines.append("## Аудит запросов (data/chat_audit.jsonl)\n")
    if not AUDIT_LOG.exists():
        lines.append("Записей пока нет.\n")
    else:
        records = []
        try:
            with open(AUDIT_LOG, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            lines.append(f"Ошибка чтения: {e}\n")
        if not records:
            lines.append("Записей нет.\n")
        else:
            by_day = {}
            for r in records[-500:]:
                ts = (r.get("ts") or "")[:10]
                by_day.setdefault(ts, {"count": 0, "prompt_len": 0, "reply_len": 0})
                by_day[ts]["count"] += 1
                by_day[ts]["prompt_len"] += r.get("prompt_len", 0)
                by_day[ts]["reply_len"] += r.get("reply_len", 0)
            lines.append("| Дата | Запросов | Символов запрос | Символов ответ |\n")
            lines.append("| --- | --- | --- | --- |\n")
            for day in sorted(by_day.keys(), reverse=True)[:30]:
                v = by_day[day]
                lines.append(f"| {day} | {v['count']} | {v['prompt_len']} | {v['reply_len']} |\n")
    # Текущая сессия дашборда (кратко)
    lines.append("\n## Текущая сессия дашборда (снимок)\n")
    if not session_messages:
        lines.append("Сообщений в текущей сессии нет.\n")
    else:
        for i, msg in enumerate(session_messages[-50:], 1):
            role = msg.get("role", "")
            content = (msg.get("content") or "")[:300]
            if len((msg.get("content") or "")) > 300:
                content += "..."
            content = content.replace("\n", " ")
            lines.append(f"- **{i}. {role}:** {content}\n")
    try:
        PASSPORT_HISTORY_FILE.write_text("".join(lines), encoding="utf-8")
    except Exception as e:
        logger.warning("Ошибка записи истории диалогов: %s", e)


def _passport_save_if_due(session_messages: list) -> None:
    """Если прошло 15 минут с последнего сохранения — записывает паспорт и историю, обновляет метку времени."""
    PASSPORT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    last_save = None
    if PASSPORT_LAST_SAVE_FILE.exists():
        try:
            last_save = datetime.fromisoformat(PASSPORT_LAST_SAVE_FILE.read_text(encoding="utf-8").strip())
        except Exception:
            pass
    if last_save is None or (now - last_save).total_seconds() >= PASSPORT_INTERVAL_MINUTES * 60:
        _write_passport_project()
        _write_dialogue_history(session_messages)
        try:
            PASSPORT_LAST_SAVE_FILE.write_text(now.isoformat(), encoding="utf-8")
        except Exception as e:
            logger.warning("Ошибка записи метки автосохранения Паспорт: %s", e)
        git_push_if_changes(commit_message="Автосохранение: паспорт и история диалогов")


# ---------- Проверка отчёта агентом ----------
def _extract_text_from_uploaded_file(uploaded_file) -> str | None:
    """Извлекает текст из загруженного файла (.txt или .docx). Макс. 50_000 символов."""
    max_chars = 50_000
    try:
        if uploaded_file.name.lower().endswith(".txt"):
            text = uploaded_file.getvalue().decode("utf-8", errors="replace")
        elif uploaded_file.name.lower().endswith(".docx"):
            import io
            from docx import Document
            doc = Document(io.BytesIO(uploaded_file.getvalue()))
            text = "\n".join(p.text for p in doc.paragraphs)
        else:
            return None
        return text[:max_chars] + ("…" if len(text) > max_chars else "")
    except Exception as e:
        logger.warning("Ошибка извлечения текста из файла: %s", e)
        return None


def _block_check_report() -> None:
    """Кнопка «Проверить отчёт агентом»: загрузка файла, отправка текста агенту."""
    if not _ensure_conversation():
        return
    with st.expander("📄 Проверить отчёт агентом", expanded=False):
        st.caption("Загрузите .txt или .docx — агент проверит отчёт на полноту и соответствие грантовым требованиям.")
        uploaded = st.file_uploader("Файл отчёта", type=["txt", "docx"], key="dashboard_report_upload")
        if uploaded and st.button("Отправить на проверку", key="btn_check_report"):
            text = _extract_text_from_uploaded_file(uploaded)
            if not text:
                st.error("Не удалось прочитать текст из файла. Поддерживаются .txt и .docx.")
                return
            prompt = "Проверь этот отчёт на полноту и соответствие грантовым требованиям. Укажи, если чего-то не хватает или есть замечания.\n\n---\n\n" + text
            st.session_state.dashboard_messages.append({"role": "user", "content": f"[Проверка отчёта: {uploaded.name}]"})
            with st.spinner("Агент проверяет отчёт..."):
                reply = _send_to_agent(prompt)
                st.session_state.dashboard_messages.append({"role": "assistant", "content": reply or "Ошибка запроса к агенту."})
            st.success("Ответ агента добавлен в диалог ниже.")
            st.rerun()


# ---------- Окно диалога с агентом ----------
def block_chat() -> None:
    """Окно диалога с агентом. При нажатии на быстрые действия по гранту их формулировки (prompt из config) отправляются агенту и ответ показывается здесь."""
    st.subheader("💬 Диалог с агентом")
    if not _ensure_conversation():
        st.warning("Настройте API (api_key, folder_id в config или .env) для диалога с агентом.")
        return

    if "dashboard_messages" not in st.session_state:
        st.session_state.dashboard_messages = []

    _block_check_report()

    # Обработка очереди от быстрых действий: формулировки (prompt) из кнопок уходят сюда
    if "dashboard_prompt_to_send" in st.session_state and st.session_state.dashboard_prompt_to_send:
        prompt = (st.session_state.dashboard_prompt_to_send.pop(0) or "").strip()
        if prompt:
            st.session_state.dashboard_messages.append({"role": "user", "content": prompt})
            with st.spinner("Ответ агента..."):
                reply = _send_to_agent(prompt)
                st.session_state.dashboard_messages.append({"role": "assistant", "content": reply or "Ошибка запроса. Проверьте настройки API в config/.env."})
        st.rerun()

    for msg in st.session_state.dashboard_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Введите сообщение или нажмите быстрый запрос справа"):
        st.session_state.dashboard_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Думаю..."):
                reply = _send_to_agent(prompt)
                text = reply if reply else "Ошибка запроса к агенту (пустой ответ). " + _agent_config_hint()
                st.markdown(text)
                st.session_state.dashboard_messages.append({"role": "assistant", "content": text})
        st.rerun()


def block_chat_and_tools() -> None:
    """Диалог с агентом и быстрые действия в одной колонке (2:1)."""
    chat_col, tools_col = st.columns([2, 1])
    with chat_col:
        block_chat()
    with tools_col:
        block_tools()


# Реестр блоков дашборда для настраиваемого расположения (перенос между колонками и порядок)
DEFAULT_LAYOUT_LEFT = [
    "grant_header", "stages", "kkt", "budget", "indicators", "risks", "info_activity",
    "schedule", "calendar_month", "reminders", "audit", "agent_stats", "status",
]
DEFAULT_LAYOUT_RIGHT = [
    "neuropulse_calendar", "chat_and_tools", "contacts", "notifications",
    "communications", "documents_archive", "links", "vector_store",
]


def _get_block_registry() -> dict:
    """Возвращает реестр блоков: id -> (название, функция отрисовки)."""
    return {
        "grant_header": ("Шапка гранта", block_grant_header),
        "stages": ("Этапы", block_stages),
        "kkt": ("Ключевые контрольные точки", block_kkt),
        "budget": ("Бюджет", block_budget),
        "indicators": ("Показатели", block_indicators),
        "risks": ("Риски", block_risks),
        "info_activity": ("Информационная активность", block_info_activity),
        "schedule": ("Ближайшие сроки", block_schedule),
        "calendar_month": ("Календарь (месяц)", block_calendar_month),
        "reminders": ("Напоминания", block_reminders),
        "neuropulse_calendar": ("Календарь Нейропульс", block_neuropulse_calendar),
        "audit": ("Аудит чата", block_audit),
        "agent_stats": ("Статус агента", block_agent_stats),
        "status": ("Настройки", block_status),
        "chat_and_tools": ("Диалог с агентом и быстрые действия", block_chat_and_tools),
        "contacts": ("Контакты по гранту", block_contacts),
        "notifications": ("Настройки уведомлений", block_notifications),
        "communications": ("Коммуникации с грантодателем", block_communications),
        "documents_archive": ("Файловый архив", block_documents_archive),
        "links": ("Ссылки", block_links),
        "vector_store": ("Vector Store", block_vector_store),
    }


def _load_dashboard_layout() -> tuple[list[str], list[str]]:
    """Загружает раскладку из data/dashboard_layout.json или возвращает умолчание."""
    registry = _get_block_registry()
    valid_ids = set(registry)
    if DASHBOARD_LAYOUT_PATH.exists():
        try:
            with open(DASHBOARD_LAYOUT_PATH, encoding="utf-8") as f:
                data = json.load(f)
            left = [x for x in (data.get("left") or []) if x in valid_ids]
            right = [x for x in (data.get("right") or []) if x in valid_ids]
            if left or right:
                # Добавить блоки, которых не было в сохранённой раскладке
                used = set(left) | set(right)
                for bid in valid_ids:
                    if bid not in used:
                        right.append(bid)
                return (left, right)
        except Exception:
            pass
    return (list(DEFAULT_LAYOUT_LEFT), list(DEFAULT_LAYOUT_RIGHT))


def _save_dashboard_layout(left: list[str], right: list[str]) -> None:
    """Сохраняет раскладку в data/dashboard_layout.json."""
    DASHBOARD_LAYOUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DASHBOARD_LAYOUT_PATH, "w", encoding="utf-8") as f:
        json.dump({"left": left, "right": right}, f, ensure_ascii=False, indent=2)


def _render_layout_editor() -> None:
    """Рендерит экспандер «Расположение блоков»: перенос между колонками и изменение порядка (аналог drag-and-drop)."""
    registry = _get_block_registry()
    key_layout = "dashboard_layout_blocks"
    st.session_state[key_layout] = _load_dashboard_layout()
    left_ids, right_ids = st.session_state[key_layout]

    with st.expander("📐 Расположение блоков (перенос и порядок)", expanded=False):
        st.caption("Меняйте порядок блоков и колонку (левая/правая). Изменения сохраняются в data/dashboard_layout.json.")
        lcol, rcol = st.columns(2)
        with lcol:
            st.markdown("**Левая колонка**")
            for i, bid in enumerate(left_ids):
                if bid not in registry:
                    continue
                title = registry[bid][0]
                a, b, c, d = st.columns([2, 1, 1, 1])
                with a:
                    st.markdown(f"• {title}")
                with b:
                    if i > 0 and st.button("↑", key=f"left_up_{bid}", help="Вверх"):
                        left_ids[i], left_ids[i - 1] = left_ids[i - 1], left_ids[i]
                        _save_dashboard_layout(left_ids, right_ids)
                        st.rerun()
                with c:
                    if i < len(left_ids) - 1 and st.button("↓", key=f"left_down_{bid}", help="Вниз"):
                        left_ids[i], left_ids[i + 1] = left_ids[i + 1], left_ids[i]
                        _save_dashboard_layout(left_ids, right_ids)
                        st.rerun()
                with d:
                    if st.button("→", key=f"left_to_right_{bid}", help="В правую колонку"):
                        left_ids.remove(bid)
                        right_ids.append(bid)
                        _save_dashboard_layout(left_ids, right_ids)
                        st.rerun()
        with rcol:
            st.markdown("**Правая колонка**")
            for i, bid in enumerate(right_ids):
                if bid not in registry:
                    continue
                title = registry[bid][0]
                a, b, c, d = st.columns([2, 1, 1, 1])
                with a:
                    st.markdown(f"• {title}")
                with b:
                    if st.button("←", key=f"right_to_left_{bid}", help="В левую колонку"):
                        right_ids.remove(bid)
                        left_ids.append(bid)
                        _save_dashboard_layout(left_ids, right_ids)
                        st.rerun()
                with c:
                    if i > 0 and st.button("↑", key=f"right_up_{bid}", help="Вверх"):
                        right_ids[i], right_ids[i - 1] = right_ids[i - 1], right_ids[i]
                        _save_dashboard_layout(left_ids, right_ids)
                        st.rerun()
                with d:
                    if i < len(right_ids) - 1 and st.button("↓", key=f"right_down_{bid}", help="Вниз"):
                        right_ids[i], right_ids[i + 1] = right_ids[i + 1], right_ids[i]
                        _save_dashboard_layout(left_ids, right_ids)
                        st.rerun()
        if st.button("Сбросить к умолчанию", key="layout_reset"):
            st.session_state[key_layout] = (list(DEFAULT_LAYOUT_LEFT), list(DEFAULT_LAYOUT_RIGHT))
            _save_dashboard_layout(DEFAULT_LAYOUT_LEFT, DEFAULT_LAYOUT_RIGHT)
            st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="Дашборд — Грантовый контролёр НейроПульс",
        page_icon="📋",
        layout="wide",
    )
    # Автосохранение Паспорт каждые 15 минут
    _passport_save_if_due(st.session_state.get("dashboard_messages", []))
    # Подтверждение после перезапуска (диалог с агентом не трогаем — он в session_state и сохраняется при rerun)
    if st.session_state.get("dashboard_restart_requested"):
        n_msg = len(st.session_state.get("dashboard_messages", []))
        st.success("✅ Дашборд перезапущен. Данные обновлены." + (f" Диалог с агентом сохранён ({n_msg} сообщ.)." if n_msg else ""))
        st.session_state["dashboard_restart_requested"] = False
    head_col1, head_col2 = st.columns([4, 1])
    with head_col1:
        st.title("📋 Дашборд проекта НейроПульс")
        st.caption("Мониторинг гранта, сроки, диалог с агентом. Расположение блоков настраивается в экспандере «Расположение блоков».")
    with head_col2:
        if st.button("🔄 Перезапустите дашборд", type="primary", help="Обновить данные и перезагрузить страницу. Диалог с агентом сохраняется."):
            st.session_state["dashboard_restart_requested"] = True
            st.rerun()

    left_ids, right_ids = _load_dashboard_layout()
    _render_layout_editor()
    st.session_state["dashboard_layout_left"] = left_ids
    st.session_state["dashboard_layout_right"] = right_ids

    registry = _get_block_registry()
    col1, col2 = st.columns(2)

    with col1:
        for i, bid in enumerate(left_ids):
            if bid not in registry:
                continue
            st.session_state["dashboard_current_block"] = {"bid": bid, "side": "left", "index": i, "total": len(left_ids)}
            _block_header_with_arrows(registry[bid][0], bid, "left", i, len(left_ids), left_ids, right_ids)
            registry[bid][1]()
            if i < len(left_ids) - 1:
                st.divider()

    with col2:
        for i, bid in enumerate(right_ids):
            if bid not in registry:
                continue
            st.session_state["dashboard_current_block"] = {"bid": bid, "side": "right", "index": i, "total": len(right_ids)}
            _block_header_with_arrows(registry[bid][0], bid, "right", i, len(right_ids), left_ids, right_ids)
            registry[bid][1]()
            if i < len(right_ids) - 1:
                st.divider()


if __name__ == "__main__":
    _register_atexit()
    main()

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

# Папка «Паспорт»: паспорт проекта и краткая история диалогов (автосохранение раз в 15 мин)
PASSPORT_DIR = PROJECT_ROOT / "Паспорт"
PASSPORT_PROJECT_FILE = PASSPORT_DIR / "паспорт_проекта.md"
PASSPORT_HISTORY_FILE = PASSPORT_DIR / "история_диалогов.md"
PASSPORT_LAST_SAVE_FILE = PASSPORT_DIR / ".last_passport_save"
PASSPORT_INTERVAL_MINUTES = 15

STATUS_LABELS = {"not_started": "⚪ Не начато", "in_progress": "🟡 В работе", "done": "🟢 Выполнено", "overdue": "🔴 Просрочено"}
STATUS_COLORS = {"not_started": "#888", "in_progress": "#d4a017", "done": "#28a745", "overdue": "#dc3545"}


def _block_header(title: str, block_id: str) -> bool:
    """Заголовок блока с шестерёнкой справа. Возвращает True, если нажали «Настройки»."""
    key_open = f"dashboard_settings_{block_id}"
    if key_open not in st.session_state:
        st.session_state[key_open] = False

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
    upcoming = []
    for ev in events:
        try:
            d = datetime.fromisoformat(ev["date"].replace("Z", "")).date()
        except (KeyError, ValueError):
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
    st.caption(
        "ККТ создаются и редактируются в личном кабинете АНО «Гранты Ямала» (раздел «Ключевые контрольные точки» / «Мониторинг»). "
        "На дашборде отображается локальная копия из data/grant_kkt.json."
    )


def _content_kkt(block_id: str) -> None:
    points = _load_kkt()
    if not points:
        st.info("Добавьте данные в data/grant_kkt.json (можно скопировать из data/grant_kkt.example.json).")
        return
    today = datetime.utcnow().date()
    rows = []
    for i, p in enumerate(points, 1):
        desc = p.get("description", "")
        date_end = (p.get("date_end") or "").strip()
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
    st.dataframe(rows, use_container_width=True, hide_index=True, column_config={"Контрольная точка": st.column_config.TextColumn("Контрольная точка", width="medium")})
    st.caption("Источник: АНО «Гранты Ямала». Редактирование — в личном кабинете информационной системы грантодателя.")


def block_kkt() -> None:
    _block_with_settings("🎯 Ключевые контрольные точки", "kkt", _content_kkt, _settings_kkt)


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
    st.dataframe(rows, use_container_width=True, hide_index=True)


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
        st.warning("Настройте YANDEX_API_KEY и YANDEX_FOLDER_ID в config/.env (или в config.json) для проверки API.")
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
        if st.button(title, key=f"tool_btn_{t.get('id', title)}", use_container_width=True):
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


# ---------- Блок: Календарь Нейропульс (отдельный фрейм) ----------
def _settings_neuropulse_cal(block_id: str) -> None:
    days = st.number_input("Период (дней вперёд)", min_value=1, max_value=365, value=_get("dashboard_neuropulse_days", 60), key=f"ni_neuropulse_days_{block_id}")
    st.session_state["dashboard_neuropulse_days"] = days
    show_desc = st.checkbox("Показывать описание", value=_get("dashboard_neuropulse_show_desc", True), key=f"cb_neuropulse_desc_{block_id}")
    st.session_state["dashboard_neuropulse_show_desc"] = show_desc
    st.caption("Календарь «Нейропульс» создайте в calendar.yandex.ru. URL возьмите из Экспорт календаря и укажите в config/.env: YANDEX_CALENDAR_NEUROPULSE_URL.")


def _content_neuropulse_cal(block_id: str) -> None:
    try:
        from src.yandex_calendar_client import fetch_neuropulse_events, get_yandex_calendar_config
    except ImportError:
        st.info("Модуль Яндекс Календаря недоступен.")
        return
    cfg = get_yandex_calendar_config()
    embed_url = (cfg.get("neuropulse_embed_url") or "").strip()
    caldav_url = (cfg.get("neuropulse_calendar_url") or "").strip()
    has_caldav = caldav_url and cfg.get("user") and cfg.get("password")

    # Виджет календаря — как в Яндексе: embed/week с layer_ids и tz_id (только публичный адрес, без private_token)
    if embed_url:
        safe_url = embed_url.replace('"', "&quot;").replace("<", "").replace(">", "")
        # Код как в «Вставка на сайт»: width 800, height 450, frameborder 0, border #eee
        iframe_html = (
            f'<iframe src="{safe_url}" width="800" height="450" frameborder="0" '
            'style="border: 1px solid #eee; max-width: 100%; box-sizing: border-box;"></iframe>'
        )
        st.components.v1.html(iframe_html, height=460)
    if not embed_url and not has_caldav:
        st.info(
            "Задайте календарь «Нейропульс»: **YANDEX_CALENDAR_NEUROPULSE_EMBED_URL** (публичный адрес из Экспорт в calendar.yandex.ru) "
            "и/или **YANDEX_CALENDAR_NEUROPULSE_URL** (CalDAV) + учётные данные в config/.env."
        )
        return
    if not has_caldav:
        st.caption("Список событий ниже загружается по CalDAV — укажите YANDEX_CALENDAR_NEUROPULSE_URL, YANDEX_CALENDAR_USER и YANDEX_CALENDAR_APP_PASSWORD.")
        return

    # Список событий по CalDAV
    if embed_url:
        st.markdown("**Список событий (CalDAV)**")
    days = _get("dashboard_neuropulse_days", 60)
    show_desc = _get("dashboard_neuropulse_show_desc", True)
    today = datetime.utcnow().date()
    end = today + timedelta(days=days)
    events = fetch_neuropulse_events(today, end)
    if not events:
        st.caption("В календаре «Нейропульс» за выбранный период событий нет.")
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
  <div class="neuropulse-title">📅 Календарь Нейропульс</div>
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
    contacts = _load_grant_contacts()
    if not contacts:
        st.info("Добавьте data/grant_contacts.json (скопируйте из grant_contacts.example.json) и заполните команду и партнёров по гранту.")
        return
    rows = []
    for c in contacts:
        name = c.get("name") or "—"
        role = c.get("role") or "—"
        email = c.get("email") or "—"
        rows.append({"Имя": name, "Роль": role, "Email": email})
    st.dataframe(rows, use_container_width=True, hide_index=True)


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
    st.dataframe(rows, use_container_width=True, hide_index=True)


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
    st.dataframe(rows, use_container_width=True, hide_index=True)


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
    st.dataframe(rows, use_container_width=True, hide_index=True)


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


# ---------- Окно диалога с агентом ----------
def block_chat() -> None:
    """Окно диалога с агентом. При нажатии на быстрые действия по гранту их формулировки (prompt из config) отправляются агенту и ответ показывается здесь."""
    st.subheader("💬 Диалог с агентом")
    if not _ensure_conversation():
        st.warning("Настройте API (api_key, folder_id в config или .env) для диалога с агентом.")
        return

    if "dashboard_messages" not in st.session_state:
        st.session_state.dashboard_messages = []

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


def main() -> None:
    st.set_page_config(
        page_title="Дашборд — Грантовый контролёр НейроПульс",
        page_icon="📋",
        layout="wide",
    )
    # Автосохранение Паспорт каждые 15 минут
    _passport_save_if_due(st.session_state.get("dashboard_messages", []))
    # Подтверждение после перезапуска
    if st.session_state.get("dashboard_restart_requested"):
        st.success("✅ Дашборд перезапущен. Данные обновлены.")
        st.session_state["dashboard_restart_requested"] = False
    head_col1, head_col2 = st.columns([4, 1])
    with head_col1:
        st.title("📋 Дашборд проекта НейроПульс")
        st.caption("Мониторинг гранта (этапы, бюджет, показатели), сроки, аудит чата, статус агента. Справа — диалог с агентом и быстрые действия.")
    with head_col2:
        if st.button("🔄 Перезапустите дашборд", type="primary", help="Обновить данные и перезагрузить страницу"):
            st.session_state["dashboard_restart_requested"] = True
            st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        block_grant_header()
        st.divider()
        block_stages()
        st.divider()
        block_kkt()
        st.divider()
        block_budget()
        st.divider()
        block_indicators()
        st.divider()
        block_info_activity()
        st.divider()
        block_schedule()
        st.divider()
        block_audit()
        st.divider()
        block_status()

    with col2:
        chat_col, tools_col = st.columns([2, 1])
        with chat_col:
            block_chat()
        with tools_col:
            block_tools()
        st.divider()
        block_contacts()
        st.divider()
        block_neuropulse_calendar()
        st.divider()
        block_links()
        st.divider()
        block_vector_store()


if __name__ == "__main__":
    _register_atexit()
    main()

"""
Дашборд проекта neuropulse-grant-agent.
Блоки: диалог с агентом, ближайшие сроки, аудит чата, статус агента, быстрые действия, Vector Store, ссылки.
При нажатии на быстрые действия формулировка уходит в диалог с агентом.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from datetime import datetime, timedelta

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import json
import logging

import streamlit as st

from src.agent_api_client import load_config, PROJECT_ROOT

logger = logging.getLogger(__name__)

AUDIT_LOG = PROJECT_ROOT / "data" / "chat_audit.jsonl"
CALENDAR_PATH = PROJECT_ROOT / "data" / "grant_calendar.json"
CALENDAR_EXAMPLE = PROJECT_ROOT / "data" / "grant_calendar.example.json"
CONTACTS_PATH = PROJECT_ROOT / "data" / "grant_contacts.json"
CONTACTS_EXAMPLE = PROJECT_ROOT / "data" / "grant_contacts.example.json"


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


# ---------- Диалог с агентом (сессия и аудит) ----------
def _ensure_conversation() -> str | None:
    """Возвращает conversation_id для диалога с агентом; при необходимости создаёт или загружает из файла. None если API не настроен."""
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


def _send_to_agent(prompt: str) -> str | None:
    """Отправляет сообщение агенту, возвращает ответ или None при ошибке."""
    conv_id = _ensure_conversation()
    if not conv_id:
        return None
    try:
        from src.yandex_ai_client import ask_in_conversation
        reply = ask_in_conversation(conv_id, prompt)
        _log_audit(conv_id, len(prompt), len(reply))
        return reply
    except Exception as e:
        logger.exception("Ошибка запроса к агенту: %s", e)
        return f"Ошибка: {e}"


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
    api_cfg = config.get("api", {})
    ya_cfg = config.get("yandex_ai_studio", {})
    project_cfg = config.get("project", {})

    has_key = bool(api_cfg.get("api_key"))
    folder_id = (ya_cfg.get("folder_id") or "").strip()
    agent_name = ya_cfg.get("agent_name") or "—"
    model = ya_cfg.get("model") or "—"
    version = project_cfg.get("version") or "—"

    st.markdown(f"**Проект:** {project_cfg.get('name', '—')} v{version}")
    st.markdown(f"**Агент:** {agent_name}")
    st.markdown(f"**Модель:** {model}")
    st.caption(f"API ключ: {'задан' if has_key else 'не задан'} | Folder ID: {'задан' if folder_id else 'не задан'}")

    configured = has_key and folder_id
    if not configured:
        st.warning("Настройте api_key и folder_id в config или .env для проверки API.")
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
    only_completed = st.checkbox("Показывать только файлы со статусом completed", value=_get("dashboard_vs_only_completed", True), key=f"cb_vs_compl_{block_id}")
    st.session_state["dashboard_vs_only_completed"] = only_completed
    limit = st.number_input("Макс. файлов в списке", min_value=5, max_value=100, value=_get("dashboard_vs_files_limit", 20), key=f"ni_vs_lim_{block_id}")
    st.session_state["dashboard_vs_files_limit"] = limit


def _content_vs(block_id: str) -> None:
    config = load_config()
    vs_id = (config.get("yandex_ai_studio", {}) or {}).get("vector_store_id") or ""
    if not vs_id:
        st.info("В конфиге не задан vector_store_id (yandex_ai_studio.vector_store_id).")
        return
    only_completed = _get("dashboard_vs_only_completed", True)
    limit = _get("dashboard_vs_files_limit", 20)
    try:
        from src.vector_store_client import get_vector_store, list_vector_store_files
        vs = get_vector_store(vs_id)
        name = getattr(vs, "name", None) or vs_id
        st.caption(f"Индекс: {name}")
        status_filter = "completed" if only_completed else None
        r = list_vector_store_files(vs_id, limit=limit, status=status_filter)
        items = getattr(r, "data", r) if not isinstance(r, list) else r or []
        if not items:
            st.caption("Файлов в индексе нет или ни один не в статусе completed.")
            return
        for f in items:
            fn = getattr(f, "filename", None) or getattr(f, "name", "(без имени)")
            stt = getattr(f, "status", "")
            st.markdown(f"- {fn} — {stt}")
    except Exception as e:
        st.error(f"Ошибка Vector Store: {e}")


def block_vector_store() -> None:
    _block_with_settings("📚 База знаний (Vector Store)", "vector_store", _content_vs, _settings_vs)


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
                st.session_state.dashboard_messages.append({"role": "assistant", "content": reply or "Ошибка запроса."})
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
                text = reply if reply else "Ошибка запроса к агенту."
                st.markdown(text)
                st.session_state.dashboard_messages.append({"role": "assistant", "content": text})
        st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="Дашборд — Грантовый контролёр НейроПульс",
        page_icon="📋",
        layout="wide",
    )
    st.title("📋 Дашборд проекта НейроПульс")
    st.caption("Обзор сроков, аудит чата, статус агента. Справа — диалог с агентом и быстрые действия (формулировки из кнопок уходят в диалог).")

    col1, col2 = st.columns(2)

    with col1:
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
        block_vector_store()
        st.divider()
        block_links()


if __name__ == "__main__":
    main()

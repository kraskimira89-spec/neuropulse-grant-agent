"""
Веб-чат к агенту «Грантовый контролёр НейроПульс» (Streamlit).
Выбор: новая тема / продолжить прошлый разговор. Кнопки быстрых действий по гранту.
Логирование для аудита (без персональных данных).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Корень проекта в sys.path, чтобы при запуске streamlit run src/web_chat.py находился модуль src
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import hashlib
import json
import logging

import streamlit as st

from src.agent_api_client import load_config
from src.yandex_ai_client import (
    create_conversation,
    load_session_id,
    ask_in_conversation,
    save_session_id,
)

PROJECT_ROOT = _PROJECT_ROOT
AUDIT_LOG = PROJECT_ROOT / "data" / "chat_audit.jsonl"
logger = logging.getLogger(__name__)


def _ensure_conversation() -> str:
    """Возвращает текущий conversation_id из session_state; при необходимости создаёт или загружает."""
    if "conversation_id" not in st.session_state:
        conv_id = load_session_id()
        if conv_id:
            st.session_state.conversation_id = conv_id
            st.session_state.continued = True
        else:
            st.session_state.conversation_id = create_conversation()
            save_session_id(st.session_state.conversation_id)
            st.session_state.continued = False
    return st.session_state.conversation_id


def _start_new_topic() -> None:
    """Новая тема: новый conversation_id, очистка истории в сессии."""
    st.session_state.conversation_id = create_conversation()
    save_session_id(st.session_state.conversation_id)
    if "messages" in st.session_state:
        st.session_state.messages = []
    st.session_state.continued = False
    st.rerun()


def _continue_previous() -> None:
    """Продолжить прошлый разговор: загрузить conversation_id из файла."""
    conv_id = load_session_id()
    if conv_id:
        st.session_state.conversation_id = conv_id
        if "messages" not in st.session_state:
            st.session_state.messages = []
        st.session_state.continued = True
        st.rerun()
    else:
        st.warning("Нет сохранённой сессии. Начните новый диалог.")


def _log_audit(conversation_id: str, prompt_len: int, reply_len: int) -> None:
    """Пишет в data/chat_audit.jsonl запись для аудита (без текста сообщений)."""
    try:
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        conv_hash = hashlib.sha256(conversation_id.encode()).hexdigest()[:16]
        from datetime import datetime
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


def _get_grant_tools() -> list[dict]:
    """Читает из config список быстрых действий (grant_tools)."""
    config = load_config()
    return config.get("grant_tools", [])


def main() -> None:
    st.set_page_config(
        page_title="Грантовый контролёр НейроПульс",
        page_icon="📋",
        layout="centered",
    )

    st.title("📋 Грантовый контролёр НейроПульс")
    st.caption("Ассистент по гранту губернатора и проекту Нейропульс. Задайте вопрос или выберите быстрый запрос.")

    # Боковая панель: новая тема / продолжить
    with st.sidebar:
        st.subheader("Сессия")
        if st.button("🆕 Новая тема", use_container_width=True):
            _start_new_topic()
        if st.button("▶️ Продолжить прошлый разговор", use_container_width=True):
            _continue_previous()
        st.divider()
        st.subheader("Быстрые действия по гранту")
        grant_tools = _get_grant_tools()
        for tool in grant_tools:
            if st.button(tool.get("title", tool.get("id", "")), key=tool.get("id", ""), use_container_width=True):
                if "prompt_to_send" not in st.session_state:
                    st.session_state.prompt_to_send = []
                st.session_state.prompt_to_send.append(tool.get("prompt", ""))
                st.rerun()

    # Инициализация истории и сессии
    if "messages" not in st.session_state:
        st.session_state.messages = []
    conv_id = _ensure_conversation()
    if getattr(st.session_state, "continued", False):
        st.info("Продолжение прошлого разговора. Контекст сохранён на стороне агента.")

    # Подставленный быстрый запрос
    if "prompt_to_send" in st.session_state and st.session_state.prompt_to_send:
        prompt = st.session_state.prompt_to_send.pop(0)
        if prompt and "messages" in st.session_state:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Ответ агента..."):
                try:
                    reply = ask_in_conversation(conv_id, prompt)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    _log_audit(conv_id, len(prompt), len(reply))
                except Exception as e:
                    st.session_state.messages.append({"role": "assistant", "content": f"Ошибка: {e}"})
            st.rerun()

    # Вывод истории
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Поле ввода
    if prompt := st.chat_input("Введите сообщение..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Думаю..."):
                try:
                    reply = ask_in_conversation(conv_id, prompt)
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    _log_audit(conv_id, len(prompt), len(reply))
                except Exception as e:
                    err = f"Ошибка запроса к агенту: {e}"
                    st.error(err)
                    st.session_state.messages.append({"role": "assistant", "content": err})


if __name__ == "__main__":
    main()

"""
Клиент для запросов к Yandex AI Studio (Responses API).
Читает api_key, folder_id, model из config/config.json или переменных окружения.
Поддерживается .env в config/.env и в корне проекта.
Диалог с историей: Conversations API (сессии с conversation_id).
"""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

from src.agent_api_client import PROJECT_ROOT, load_config

logger = logging.getLogger(__name__)

# Базовый URL API Yandex AI Studio
# Responses API для агентов (Conversations) требует rest-assistant — иначе ответы пустые
YANDEX_AI_BASE_URL = "https://ai.api.cloud.yandex.net/v1"
REST_ASSISTANT_BASE_URL = "https://rest-assistant.api.cloud.yandex.net/v1"

# Файл для сохранения ID последней сессии (чтобы продолжить диалог позже)
SESSION_ID_FILE = PROJECT_ROOT / "data" / ".last_conversation_id"


def _load_dotenv() -> None:
    """Загружает переменные из config/.env и .env в корне (если есть python-dotenv)."""
    try:
        from dotenv import load_dotenv
        config_env = PROJECT_ROOT / "config" / ".env"
        if config_env.exists():
            load_dotenv(config_env)
        load_dotenv(PROJECT_ROOT / ".env")
    except ImportError:
        pass


def get_yandex_ai_config() -> dict:
    """Читает настройки для Yandex AI Studio из config и env."""
    _load_dotenv()
    config = load_config()
    api_cfg = config.get("api", {})
    yandex_cfg = config.get("yandex_ai_studio", {})

    api_key = os.getenv("YANDEX_API_KEY") or api_cfg.get("api_key") or ""
    folder_id = os.getenv("YANDEX_FOLDER_ID") or yandex_cfg.get("folder_id") or ""
    agent_id = (os.getenv("YANDEX_AI_AGENT_ID") or yandex_cfg.get("agent_id") or "").strip()
    model = yandex_cfg.get("model") or "deepseek-v32"
    instructions = yandex_cfg.get("instructions") or ""
    vector_store_id = (os.getenv("YANDEX_VECTOR_STORE_ID") or yandex_cfg.get("vector_store_id") or "").strip()
    base_url = (os.getenv("YANDEX_AI_BASE_URL") or api_cfg.get("base_url") or "").strip() or YANDEX_AI_BASE_URL
    # Не переключаем на rest-assistant: при agent_id в URI там 400 Failed to get model; используем ai.api с URI модели (см. ask_in_conversation).

    return {
        "api_key": api_key,
        "folder_id": folder_id,
        "agent_id": agent_id,
        "model": model,
        "instructions": instructions,
        "vector_store_id": vector_store_id,
        "base_url": base_url.rstrip("/"),
    }


def _tools_for_vector_store(vector_store_id: str) -> list[dict] | None:
    """Возвращает tools с file_search для базы знаний, если vector_store_id задан."""
    if not vector_store_id:
        return None
    return [{"type": "file_search", "vector_store_ids": [vector_store_id]}]


def ask(question: str, instructions: str | None = None) -> str:
    """
    Отправляет один запрос к модели Yandex AI Studio и возвращает текст ответа.
    Перед вызовом задайте api_key и folder_id в config или в переменных YANDEX_API_KEY, YANDEX_FOLDER_ID.
    """
    import openai

    cfg = get_yandex_ai_config()
    if not cfg["api_key"] or not cfg["folder_id"]:
        raise ValueError(
            "Задайте api_key и folder_id в config/config.json (api.api_key, yandex_ai_studio.folder_id) "
            "или в переменных окружения YANDEX_API_KEY и YANDEX_FOLDER_ID"
        )

    client = openai.OpenAI(
        api_key=cfg["api_key"],
        base_url=cfg["base_url"],
        project=cfg["folder_id"],
    )

    model_spec = cfg["agent_id"] or cfg["model"]
    model_uri = f"gpt://{cfg['folder_id']}/{model_spec}"
    instr = instructions if instructions is not None else cfg["instructions"]
    tools = _tools_for_vector_store(cfg.get("vector_store_id") or "")

    logger.info("Запрос к Yandex AI Studio: %s%s", model_spec, " (с базой знаний)" if tools else "")
    kwargs = {
        "model": model_uri,
        "input": question,
        "instructions": instr or "",
        "max_output_tokens": 2000,
    }
    if tools:
        kwargs["tools"] = tools
    response = client.responses.create(**kwargs)

    text = getattr(response, "output_text", None)
    if text is None and response.output:
        part = response.output[0]
        if hasattr(part, "content") and part.content:
            text = getattr(part.content[0], "text", None) or str(part.content[0])
        else:
            text = str(part)
    if text is None:
        text = str(response)
    return text


def get_client():
    """Возвращает настроенный openai.OpenAI клиент для Yandex AI Studio."""
    import openai
    cfg = get_yandex_ai_config()
    if not cfg["api_key"] or not cfg["folder_id"]:
        raise ValueError(
            "Задайте api_key и folder_id в config или в переменных YANDEX_API_KEY, YANDEX_FOLDER_ID"
        )
    return openai.OpenAI(
        api_key=cfg["api_key"],
        base_url=cfg["base_url"],
        project=cfg["folder_id"],
    ), cfg


def create_conversation() -> str:
    """
    Создаёт новую сессию диалога (conversation). Возвращает conversation_id.
    Его можно сохранить и использовать для продолжения разговора позже.
    """
    client, cfg = get_client()
    try:
        conv = client.conversations.create()
    except Exception as e:
        if _is_forbidden_folder(e):
            _raise_403_folder_hint(e)
        raise
    logger.info("Создана сессия: %s", conv.id)
    return conv.id


def _is_conversation_not_found(err: BaseException) -> bool:
    """Проверяет, что ошибка — «сессия не найдена» (404)."""
    code = getattr(err, "status_code", None)
    if code == 404:
        return True
    msg = (getattr(err, "message", None) or str(err) or "").lower()
    return "not found" in msg and "conversation" in msg


def _is_forbidden_folder(err: BaseException) -> bool:
    """Проверяет, что ошибка 403 связана с правами на каталог / неверным folder_id."""
    code = getattr(err, "status_code", None)
    if code != 403:
        return False
    msg = (getattr(err, "message", None) or str(err) or "").lower()
    return "permission" in msg and ("folder" in msg or "ai.assistants" in msg)


def _raise_403_folder_hint(original: BaseException) -> None:
    """Выбрасывает понятное исключение с подсказкой про YANDEX_FOLDER_ID и права."""
    raise ValueError(
        "Ошибка 403: неверные права или неверный идентификатор каталога. "
        "YANDEX_FOLDER_ID должен быть идентификатором каталога (в консоли Yandex Cloud он обычно вида b1g...), "
        "а не идентификатором агента. Узнать folder_id: консоль Yandex Cloud → выберите каталог → Настройки каталога. "
        "Также нужна роль ai.assistants.editor (или editor/admin) для этого каталога. "
        "Подробнее: docs/Подключение-к-API-Yandex-AI-Studio.md"
    ) from original


def ask_in_conversation(
    conversation_id: str,
    message: str,
    instructions: str | None = None,
) -> str:
    """
    Отправляет сообщение в существующую сессию (conversation).
    Модель видит всю историю диалога в этой сессии.
    При 404 (сессия не найдена) создаёт новую сессию, сохраняет её и повторяет запрос один раз.
    """
    client, cfg = get_client()
    # #region agent log
    try:
        _log_path = PROJECT_ROOT / "debug-b70e7d.log"
        open(_log_path, "a", encoding="utf-8").write(json.dumps({"sessionId": "b70e7d", "hypothesisId": "H5b", "location": "yandex_ai_client:ask_in_conversation", "message": "client cfg", "data": {"base_url_host": "rest-assistant" if "rest-assistant" in (cfg.get("base_url") or "") else "other", "agent_id_set": bool(cfg.get("agent_id"))}, "timestamp": __import__("time").time() * 1000}) + "\n")
    except Exception:
        pass
    # #endregion
    # В Conversations API с agent_id в URI ai.api возвращал пустой output; rest-assistant даёт 400 Failed to get model. Используем URI модели + instructions + tools на ai.api.
    model_spec = cfg["agent_id"] or cfg["model"]
    if cfg["agent_id"]:
        model_spec = cfg["model"] or "deepseek-v32/latest"
    model_uri = f"gpt://{cfg['folder_id']}/{model_spec}"
    instr = instructions if instructions is not None else cfg["instructions"]
    tools = _tools_for_vector_store(cfg.get("vector_store_id") or "")

    def _do_request(conv_id: str):
        kwargs = {
            "model": model_uri,
            "conversation": conv_id,
            "input": message,
            "instructions": instr or "",
            "max_output_tokens": 2000,
        }
        if tools:
            kwargs["tools"] = tools
        return client.responses.create(**kwargs)

    try:
        response = _do_request(conversation_id)
    except Exception as e:
        if _is_forbidden_folder(e):
            _raise_403_folder_hint(e)
        if _is_conversation_not_found(e):
            logger.warning("Сессия %s не найдена (404), создаём новую.", conversation_id[:16])
            # #region agent log
            try:
                open(PROJECT_ROOT / "debug-b70e7d.log", "a", encoding="utf-8").write(json.dumps({"sessionId": "b70e7d", "hypothesisId": "H4", "location": "yandex_ai_client:404_retry", "message": "conversation not found, created new", "data": {"used_rest_assistant": "rest-assistant" in (cfg.get("base_url") or "")}, "timestamp": __import__("time").time() * 1000}) + "\n")
            except Exception:
                pass
            # #endregion
            new_id = create_conversation()
            save_session_id(new_id)
            response = _do_request(new_id)
        else:
            raise

    err = getattr(response, "error", None)
    if err is not None and getattr(response, "status", None) == "failed":
        msg = getattr(err, "message", None) or str(err)
        code = getattr(err, "code", None) or ""
        logger.warning("Ответ API с ошибкой: status=failed, error=%s", msg)
        return f"Ошибка API ({code}): {msg}"

    text = getattr(response, "output_text", None)
    if not (text and str(text).strip()):
        text = None
    if text is None and getattr(response, "output", None):
        parts_text = []
        for part in response.output:
            if hasattr(part, "content") and part.content:
                for c in part.content:
                    t = getattr(c, "text", None)
                    if t and str(t).strip():
                        parts_text.append(str(t).strip())
            else:
                s = str(part).strip()
                if s and s != "None":
                    parts_text.append(s)
        if parts_text:
            text = "\n".join(parts_text)
    if text is None:
        text = str(response).strip() if getattr(response, "__str__", None) else ""
    if not (text and str(text).strip()):
        logger.warning("Ответ API пустой. model_spec=%s, output_len=%s", model_spec, len(getattr(response, "output", None) or []))
        return (
            "API вернул пустой ответ. Возможные причины: "
            "неверный **YANDEX_AI_AGENT_ID** или **model** в config (должны соответствовать агенту в AI Studio), "
            "ограничения модели или таймаут. Проверьте логи дашборда или выполните в терминале: "
            "`python -m src.yandex_ai_client \"Тест\"` — если там будет ошибка, её текст подскажет причину."
        )
    return text


def save_session_id(conversation_id: str) -> None:
    """Сохраняет ID сессии в data/.last_conversation_id для последующего продолжения."""
    SESSION_ID_FILE.parent.mkdir(parents=True, exist_ok=True)
    SESSION_ID_FILE.write_text(conversation_id.strip(), encoding="utf-8")
    logger.info("ID сессии сохранён: %s", SESSION_ID_FILE)


def load_session_id() -> str | None:
    """Читает последний сохранённый conversation_id; если файла нет — None."""
    if not SESSION_ID_FILE.exists():
        return None
    return SESSION_ID_FILE.read_text(encoding="utf-8").strip() or None


def run_chat(force_new: bool = False) -> None:
    """
    Интерактивный чат с агентом. История сохраняется между запусками:
    по умолчанию продолжается последняя сессия (даже после закрытия терминала).
    Если force_new=True — создаётся новый диалог (старая сессия остаётся в облаке, но клиент переключается на новую).
    """
    conv_id = None if force_new else load_session_id()
    if conv_id:
        print(f"Продолжаем сессию (история сохранена): {conv_id[:24]}...", file=sys.stderr)
    else:
        conv_id = create_conversation()
        save_session_id(conv_id)
        print("Новая сессия. История будет сохраняться после закрытия терминала.", file=sys.stderr)
    print('Введите сообщение (пустая строка или "выход" — завершить).\n', file=sys.stderr)

    try:
        while True:
            try:
                line = input("Вы: ").strip()
            except EOFError:
                break
            if not line or line.lower() in ("exit", "quit", "выход"):
                break
            answer = ask_in_conversation(conv_id, line)
            print("Агент:", answer)
            print()
    except KeyboardInterrupt:
        print("\nВыход.", file=sys.stderr)
    print("Сессия сохранена. При следующем запуске --chat диалог продолжится.", file=sys.stderr)


def main() -> None:
    """Точка входа: один вопрос или интерактивный чат с историей (--chat, --resume)."""
    args = sys.argv[1:]
    if not args:
        print(
            "Использование:\n"
            "  python -m src.yandex_ai_client \"Ваш вопрос\"     — один запрос\n"
            "  python -m src.yandex_ai_client --chat             — диалог (история сохраняется, после закрытия терминала продолжится)\n"
            "  python -m src.yandex_ai_client --chat --new       — начать новый диалог с нуля",
            file=sys.stderr,
        )
        sys.exit(1)

    if args[0] in ("--chat", "-c"):
        force_new = "--new" in args or "-n" in args
        try:
            run_chat(force_new=force_new)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            logger.exception("Ошибка чата")
            print(f"Ошибка: {e}", file=sys.stderr)
            sys.exit(1)
        return

    question = " ".join(args)
    try:
        answer = ask(question)
        print(answer)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logger.exception("Ошибка запроса к API")
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

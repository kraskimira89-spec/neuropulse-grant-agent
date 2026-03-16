# Обучающие материалы: Yandex AI Studio

Локальные копии документации для работы с API. Источник: [Yandex AI Studio — Документация](https://aistudio.yandex.ru/docs/ru).

## Полная документация (сводный файл)

| Файл | Описание |
|------|----------|
| [yandex_ai_studio_docs.md](yandex_ai_studio_docs.md) | Полная документация Yandex AI Studio (о сервисе, Model Gallery, Agent Atelier, AI Search, MCP Hub, API, безопасность, квоты, тарификация, глоссарий, FAQ). Дата сборки: 16.03.2026. |

## Список материалов (по темам)

| Файл | Тема | URL |
|------|------|-----|
| [01-manage-context.md](01-manage-context.md) | Управление контекстом диалога | [manage-context](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/manage-context.html) |
| [02-create-prompt.md](02-create-prompt.md) | Базовый запрос (синхронный) | [create-prompt](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/create-prompt.html) |
| [03-background-request.md](03-background-request.md) | Запрос в фоновом режиме | [background-request](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/background-request.html) |
| [04-create-function-text-agent.md](04-create-function-text-agent.md) | Агент с вызовом функции | [create-function-text-agent](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-function-text-agent.html) |
| [05-create-websearch-text-agent.md](05-create-websearch-text-agent.md) | Агент с поиском в интернете | [create-websearch-text-agent](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-websearch-text-agent.html) |
| [06-create-filesearch-text-agent.md](06-create-filesearch-text-agent.md) | Агент с поиском по файлам | [create-filesearch-text-agent](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-filesearch-text-agent.html) |
| [07-use-code-interpreter.md](07-use-code-interpreter.md) | Code Interpreter | [use-code-interpreter](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/use-code-interpreter.html) |
| [08-create-voice-agent.md](08-create-voice-agent.md) | Голосовой агент (Realtime API, WebSocket) | [create-voice-agent](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-voice-agent.html) |

## Как пользоваться

- При реализации клиента Yandex AI Studio — ориентироваться на примеры из этих файлов.
- Базовый URL API: `https://ai.api.cloud.yandex.net/v1`.
- Клиент: `openai.OpenAI(api_key=..., base_url="https://ai.api.cloud.yandex.net/v1", project=FOLDER_ID)`.
- Модель в запросе: `gpt://{FOLDER_ID}/{MODEL}` (например `yandexgpt`, `yandexgpt-lite`, `qwen3-235b-a22b-fp8`).

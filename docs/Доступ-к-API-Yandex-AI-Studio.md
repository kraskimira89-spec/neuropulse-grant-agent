# Доступ к API Yandex AI Studio для программного взаимодействия

Сводка по аутентификации, базовым URL и обращению к агенту «Грантовый контролёр» и другим сервисам.

---

## Способы аутентификации

| Способ | Для кого | Как получить | Где использовать |
|--------|----------|--------------|------------------|
| **IAM-токен** | Аккаунт на Яндексе, федеративный или локальный пользователь | [Инструкция](https://yandex.cloud/ru/docs/iam/operations/iam-token/create) (действует 12 часов) | Заголовок `Authorization: Bearer <IAM-токен>` |
| **API-ключ** | Сервисный аккаунт (рекомендуется для автоматизации) | Через интерфейс AI Studio (см. ниже) или [YC CLI](https://yandex.cloud/ru/docs/iam/operations/api-key/create) | Заголовок `Authorization: Api-Key <API-ключ>` |

### Создание API-ключа в интерфейсе AI Studio

1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) нажмите **Создать API-ключ** в правом верхнем углу.
2. Задайте описание и срок действия (максимум 1 год).
3. Сохраните **идентификатор** и **секретный ключ** — после закрытия окна ключ будет недоступен.

Автоматически создаётся сервисный аккаунт с минимальными ролями (`ai.editor`, `serverless.mcpGateways.invoker` и др.) и API-ключ с областями действия для сервисов AI Studio.

---

## Базовые URL API

| API | Endpoint |
|-----|----------|
| **OpenAI-совместимые** (Chat Completions, Embeddings, Files, Vector Stores) | `https://ai.api.cloud.yandex.net/v1` |
| **Responses API** (рекомендуется для агентов) | `https://rest-assistant.api.cloud.yandex.net/v1` |
| **Realtime API** (голосовые агенты) | `wss://ai.api.cloud.yandex.net/v1/realtime` |

В проекте по умолчанию используется `https://ai.api.cloud.yandex.net/v1`; при необходимости base URL можно задать в конфиге или переменной окружения.

---

## Обращение к агенту «Грантовый контролёр»

Агент создан в **Agent Atelier** с инструкциями, инструментами и поисковым индексом. У него есть уникальный **идентификатор** (виден в интерфейсе). Для вызова через API укажите его в формате модели.

### Формат указания модели/агента

```
gpt://<folder_id>/<agent_id>
```

Где:
- **folder_id** — [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id), в котором создан агент (обычно вида `b1g...`). **Не путать с идентификатором агента.**
- **agent_id** — идентификатор сохранённого агента в AI Studio.

В проекте: задайте `YANDEX_FOLDER_ID` и либо `YANDEX_AI_AGENT_ID` (или `yandex_ai_studio.agent_id`), либо укажите `model` равным `agent_id` в конфиге.

### Пример запроса через Responses API (Python)

```python
import openai

FOLDER_ID = "ваш_folder_id"   # каталог, обычно b1g...
AGENT_ID = "ваш_agent_id"     # из интерфейса Agent Atelier
API_KEY = "ваш_api_ключ"

client = openai.OpenAI(
    api_key=API_KEY,
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
    project=FOLDER_ID
)

response = client.responses.create(
    model=f"gpt://{FOLDER_ID}/{AGENT_ID}",
    input="Какие мероприятия запланированы на следующую неделю?",
)

print(response.output_text)
print("Аннотации (источники):", getattr(response, "annotations", None))
```

### Передача контекста диалога

Используйте **Conversations API** (как в проекте: `conversations.create`, затем `responses.create` с `conversation=conversation_id`) либо параметр `previous_response_id`, равный `id` предыдущего ответа.

```python
# Первый запрос
resp1 = client.responses.create(
    model=f"gpt://{FOLDER_ID}/{AGENT_ID}",
    input="Привет, напомни, какие у меня задачи?"
)
# Второй запрос с контекстом
resp2 = client.responses.create(
    model=f"gpt://{FOLDER_ID}/{AGENT_ID}",
    previous_response_id=resp1.id,
    input="А что по срокам?"
)
```

---

## Работа с файлами и поисковыми индексами

Дополнительные файлы для агента загружаются через **Files API** и при необходимости привязываются к поисковому индексу (Vector Store). В проекте используется `src/vector_store_client.py`.

```python
# Загрузка файла
with open("report.pdf", "rb") as f:
    file = client.files.create(file=f, purpose="assistants")

# Использование в запросе (если агент поддерживает file_search)
response = client.responses.create(
    model=f"gpt://{FOLDER_ID}/{AGENT_ID}",
    input="Проверь этот отчёт",
    tools=[{"type": "file_search", "vector_store_ids": ["id_вашего_индекса"]}]
)
```

---

## Важные моменты

- **Роли**: У сервисного аккаунта должны быть роли на каталог: минимум `ai.assistants.editor` и `ai.languageModels.user`.
- **folder_id и agent_id**: В `YANDEX_FOLDER_ID` указывается только идентификатор **каталога** (обычно `b1g...`), не идентификатор агента. Иначе API вернёт 403.
- **Логирование**: Запросы по умолчанию логируются. Для отключения можно передать заголовок `x-data-logging-enabled: false`.
- **Квоты**: [Квоты и лимиты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html).
- **Тарификация**: [Правила тарификации](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html).

---

## Полезные ссылки

- [Аутентификация в API](https://aistudio.yandex.ru/docs/ru/ai-studio/api-ref/authentication.html)
- [Создание API-ключа](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/get-api-key.html)
- [Responses API (OpenAI-совместимый)](https://aistudio.yandex.ru/docs/ru/ai-studio/responses/index.html)
- [Работа с файлами](https://aistudio.yandex.ru/docs/ru/ai-studio/files/index.html)
- [Управление контекстом диалога (Conversations API)](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/conversations-api.html)

В проекте клиент к API: `src/yandex_ai_client.py`; настройка: [Подключение-к-API-Yandex-AI-Studio.md](Подключение-к-API-Yandex-AI-Studio.md).

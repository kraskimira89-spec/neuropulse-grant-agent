# Запрос в фоновом режиме

Источник: [Фоновый запрос Responses API](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/background-request.html)

## Когда использовать

Объёмные задачи (большие документы и т.п.). API возвращает ID задачи, соединение разрывается; статус и результат получают отдельно.

- Короткий ответ → [базовый запрос](02-create-prompt.md).
- Контекст диалога → [управление контекстом](01-manage-context.md).

---

## Пример

```python
import openai
import time

YANDEX_API_KEY = "<API-ключ>"
YANDEX_FOLDER_ID = "<идентификатор_каталога>"
YANDEX_MODEL = "yandexgpt"

client = openai.OpenAI(
    api_key=YANDEX_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=YANDEX_FOLDER_ID,
)

# 1. Создаем ответ в фоне
resp = client.responses.create(
    model=f"gpt://{YANDEX_FOLDER_ID}/{YANDEX_MODEL}",
    input="Сделай краткое резюме текста: '...'",
    background=True,
)
print("Задача отправлена:", resp.id)

# 2. Опрашиваем статус
while True:
    status = client.responses.retrieve(resp.id)
    print("Статус:", status.status)
    if status.status in ["completed", "failed", "cancelled"]:
        break
    time.sleep(2)

# 3. Результат
if status.status == "completed":
    print("Готовый ответ:", status.output_text)
else:
    print("Ошибка:", status.status)
```

## Статусы

- `completed` — успешно.
- `cancelled` — отменено.
- `failed` — ошибка.
- `in_progress` — выполняется.
- `queued` — в очереди.

Результат при `completed` — в `status.output_text`.

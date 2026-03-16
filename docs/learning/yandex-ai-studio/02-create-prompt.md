# Базовый запрос к модели (синхронный режим)

Источник: [Отправить базовый запрос](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/create-prompt.html)

## Responses API — короткий ответ

- Роль: `ai.languageModels.user`.
- Для чата с контекстом — см. [Управление контекстом](01-manage-context.md).
- Для больших задач — [фоновый режим](03-background-request.md).

---

## Пример запроса

```python
import openai

YANDEX_CLOUD_MODEL = "yandexgpt-lite"

client = openai.OpenAI(
    api_key=YANDEX_CLOUD_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=YANDEX_CLOUD_FOLDER
)

response = client.responses.create(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    input="Придумай 3 необычные идеи для стартапа в сфере путешествий.",
    temperature=0.8,
    max_output_tokens=1500
)

print(response.output[0].content[0].text)
# или
print(response.output_text)  # если доступно
```

Переменные: `export YANDEX_CLOUD_FOLDER=<id>`, `export YANDEX_CLOUD_API_KEY=<key>`.

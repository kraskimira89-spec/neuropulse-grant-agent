# Текстовый агент с поиском по файлам

Источник: [Агент с поиском по файлам](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-filesearch-text-agent.html)

Инструмент `file_search` — модель использует информацию из вашего поискового индекса (vector store).

---

## Подготовка

1. Создать поисковый индекс в AI Studio ([manage-searchindex](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/manage-searchindex.html#create-index)).
2. Получить `VECTOR_STORE_ID`.

---

## Пример

```python
import openai
import json

YANDEX_CLOUD_MODEL = "yandexgpt"

client = openai.OpenAI(
    api_key=YANDEX_CLOUD_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=YANDEX_CLOUD_FOLDER
)

response = client.responses.create(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    instructions="Ты — умный ассистент. Если спрашивают про отдых — ищи в подключенном индексе",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [VECTOR_STORE_ID]
    }],
    input="Где мне отдохнуть?"
)

print("Текст ответа:")
print(response.output_text)
print("\nПолный ответ (JSON):")
print(json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
```

Переменные: `YANDEX_CLOUD_FOLDER`, `YANDEX_CLOUD_API_KEY`, `VECTOR_STORE_ID`.

В ответе могут быть `file_search_call` с результатами и аннотации `file_citation` в тексте.

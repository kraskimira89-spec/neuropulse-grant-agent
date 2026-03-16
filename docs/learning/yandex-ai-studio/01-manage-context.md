# Управление контекстом диалога в AI Studio

Источник: [Управление контекстом диалога](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/manage-context.html)

## Три способа передавать контекст (Responses API)

1. **Ручное управление** — хранить историю на стороне приложения, явно передавать сообщения в `input`.
2. **Связывание ответов** — параметр `previous_response_id` для чата в реальном времени.
3. **Conversations API** — объект `conversation` с уникальным ID, диалог хранится на стороне API.

---

## Перед началом работы

- Сервисный аккаунт с ролями `ai.assistants.editor` и `ai.languageModels.user`.
- API-ключ с областью `yc.ai.foundationModels.execute`.
- Python 3.10+, venv, `pip install openai`.

---

## Conversations API

Создаётся объект `conversation`, передаётся в следующие запросы.

```python
import openai

YC_MODEL = "yandexgpt"

client = openai.OpenAI(
    api_key=YC_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=YC_FOLDER_ID
)

# 1) создаём conversation
conv = client.conversations.create()
print("conversation id:", conv.id)

# 2) первое сообщение
r1 = client.responses.create(
    model=f"gpt://{YC_FOLDER_ID}/{YC_MODEL}",
    conversation=conv.id,
    input=[
        {"role": "developer", "content": "Ты мой ассистент."},
        {"role": "user", "content": "Привет! Запомни: я живу в Серпухове."}
    ]
)
print("assistant:", r1.output_text)

# 3) продолжаем в том же conversation
r2 = client.responses.create(
    model=f"gpt://{YC_FOLDER_ID}/{YC_MODEL}",
    conversation=conv.id,
    input="В каком городе я живу?"
)
print("assistant:", r2.output_text)

# 4) с инструментом web_search
r3 = client.responses.create(
    model=f"gpt://{YC_FOLDER_ID}/{YC_MODEL}",
    conversation=conv.id,
    input="Какая погода будет на выходных?",
    tools=[{"type": "web_search"}]
)
print("assistant:", r3.output_text)
```

Переменные: `export YC_FOLDER_ID=<id>`, `export YC_API_KEY=<key>`.

---

## Связывание ответов (previous_response_id)

```python
import openai

YC_MODEL = "yandexgpt"
previous_id = None

client = openai.OpenAI(
    api_key=YC_API_KEY,
    project=YC_FOLDER_ID,
    base_url="https://ai.api.cloud.yandex.net/v1",
)

while True:
    user_input = input("Вы: ")
    if user_input.lower() in ("exit", "quit", "выход"):
        break

    response = client.responses.create(
        model=f"gpt://{YC_FOLDER_ID}/{YC_MODEL}",
        input=user_input,
        instructions="Ты — текстовый агент...",
        previous_response_id=previous_id
    )
    previous_id = response.id
    print("Агент:", response.output_text)
```

---

## Ручное управление (история в input)

```python
import openai

client = openai.OpenAI(
    api_key=YC_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=YC_FOLDER_ID,
)

response = client.responses.create(
    model=f"gpt://{YC_FOLDER_ID}/yandexgpt",
    input=[
        {"role": "user", "content": "Привет! Помоги с выбором подарка."},
        {"role": "assistant", "content": "Расскажи о себе"},
        {"role": "user", "content": "Меня зовут Глеб."},
        {"role": "user", "content": "Я люблю путешествовать."},
        {"role": "user", "content": "Увлекаюсь аниме и дизайном."},
    ],
)
print(response.output_text)
```

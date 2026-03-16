# Текстовый агент с вызовом функции

Источник: [Создать агента с вызовом функции](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-function-text-agent.html)

Агент может вызывать описанные функции; приложение выполняет их и передаёт результат обратно в модель.

---

## Пример: погода

```python
import openai
import json

YANDEX_CLOUD_MODEL = "yandexgpt"

client = openai.OpenAI(
    api_key=YANDEX_CLOUD_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=YANDEX_CLOUD_FOLDER
)

# 1. Определение функций
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Получить текущую погоду для указанного города.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "Название города"},
            },
            "required": ["city"],
        },
    },
]

def get_weather(city):
    return {"город": city, "температура": "12 °C", "состояние": "Облачно"}

input_list = [{"role": "user", "content": "Какая погода в Красноярске?"}]

# 2. Запрос с tools
response = client.responses.create(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    tools=tools,
    input=input_list,
)
input_list += response.output

# 3. Обработка function_call и передача результата
for item in response.output:
    if item.type == "function_call":
        if item.name == "get_weather":
            weather_info = get_weather(**json.loads(item.arguments))
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(weather_info)
            })

# 4. Второй запрос — финальный ответ
response = client.responses.create(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    instructions="Отвечай только данными о погоде из функции.",
    tools=tools,
    input=input_list,
)
print(response.output_text)
```

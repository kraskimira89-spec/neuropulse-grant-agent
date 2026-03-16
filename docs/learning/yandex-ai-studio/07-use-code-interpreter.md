# Code Interpreter

Источник: [Выполнить задачу с помощью Code Interpreter](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/use-code-interpreter.html)

**Preview.** Модель пишет и выполняет Python-код в изолированной среде. Полезно для расчётов, проверки и преобразования данных. Рекомендуются модели с большим контекстом (например Qwen).

---

## Роли и окружение

- Сервисный аккаунт: `ai.assistants.editor`, `ai.languageModels.user`.
- API-ключ с областью `yc.ai.foundationModels.execute`.

---

## Пример: презентация (stream + скачивание файлов)

```python
import openai
import json
import os

YC_MODEL = "qwen3-235b-a22b-fp8"
YC_API_KEY = os.getenv('YC_API_KEY')
YC_FOLDER_ID = os.getenv('YC_FOLDER_ID')

client = openai.OpenAI(
    api_key=YC_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=YC_FOLDER_ID
)

instruction = """
Ты программист на питоне и умеешь писать и выполнять код для решения поставленной задачи.
Проверь сначала наличие нужных тебе библиотек и если их нет – установи их.
"""
prompt = """
Сделай мне подробную презентацию в формате pptx про производные – что это такое, как их считать, добавь инфографики.
Слайдов должно быть не менее 5.
"""

stream = client.responses.create(
    model=f"gpt://{YC_FOLDER_ID}/{YC_MODEL}",
    input=prompt,
    tool_choice="auto",
    temperature=0.3,
    tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
    stream=True
)

resp_id = None
for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end='')
    elif event.type == "response.code_interpreter_call_code.delta":
        print(event.delta, end='')
    elif event.type == "response.code_interpreter_call_code.done":
        print(f"\n\nИтоговый код:\n{event.code}\n")
    elif event.type == "response.code_interpreter_call.done":
        print("\n[Код выполнен]\n")
    elif event.type == "response.in_progress":
        resp_id = event.response.id

# Полный ответ и скачивание файлов
response = client.responses.retrieve(resp_id)
os.makedirs("./downloaded_files", exist_ok=True)
for item in response.output:
    if item.type == "message":
        for content in item.content:
            if hasattr(content, 'annotations') and content.annotations:
                for annotation in content.annotations:
                    if annotation.type == "container_file_citation":
                        file_content = client.files.content(annotation.file_id)
                        local_path = os.path.join("./downloaded_files", annotation.filename)
                        with open(local_path, 'wb') as f:
                            f.write(file_content.read())
                        print(f"Сохранено: {local_path}")
```

Переменные: `export YC_FOLDER_ID=<id>`, `export YC_API_KEY=<key>`.

Файлы, созданные в контейнере (например pptx, png), доступны через `client.files.content(file_id)` и аннотации типа `container_file_citation`.

# Подключение к Yandex AI Studio по API

Краткая инструкция: как получить данные для доступа и отправить запрос к модели (в том числе к настройкам агента «Грантовый контролёр НейроПульс») из кода.

---

## 1. Что понадобится

- **API-ключ** — секретный ключ для доступа к API.
- **Идентификатор каталога (Folder ID)** — каталог в Yandex Cloud, в котором создан агент и квоты.

Без них запросы к API работать не будут.

---

## 2. Создать API-ключ

1. Откройте [интерфейс AI Studio](https://aistudio.yandex.cloud/platform/).
2. В **правом верхнем углу** нажмите **«Создать API-ключ»**.
3. При необходимости укажите описание и срок действия.
4. Нажмите **«Создать»**.
5. **Сразу скопируйте и сохраните** значение ключа (секрет). После закрытия окна его больше не покажут.

Не передавайте ключ посторонним и не публикуйте в репозитории. **Рекомендуется хранить ключ только в `.env` или `config/.env`** (они в `.gitignore`). Файл `config/config.json` отслеживается в Git — не указывайте в нём API-ключи. Если ключ когда-либо попадал в репозиторий, смените его в консоли Yandex Cloud.

---

## 3. Узнать идентификатор каталога (Folder ID)

1. В [AI Studio](https://aistudio.yandex.cloud/platform/) или [консоли Yandex Cloud](https://console.yandex.cloud/) выберите ваш **каталог** (например, `default`).
2. Откройте **настройки каталога** или страницу с информацией о каталоге.
3. Скопируйте **идентификатор каталога** — строка вида `b1gxxxxxxxxxxxxxxxxxx`.

Либо: в консоли в URL после `folderIds=` или в пути часто виден ID каталога. Подробнее: [Как получить ID каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id).

---

## 4. Куда подставить API-ключ и Folder ID

### Вариант А: файл конфигурации

Откройте `config/config.json` и заполните:

```json
{
  "api": {
    "base_url": "https://ai.api.cloud.yandex.net/v1",
    "api_key": "ваш_API_ключ_здесь",
    "timeout_seconds": 30
  },
  "yandex_ai_studio": {
    "agent_name": "Грантовый контролёр НейроПульс",
    "agent_id": "fvtqidaefjj4iktq733p",
    "folder_id": "ваш_идентификатор_каталога",
    "model": "deepseek-v32/latest"
  }
}
```

- `api.api_key` — секрет API-ключа.
- `yandex_ai_studio.folder_id` — идентификатор каталога.
- `yandex_ai_studio.model` — модель (например, `deepseek-v32` для DeepSeek; как в веб-интерфейсе агента).

**Не указывайте API-ключ в `config.json`** — файл отслеживается в Git. Храните ключ только в `.env` (см. вариант Б). Если ключ когда-либо попадал в репозиторий, смените его в консоли Yandex Cloud.

### Вариант Б: переменные окружения (.env) — рекомендуется

Создайте файл `.env` в папке **config** (`config/.env`) или в корне проекта. Оба варианта поддерживаются; `config/.env` удобен, когда все настройки лежат в `config/`. Файл `.env` не коммитится в Git (уже в `.gitignore`).

Пример **config/.env**:

```env
YANDEX_API_KEY=ваш_API_ключ
YANDEX_FOLDER_ID=ваш_идентификатор_каталога
```

Скрипт загружает переменные через `python-dotenv` из `config/.env` и из корневого `.env`.

---

## 5. Установка зависимости

В активированном виртуальном окружении проекта уже должна быть библиотека `openai`:

```bash
.\.venv\Scripts\Activate.ps1
pip install openai
```

---

## 6. Пример запроса к модели из Python

Yandex AI Studio поддерживает **OpenAI-совместимый API**. Вызов делается так же, как к модели OpenAI, но с `base_url` и `project` (Folder ID).

Однократный запрос (без сохранения диалога):

```python
import openai

API_KEY = "ваш_API_ключ"           # или из config / os.getenv
FOLDER_ID = "ваш_идентификатор_каталога"
MODEL = "deepseek-v32"             # как у агента в веб-интерфейсе

client = openai.OpenAI(
    api_key=API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=FOLDER_ID,
)

response = client.responses.create(
    model=f"gpt://{FOLDER_ID}/{MODEL}",
    input="Какие сроки подачи заявки на грант?",
    instructions="Ты — помощник по гранту губернатора и проекту Нейропульс. Отвечай кратко и по делу.",
    max_output_tokens=1000,
)

print(response.output_text)
```

Чат с сохранением контекста (несколько сообщений подряд) — см. [01-manage-context.md](learning/yandex-ai-studio/01-manage-context.md) в папке `docs/learning/yandex-ai-studio/`. передавать в `input` список сообщений `[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]` или использовать `previous_response_id` / Conversations API.

---

## 7. Пример через клиент проекта

В проекте есть модуль для вызова Yandex AI Studio: **`src/yandex_ai_client.py`**. Он читает `api_key`, `folder_id` и `model` из `config/config.json` (или из переменных окружения) и отправляет запрос к модели.

Запуск из корня проекта (с активированным `.venv`):

```bash
python -m src.yandex_ai_client "Ваш вопрос по гранту"
```

Перед первым запуском заполните в конфиге `api_key` и `yandex_ai_studio.folder_id` (и при необходимости `model`), как в шаге 4.

### Диалог с историей и запоминание сессий (API)

История **сохраняется между запусками**: даже после закрытия терминала или вкладки при следующем запуске `--chat` диалог продолжается (используется та же сессия в Yandex).

- **Чат с сохранением истории** (по умолчанию продолжается последняя сессия):
  ```bash
  python -m src.yandex_ai_client --chat
  ```
- **Начать новый диалог с нуля** (старая история остаётся в облаке, но клиент переключается на новую беседу):
  ```bash
  python -m src.yandex_ai_client --chat --new
  ```

ID сессии хранится в `data/.last_conversation_id`. В коде: `create_conversation()`, `ask_in_conversation(conversation_id, message)`, `save_session_id()`, `load_session_id()`.

---

## 8. Важно про агента в веб-интерфейсе и API

- В веб-интерфейсе вы настроили **агента** (модель + инструкция + инструменты). Его **ID** (`fvtqidaefjj4iktq733p`) в текущем API не передаётся в запрос.
- По API вызывается **модель** (например, DeepSeek) с теми же параметрами: та же модель, та же инструкция в `instructions`, при необходимости те же инструменты в `tools`. То есть вы «повторяете» настройки агента в коде.
- Если в агенте включён поиск по файлам или веб-поиск, в API нужно передать те же `tools` (см. [05-create-websearch-text-agent.md](learning/yandex-ai-studio/05-create-websearch-text-agent.md), [06-create-filesearch-text-agent.md](learning/yandex-ai-studio/06-create-filesearch-text-agent.md)).

---

## Устранение неполадок

### Ошибка 403: «Permission EXEC denied», «You need the ai.assistants.editor, editor, or admin role»

Означает: у учётной записи (или API-ключа), от имени которого идёт запрос, **нет нужной роли на каталог**.

**Что сделать:**

1. Откройте [консоль Yandex Cloud](https://console.yandex.cloud/) и выберите ваш **каталог** (тот, чей `folder_id` указан в `.env`).
2. Перейдите в **«Управление доступом»** (или **IAM** / **Права доступа** для каталога).
3. Найдите субъект, от которого создан API-ключ:
   - если ключ создавали в AI Studio от своего Яндекс ID — ищите свой аккаунт (email);
   - если ключ от сервисного аккаунта — ищите этот сервисный аккаунт.
4. Назначьте ему одну из ролей на **этот каталог**:
   - **ai.assistants.editor** — достаточно для вызова Responses API и агентов;
   - или **editor** / **admin** на каталог.
5. Сохраните изменения и подождите 1–2 минуты. После этого повторите запрос.

Дополнительно при создании API-ключа в AI Studio у ключа должна быть **область действия** `yc.ai.foundationModels.execute`. Если создаёте новый ключ — проверьте, что эта область выбрана.

### Ошибка «Invalid control character at: line … column …»

Возникает при разборе JSON. Частые причины:

1. **config/config.json** — в одной из строк есть перевод строки или табуляция внутри значения. В JSON строки должны быть в одну строку; переносы внутри значения нужно заменять на `\n`. Проверьте, что после каждого значения стоит запятая и закрывающая кавычка, например: `"folder_id": "ваш_id",` (с запятой в конце).
2. **Ответ API** — иногда ответ модели содержит символ, ломающий разбор. Попробуйте запрос ещё раз.

---

## Ссылки

- [Документация Yandex AI Studio — Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
- [Получить API-ключ](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/get-api-key.html)
- [Идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id)
- Локальные материалы: [docs/learning/yandex-ai-studio/README.md](learning/yandex-ai-studio/README.md)

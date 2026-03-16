# Работа с Vector Store API (поисковые индексы агента)

Просмотр списка индексов и файлов в индексе через API Yandex AI Studio (OpenAI-совместимый Vector Store API).

---

## Что нужно

- **API-ключ** и **folder_id** (как для [подключения к API](Подключение-к-API-Yandex-AI-Studio.md)).
- **Права:** роль с доступом к Vector Store (например `ai.assistants.editor` на каталог).
- **vector_store_id** — идентификатор поискового индекса. Его можно:
  - взять в веб-интерфейсе AI Studio (Agent Atelier → AI Search / поисковые индексы → выберите индекс → скопировать ID);
  - или получить списком через API (см. ниже).

---

## Конфиг и переменные окружения

В **config/config.json** в секции `yandex_ai_studio` добавьте (по желанию):

```json
"vector_store_id": "ваш_идентификатор_индекса"
```

Либо в **config/.env**:

```env
YANDEX_VECTOR_STORE_ID=ваш_идентификатор_индекса
```

Тогда команды ниже смогут использовать индекс по умолчанию без передачи ID в аргументах.

---

## Команды (CLI)

Из корня проекта с активированным `.venv`:

**Список всех поисковых индексов в каталоге:**

```bash
python -m src.vector_store_client
```

Вывод: id, name, status, file_counts по каждому индексу.

**Список файлов в конкретном индексе:**

```bash
python -m src.vector_store_client --files <vector_store_id>
```

или, если задан `vector_store_id` в конфиге:

```bash
python -m src.vector_store_client --files
```

Вывод: id, filename, status по каждому файлу в индексе.

---

## Использование в коде

```python
from src.vector_store_client import (
    list_vector_stores,
    list_vector_store_files,
    get_vector_store,
    print_vector_stores,
    print_vector_store_files,
)

# Список индексов
stores = list_vector_stores(limit=20)
for s in stores.data:
    print(s.id, s.name, getattr(s, "status", None))

# Список файлов в индексе
vector_store_id = "ваш_vector_store_id"
files = list_vector_store_files(vector_store_id, limit=50)
for f in files.data:
    print(f.id, f.filename, f.status)

# Информация об одном индексе
info = get_vector_store(vector_store_id)
print(info.name, info.file_counts)
```

---

## Ссылки

- [Vector stores API (Yandex)](https://aistudio.yandex.ru/docs/ru/ai-studio/vectorStores/index.html)
- [Управление поисковым индексом](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/manage-searchindex.html)
- В проекте: [06-create-filesearch-text-agent.md](learning/yandex-ai-studio/06-create-filesearch-text-agent.md) — использование индекса в запросах к модели (file_search).

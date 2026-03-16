# neuropulse-grant-agent

Агент для работы с грантами (NeuroPulse). Заготовка проекта с клиентом API и конфигурацией.

## Структура проекта

```
neuropulse-grant-agent/
├── src/               # исходный код
│   └── agent_api_client.py
├── config/            # конфигурация (API, промпты)
│   └── config.json
├── data/              # примеры данных, шаблоны отчётов
├── tests/             # тесты
├── docs/              # документация
│   └── learning/      # обучающие материалы (Yandex AI Studio и др.)
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Окружение

1. Создать виртуальное окружение и установить зависимости:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. Параметры API — в `config/config.json` или в `.env` (см. `.env.example`).

## Логирование

Параметры в `config/config.json` → секция `logging`:

- `level` — уровень (DEBUG, INFO, WARNING, ERROR)
- `log_file` — путь к файлу логов (например `logs/app.log`), опционально
- `format` — формат строки лога

Включение при старте приложения:

```python
from src.logging_config import setup_logging
setup_logging()  # читает config.json
```

Далее во всех модулях используйте `logging.getLogger(__name__)`; вывод идёт в stderr и при заданном `log_file` — в файл.

## Запуск

После настройки `base_url` и `api_key` в конфиге можно подключать клиент:

```python
from src.logging_config import setup_logging
from src.agent_api_client import AgentAPIClient, load_config

setup_logging()
client = AgentAPIClient()
if client.is_configured():
    # вызовы API
    pass
```

## Документация и обучение

- **Пошаговая настройка агента (без программирования)** — инструкция по созданию агента в веб-интерфейсе Yandex AI Studio для помощи по гранту губернатора и проекту «Нейропульс»: [docs/Инструкция-настройка-агента-грант-Нейропульс.md](docs/Инструкция-настройка-агента-грант-Нейропульс.md).
- **Подключение по API** — как получить API-ключ и Folder ID, настроить конфиг и отправить запрос к модели из Python: [docs/Подключение-к-API-Yandex-AI-Studio.md](docs/Подключение-к-API-Yandex-AI-Studio.md).
- **Vector Store API** — список индексов и файлов в индексе агента: [docs/Vector-Store-API.md](docs/Vector-Store-API.md).
- **План разработки агента по гранту** — веб-чат, быстрые действия, напоминания, аудит: [docs/План-разработки-агента-гранта.md](docs/План-разработки-агента-гранта.md).
- **Yandex AI Studio** — локальные копии статей по API и полная документация. См. [docs/learning/yandex-ai-studio/README.md](docs/learning/yandex-ai-studio/README.md).

## Репозиторий

- GitHub: https://github.com/kraskimira89-spec/neuropulse-grant-agent

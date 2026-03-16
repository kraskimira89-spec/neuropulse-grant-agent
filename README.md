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

## Запуск

После настройки `base_url` и `api_key` в конфиге можно подключать клиент:

```python
from src.agent_api_client import AgentAPIClient, load_config

client = AgentAPIClient()
if client.is_configured():
    # вызовы API
    pass
```

## Репозиторий

- GitHub: https://github.com/kraskimira89-spec/neuropulse-grant-agent

# Конфигурация

- **Секреты (API-ключи, пароли)** храните только в `.env` в корне проекта или в `config/.env`. См. `.env.example`.
- **YANDEX_API_KEY** и **YANDEX_FOLDER_ID** для Yandex AI Studio читаются только из переменных окружения, не из `config.json`.
- Если нет `config.json`, используется `config.example.json`. Чтобы задать свои настройки, скопируйте `config.example.json` в `config.json` (локально; `config.json` в .gitignore, в репозиторий не коммитится).
- Чтобы убрать `config.json` из репозитория (если он уже был закоммичен): `git rm --cached config/config.json`, затем коммит.

# Голосовой агент через Realtime API (WebSocket)

Источник: [Создать голосового агента через Realtime API](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-voice-agent.html)

**Realtime API** — событийно-ориентированный интерфейс для голосового взаимодействия по WebSocket. Модель `speech-realtime-250923`: распознавание речи (VAD), генерация ответа, синтез речи. Поддерживаются инструменты (функции, web_search, file_search).

---

## Схема работы

1. Микрофон → фрагменты аудио отправляются агенту (`input_audio_buffer.append`).
2. Сервер (VAD) возвращает распознанный текст в `conversation.item.input_audio_transcription.completed`.
3. Модель генерирует ответ: `response.output_text.delta` и `response.output_audio.delta`.
4. Клиент выводит текст и воспроизводит аудио. При новом запросе пользователя воспроизведение прерывается.

**Совет:** при отладке использовать наушники, чтобы агент не распознавал свой голос.

---

## Перед началом работы

- Роль сервисного аккаунта: `ai.models.user` на каталог.
- API-ключ для сервисного аккаунта.
- Python 3.10+, venv.
- Зависимости: `pip install numpy sounddevice aiohttp` (sounddevice ≥ 0.4.6, numpy ≥ 1.26.0, aiohttp ≥ 3.9.0).

---

## Подключение и настройка сессии

```python
import aiohttp

WS_URL = (
    f"wss://rest-assistant.api.cloud.yandex.net/v1/realtime/openai"
    f"?model=gpt://{YANDEX_CLOUD_FOLDER_ID}/speech-realtime-250923"
)
HEADERS = {"Authorization": f"api-key {YANDEX_CLOUD_API_KEY}"}

# Подключение
session = aiohttp.ClientSession()
ws = await session.ws_connect(WS_URL, headers=HEADERS, heartbeat=20.0)

# Настройка сессии: инструкции, аудио, инструменты
await ws.send_json({
    "type": "session.update",
    "session": {
        "instructions": "Ты вежливый русскоязычный ассистент. Отвечай кратко. ...",
        "output_modalities": ["audio"],  # или ["text"]
        "audio": {
            "input": {
                "format": {"type": "audio/pcm", "rate": 24000, "channels": 1},
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.5,
                    "silence_duration_ms": 400,
                },
            },
            "output": {
                "format": {"type": "audio/pcm", "rate": 44100},
                "voice": "dasha",  # голос озвучки
            },
        },
        "tools": [
            {"type": "function", "name": "get_weather", "description": "...", "parameters": {...}},
            {"type": "function", "name": "web_search", "description": "Поиск в интернете", "parameters": "{}"},
            {"type": "function", "name": "file_search", "description": VECTOR_STORE_ID, "parameters": "{}"},
        ],
    },
})
```

---

## Отправка и приём аудио

- **Uplink:** отправка фрагментов с микрофона в base64:
  `{"type": "input_audio_buffer.append", "audio": "<base64>"}`
- **Downlink — основные события:**
  - `conversation.item.input_audio_transcription.completed` — распознанный текст пользователя
  - `input_audio_buffer.speech_started` — пользователь начал говорить (прервать воспроизведение)
  - `response.created` — начало ответа агента
  - `response.output_text.delta` — текст ответа
  - `response.output_audio.delta` — аудио (base64), воспроизводить через PCM
  - `response.output_item.done` — завершён вызов функции; отправить `conversation.item.create` с `function_call_output` и затем `response.create`

---

## Вызов функции из голосового агента

При `response.output_item.done` с `item.type == "function_call"`:

1. Выполнить функцию локально (или через API).
2. Отправить результат:
   `{"type": "conversation.item.create", "item": {"type": "function_call_output", "call_id": "...", "output": "<json>"}}`
3. Запросить продолжение: `{"type": "response.create"}`

---

## Параметры из документации

- **VOICE** — голос озвучки (см. [голоса SpeechKit](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/ru/speechkit/tts/voices.html#premium)).
- **IN_RATE / OUT_RATE** — частоты дискретизации входа и выхода (в примере 24000 / 44100).
- **VECTOR_STORE_ID** — ID поискового индекса для file_search.
- Аудио: PCM, float32 → PCM16 для отправки; base64 по WebSocket.

Полный пример клиента (микрофон, воспроизведение, uplink/downlink) см. в оригинальной статье по ссылке выше.

# Документация Yandex AI Studio

> Полная документация, собранная с https://aistudio.yandex.ru/docs/ru/ai-studio/
> Дата сборки: 16 марта 2026

---

## Содержание


- [1. О сервисе](#раздел-1-о-сервисе)
- [2. Начало работы](#раздел-2-начало-работы)
- [3. Model Gallery](#раздел-3-model-gallery)
  - [3.1 Обзор AI-моделей](#3-1-обзор-ai-моделей)
  - [3.2 Модели базового инстанса](#3-2-модели-базового-инстанса)
  - [3.3 Модели выделенного инстанса](#3-3-модели-выделенного-инстанса)
  - [3.4 Пакетная обработка данных](#3-4-пакетная-обработка-данных)
  - [3.5 Вызов функций](#3-5-вызов-функций)
  - [3.6 Режим рассуждений](#3-6-режим-рассуждений)
  - [3.7 Форматирование ответов (Structured Output)](#3-7-форматирование-ответов)
  - [3.8 Классификаторы](#3-8-классификаторы)
  - [3.8.1 Модели классификаторов](#3-8-1-модели-классификаторов)
  - [3.9 Эмбеддинги](#3-9-эмбеддинги)
  - [3.10 Датасеты](#3-10-датасеты)
  - [3.11 Дообучение](#3-11-дообучение)
  - [3.12 Токены](#3-12-токены)
- [4. Agent Atelier](#раздел-4-agent-atelier)
  - [4.1 Обзор AI-агентов](#4-1-обзор-ai-агентов)
  - [4.2 Текстовые агенты](#4-2-текстовые-агенты)
  - [4.3 Голосовые агенты (Realtime API)](#4-3-голосовые-агенты)
  - [4.4 Управление контекстом диалога](#4-4-управление-контекстом)
  - [4.5 Code Interpreter](#4-5-code-interpreter)
- [5. AI Search](#раздел-5-ai-search)
  - [5.1 Обзор AI Search](#5-1-обзор-ai-search)
  - [5.2 Поисковые индексы Vector Store](#5-2-поисковые-индексы-vector-store)
  - [5.3 Инструмент поиска по файлам](#5-3-инструмент-поиска-по-файлам)
  - [5.4 Инструмент поиска в интернете](#5-4-инструмент-поиска-в-интернете)
- [6. MCP Hub](#раздел-6-mcp-hub)
  - [6.1 Обзор MCP Hub](#6-1-обзор-mcp-hub)
  - [6.2 Шаблоны MCP-серверов](#6-2-шаблоны-mcp-серверов)
- [7. API и интеграции](#раздел-7-api-и-интеграции)
  - [7.1 Особенности реализации API](#7-1-особенности-api)
  - [7.2 Аутентификация в API](#7-2-аутентификация)
  - [7.3 Заголовки для диагностики ошибок](#7-3-заголовки-диагностики)
  - [7.4 Пошаговые инструкции](#7-4-пошаговые-инструкции)
  - [7.5 Отключение логирования запросов](#7-5-отключение-логирования)
  - [7.6 Переход с AI Assistant API на Responses API](#7-6-переход-assistant-responses)
- [8. Yandex AI Studio SDK](#раздел-8-yandex-ai-studio-sdk)
  - [8.1 Обзор SDK](#8-1-обзор-sdk)
  - [8.2 Миграция с Yandex Cloud ML SDK](#8-2-миграция-sdk)
- [9. Безопасность](#раздел-9-безопасность)
  - [9.1 Управление доступом](#9-1-управление-доступом)
  - [9.2 Создание API-ключа](#9-2-создание-api-ключа)
  - [9.3 Модерация ответов](#9-3-модерация-ответов)
  - [9.4 Управление правилами модерации](#9-4-управление-правилами-модерации)
  - [9.5 Управление словарями правил модерации](#9-5-управление-словарями-модерации)
- [10. Квоты и лимиты](#раздел-10-квоты-и-лимиты)
- [11. Тарификация](#раздел-11-тарификация)
- [12. История изменений](#раздел-12-история-изменений)
- [13. Глоссарий](#раздел-13-глоссарий)
- [14. FAQ](#раздел-14-faq)
- [15. Устранение неполадок](#раздел-15-устранение-неполадок)
  - [15.1 Коды ошибок](#15-1-коды-ошибок)
- [Приложение: Публичные материалы](#приложение-публичные-материалы)

---


# 1. О сервисе

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html

Yandex AI Studio — это платформа Yandex Cloud для создания AI-приложений и AI-агентов на базе больших генеративных моделей. AI Studio предоставляет все необходимое для всех этапов от экспериментов и прототипирования до промышленного внедрения разработок.

## Модели и базовые возможности

В [Model Gallery](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html) доступен большой выбор моделей для генерации текста, голоса и изображений, [текстовой классификации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/index.html) и построения [эмбеддингов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html). С их помощью вы можете решать прикладные задачи: создавать и анализировать контент, классифицировать данные, строить поиск по документам или обрабатывать большие массивы однотипной информации.

## Использование моделей

Выберите интерфейс и модель для своих задач — в AI Studio есть все необходимое:
* [AI Playground](https://console.yandex.cloud/link/ml/ai-studio/playground) — для экспериментов, тестирования моделей и генерации изображений.
* [Agent Atelier](https://console.yandex.cloud/link/ml/ai-studio/agents) — для создания и управления агентами в интерфейсе AI Studio.
* OpenAI-совместимые API, OpenAI SDK и Yandex AI Studio SDK — для встраивания моделей в приложения.
* [Модели базового инстанса](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html) — для большинства бизнес-сценариев.
* [Выделенные инстансы](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/dedicated-instance.html) — для развертывания моделей, которых нет в базовом инстансе.
* [Пакетная обработка](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/batch-processing.html) — для асинхронной обработки информации.

## Разработка AI-приложений

Среда разработки [Agent Atelier](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/index.html) позволяет создавать решения на основе текстовых и голосовых AI-агентов с использованием готовых и настраиваемых [инструментов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/index.html#tools). А если готовых инструментов не хватает, вы всегда можете создать собственный MCP-сервер в MCP Hub, чтобы дать агенту возможность использовать любые внешние инструменты и API.

Для визуального проектирования в AI Studio доступен low-code-конструктор Yandex Workflows.

## API и интеграции

AI Studio предоставляет REST API, совместимые с OpenAI:
* Responses API — для создания текстовых агентов;
* Realtime API — для голосовых агентов;
* Files API и Vector Store API — для загрузки файлов и поиска по по ним.

OpenAI-совместимые API поддерживают интеграцию с популярными фреймворками LangChain и LangGraph.

Помимо этого AI Studio предлагает gRPC и REST API для отдельных задач генерации, анализа и обучения.

Подробнее про все доступные API — в разделе [Обзор API Yandex AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/api.html).

## Ограничения сервиса

Актуальные технические и организационные ограничения AI Studio приведены в разделе [Квоты и лимиты в Yandex AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html).

---

### Ссылки на другие страницы документации:
* [Документация AI Studio](https://aistudio.yandex.ru/docs/ru/index.html)
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
* [Публичные материалы](https://aistudio.yandex.ru/docs/ru/ai-studio/public-talks.html)
* [Термины и определения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html)
* [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)
* [Обзор](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html)
* [Обзор технологий SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/overview.html)
* [О сервисе Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/concepts/index.html)
* [О сервисе Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/concepts/ocr/index.html)
* [О сервисе Translate](https://aistudio.yandex.ru/docs/ru/translate/concepts/index.html)

---


# 2. Начало работы

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html

Платформа [Yandex AI Studio](https://aistudio.yandex.ru/) объединяет ИИ-сервисы и технологии Yandex Cloud для вашего бизнеса, чтобы вы могли создавать собственные ИИ-решения.

AI Studio предоставляет широкий выбор API и инструментов для решения любой задачи: OpenAI-совместимые API для создания текстовых и голосовых агентов, MCP-серверы и инструменты веб-поиска и поиска по файлам, а также специализированные API, разработанные в Яндексе.

В этом разделе вы создадите и настроите свой аккаунт, а затем отправите свой первый запрос к генеративной текстовой модели, доступной в Model Gallery.

## Подготовьте облако к работе

AI Studio использует [ресурсную модель](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy) Yandex Cloud: большинство сервисов хранит ресурсы в каталогах. Каталоги принадлежат облакам, а облака — организациям. Каталог потребуется и для работы с AI Studio.

1. [Войдите в AI Studio](https://aistudio.yandex.cloud/platform/), используя личный аккаунт на Яндексе (Яндекс ID). Подробную инструкцию, как создать такой аккаунт, смотрите в Справке [Яндекс ID](https://yandex.ru/support/passport/authorization/registration.html).
2. Создайте организацию:
    * Введите название организации.
    * Укажите название облака — оно будет использоваться для всех ресурсов Yandex Cloud.
    * Нажмите **Открыть AI Studio**.

В организации будет автоматически создан новый каталог с именем `default`.

## Привяжите платежный аккаунт

Для работы с AI Studio необходим активный [платежный аккаунт](https://yandex.cloud/ru/docs/billing/concepts/billing-account), привязанный к вашему облаку. При создании первого платежного аккаунта, привязанного к пользовательскому аккаунту, вам будет начислен [стартовый грант](https://yandex.cloud/ru/docs/getting-started/usage-grant).

1. После авторизации в AI Studio нажмите кнопку **Привязать платежный аккаунт** в правом верхнем углу интерфейса.
2. Создайте платежный аккаунт или выберите существующий.
    * Нажмите кнопку **Добавить карту**.
    * Укажите данные карты: 16-значный номер, срок действия, код CVV (с обратной стороны карты).
    * Нажмите кнопку **Привязать**.
3. Убедитесь, что платежный аккаунт имеет статус `ACTIVE` или `TRIAL_ACTIVE`.

## Создайте API-ключ

Чтобы создать API-ключ:

1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) нажмите **Создать API-ключ** в правом верхнем углу.
2. (Опционально) Измените описание API-ключа, чтобы вы легко могли найти его после.
3. Выберите срок действия API-ключа.
4. Нажмите кнопку **Создать**.
5. Сохраните идентификатор и секретный ключ.

> **Внимание**
> Не передавайте никому свой API-ключ. После закрытия диалога значение ключа будет недоступно.

## Настройте окружение

Установите необходимые пакеты и библиотеки:

### Python
Установите библиотеку OpenAI Python:
```bash
pip install --upgrade openai
```

Чтобы использовать [модели](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html) Model Gallery, задайте данные для аутентификации. Для этого вам понадобятся [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id) и секретное значение созданного API-ключа:
```python
import openai

FOLDER_ID='<идентификатор_каталога>'
API_KEY='<значение_API-ключа>'

client = openai.OpenAI(
    api_key=API_KEY,
    project=FOLDER_ID,
    base_url="https://ai.api.cloud.yandex.net/v1"
)
```

### Node.js
Установите библиотеку OpenAI Node.js:
```bash
npm install --save openai
# or
yarn add openai
```

Чтобы использовать модели Model Gallery, задайте данные для аутентификации:
```javascript
import OpenAI from "openai";

FOLDER_ID='<идентификатор_каталога>'
API_KEY='<значение_API-ключа>'

const openai = new OpenAI({
  apiKey: 'API_KEY',
  project: 'FOLDER_ID',
  baseURL: 'https://ai.api.cloud.yandex.net/v1'
});
```

### cURL
Установите [cURL](https://curl.haxx.se/).

Задайте переменные окружения:
```bash
export FOLDER_ID='<идентификатор_каталога>'
export API_KEY='<значение_API-ключа>'
```

## Отправьте запрос к модели

Отправьте запрос к модели. Для примера обратитесь к модели Alice AI LLM:

### Python
```python
YANDEX_CLOUD_MODEL = "aliceai-llm"

response = client.responses.create(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    input="Придумай 3 необычные идеи для стартапа в сфере путешествий.",
    temperature=0.8,
    max_output_tokens=1500
)

print(response.output[0].content[0].text)
```

### Node.js
```javascript
const response = await client.responses.create({
  model: "gpt://<идентификатор_каталога>/aliceai-llm",
  input: 'Придумай 3 необычные идеи для стартапа в сфере путешествий.'
});

console.log(response.output_text);
```

### cURL
```bash
curl \
  --request POST https://ai.api.cloud.yandex.net/v1/responses \
  --header "Authorization: Api-Key ${API_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "modelUri": "gpt://'${FOLDER_ID}'/aliceai-llm",
    "temperature": 0.8,
    "max_output_tokens": 1500,
    "input": "Придумай 3 необычные идеи для стартапа в сфере путешествий."
  }'
```

## Что дальше
* [Узнайте подробнее о сервисе](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)

---
**Ссылки на другие страницы документации:**
* [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
* [Тарифы](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing/)
* [Термины и определения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html)
* [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)
* [Получить API-ключ](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/get-api-key.html)
* [Квоты и лимиты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html)

---


# 3. Model Gallery


## 3.1 Обзор AI-моделей

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html

Yandex AI Studio предоставляет широкие возможности для работы с генеративными моделями для решения бизнес-задач:

* Собственные и опенсорс-модели в [базовом инстансе](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html#generation) с [оплатой](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html#rules-generating) за потребленные [токены](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html).
* [Дообучение](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html) моделей по методу LoRA.
* Готовые и дообучаемые модели [классификации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/index.html) текста.
* Большой выбор [текстовых](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html#text-batch) и [мультимодальных](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html#multimodels-batch) опенсорс-моделей для обработки больших объемов данных в пакетном режиме с [предоплаченным минимальным объемом токенов](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html#rules-generating).
* Выделенные инстансы моделей, если вам требуется обрабатывать большие объемы данных с гарантированным временем ответа.

Для работы с моделями доступны два интерфейса: AI Playground в интерфейсе AI Studio и различные API для [создания агентов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/index.html) и прямого обращения к моделям.

## Собственные модели Яндекса

В Model Gallery доступны разработанные в Яндексе модели генерации текста и изображений, которые вы можете использовать для бизнеса.

Самая маленькая и быстрая текстовая модель YandexGPT Lite отлично справляется с задачами, где важна скорость ответа и не требуются сложные рассуждения и глубокие познания в сложных предметных областях. Например, YandexGPT Lite можно использовать для классификации входящих сообщений пользователей, форматирования текста или суммаризации встреч.

YandexGPT Pro подойдет для решения более сложных задач: поиска по базам знаний и генерации результатов на основе найденной информации (RAG-сценарий), анализа документов, построения отчетов и аналитики, извлечения информации и автоматизации заполнения полей, форм и баз CRM.

Alice AI LLM — новая флагманская модель Яндекса — не только решает сложные задачи не хуже YandexGPT Pro, но и значительно лучше поддерживает диалог в чатовых сценариях, извлекая информацию из всего полученного контекста. Alice AI LLM отлично подойдет для создания «человеко-ориентированных» AI-ассистентов.

Текстовые модели Яндекса могут понимать около 20 языков, в том числе английский и японский, но предназначены в первую очередь для эффективной работы с текстами на русском языке. Собственный [токенизатор](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html) позволяет моделям Яндекса эффективнее потреблять токены по сравнению с другими доступными моделями, что экономит ваши средства. [Пример расчета стоимости](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html#example-generating) использования разных моделей для решения одной задачи доступен на [странице тарификации](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html#text-sync-async).

Кроме текстовых моделей в Model Gallery доступна модель YandexART — генеративная нейросеть, которая создает изображения по текстовому запросу. YandexART работает по методу каскадной диффузии, итеративно детализируя изображения из шума. Вы можете указать формат итогового изображения в параметре `mime_type`. На данный момент поддерживается значение `image/jpeg`. По умолчанию YandexART генерирует изображение размером 1024 х 1024 пикселя. Этот размер может увеличиваться или уменьшаться в зависимости от заданного соотношения сторон, но не более чем на 10%.

Текстовые модели Яндекса доступны через OpenAI-совместимые Completions API и Responses API, а также собственный API генерации текста в форматах [REST](https://aistudio.yandex.ru/docs/ru/ai-studio/text-generation/api-ref/index.html) и [gRPC](https://aistudio.yandex.ru/docs/ru/ai-studio/text-generation/api-ref/grpc/index.html).
YandexART предоставляет собственный API генерации изображений, также доступный в форматах [REST](https://aistudio.yandex.ru/docs/ru/ai-studio/image-generation/api-ref/index.html) и [gRPC](https://aistudio.yandex.ru/docs/ru/ai-studio/image-generation/api-ref/grpc/index.html).

Кроме того, все модели доступны через AI SDK и в [AI Playground](https://console.yandex.cloud/link/ai-studio/).

## Режимы работы с моделями AI Studio

Модели AI Studio имеют три режима взаимодействия: *синхронный*, *асинхронный* и *пакетный*. Режимы отличаются временем ответа и логикой работы.

В синхронном режиме модель получает ваш запрос и возвращает результат сразу после обработки. Задержка ответа в синхронном режиме минимальна, однако он не придет моментально: для работы модели требуется время, которое зависит от модели и от загруженности системы. При включенной опции `stream` модель в процессе присылает промежуточные варианты генерации. Синхронный режим подходит, если вам нужно поддерживать диалог [чат-бота](https://yandex.cloud/ru/docs/glossary/chat-bot). В синхронном режиме модели доступны в AI Playground, AI SDK, через API генерации текста, и OpenAI-совместимые API.

В асинхронном режиме в ответ на полученный запрос модель присылает [объект Operation](https://yandex.cloud/ru/docs/api-design-guide/concepts/operation), который содержит идентификатор выполняемой операции. По идентификатору вы можете узнать статус запроса и позже получить его результат, отправив запрос на специальный эндпоинт получения результата (его значение зависит от модели). Промежуточные результаты генерации недоступны в асинхронном режиме. Как правило, генерация результата в асинхронном режиме занимает больше времени (от пары минут до нескольких часов), чем в синхронном, но будет стоить дешевле. Асинхронный режим подходит, если ваши задачи не требуют срочного ответа. В асинхронном режиме некоторые модели доступны в AI SDK, через API генерации текста и API генерации изображений.

Пакетный режим работы (batch processing) позволяет обрабатывать большой массив данных за один запрос к модели. Входные данные передаются в виде [датасета](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/resources/dataset.html), тип датасета зависит от модели. Для каждого запроса сервис AI Studio запускает индивидуальный инстанс модели, который обрабатывает датасет, а после выключает его. Результат сохраняется в виде еще одного датасета, который вы можете скачать в формате [Parquet](https://parquet.apache.org/) или сразу же использовать, например, для дообучения другой модели. Генерация результата может занять несколько часов. Обработать данные в пакетном режиме можно в интерфейсе AI Studio, с помощью AI SDK и через Batch API. Список моделей, доступных в пакетном режиме, см. в разделе [Пакетная обработка данных](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/batch-processing.html).

## См. также

* [Режим рассуждений в генеративных моделях](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/chain-of-thought.html)
* [Отправить базовый запрос с помощью Responses API](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/create-prompt.html)
* [Отправить асинхронный запрос](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/async-request.html)

## 3.2 Модели базового инстанса

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html

Сервис Yandex AI Studio предоставляет доступ к большим генеративным моделям, разработанных разными компаниями. Если стандартных моделей вам недостаточно, вы можете [дообучить](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html) некоторые модели, чтобы они точнее отвечали на ваши запросы. Все роли, необходимые для работы с моделями, перечислены в разделе [Управление доступом в Yandex AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html).

В базовом инстансе ресурсы модели доступны всем пользователям Yandex Cloud и делятся между ними, поэтому при большой нагрузке время работы моделей может увеличиваться. При этом другие пользователи гарантированно не могут получить доступ к контексту ваших переписок с моделью: даже при включенном режиме логирования запросы хранятся в обезличенном виде, а потенциально чувствительная информация маскируется. Однако если вы обрабатываете конфиденциальную информацию с помощью моделей, рекомендуем [отключать](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/disable-logging.html) логирование данных.

Для моделей базового инстанса действуют правила обновления, описанные в разделе [Жизненный цикл модели](#model-lifecycle). При обновлении моделей поколения, доступные в разных ветках (сегменты `/latest`, `/rc` и `/deprecated`), могут меняться. Модифицированные модели делят [квоты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html#quotas) на использование со своими базовыми моделями.

### Список моделей

| Модель и URI | Контекст | Доступные API |
| :--- | :--- | :--- |
| **Alice AI LLM**<br>`gpt://<идентификатор_каталога>/aliceai-llm` | 32 768 | API генерации текста, OpenAI-совместимые API |
| **YandexGPT Pro 5.1**<br>`gpt://<идентификатор_каталога>/yandexgpt/rc` | 32 768 | API генерации текста, OpenAI-совместимые API |
| **YandexGPT Pro 5**<br>`gpt://<идентификатор_каталога>/yandexgpt/latest` | 32 768 | API генерации текста, OpenAI-совместимые API |
| **YandexGPT Lite 5**<br>`gpt://<идентификатор_каталога>/yandexgpt-lite` | 32 768 | API генерации текста, OpenAI-совместимые API |
| **DeepSeek V3.2**<br>`gpt://<идентификатор_каталога>/deepseek-v32/` | 131 072 | OpenAI-совместимые API |
| **Qwen3 235B**<br>`gpt://<идентификатор_каталога>/qwen3-235b-a22b-fp8/latest` | 262 144 | OpenAI-совместимые API |
| **gpt-oss-120b**<br>`gpt://<идентификатор_каталога>/gpt-oss-120b/latest` | 131 072 | OpenAI-совместимые API |
| **gpt-oss-20b**<br>`gpt://<идентификатор_каталога>/gpt-oss-20b/latest` | 131 072 | OpenAI-совместимые API |
| [**Дообученная YandexGPT Lite**](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html)<br>`gpt://<идентификатор_каталога>/yandexgpt-lite/latest@<суффикс>` | 32 768 | API генерации текста, OpenAI-совместимые API |
| **Gemma 3 27B**<br>`gpt://<идентификатор_каталога>/gemma-3-27b-it/latest`<br>[Условия использования Gemma](https://ai.google.dev/gemma/terms) | 131 072 | OpenAI-совместимые API |
| **YandexART**<br>`art://<идентификатор_каталога>/yandex-art/latest` | 500 символов | API генерации изображений |

Модель Gemma 3 27B работает с изображениями в кодировке Base64. Модель может обрабатывать изображения с любым соотношением сторон благодаря адаптивному алгоритму, который масштабирует изображения до 896 пикселей по большей стороне, сохраняя важные визуальные детали. Каждое изображение использует 256 [токенов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html) контекста.

## Жизненный цикл модели {#model-lifecycle}

Каждая модель имеет набор характеристик жизненного цикла: название модели, ветка и дата публикации. Эти характеристики позволяют однозначно определить версию модели. Обновление моделей происходит по определенным ниже правилам, чтобы вы могли адаптировать свои решения под новую версию, если это будет необходимо.

Существует три ветки модели (от более старой к новой): `Deprecated`, `Latest`, `Release Candidate` (`RC`). Для каждой из этих веток действует [SLA](https://yandex.cloud/ru/docs/overview/sla) сервиса.

Ветка `RC` обновляется по мере готовности новой модели и может измениться в любой момент. Когда модель в ветке `RC` будет готова к общему использованию, в [истории изменений](https://aistudio.yandex.ru/docs/ru/ai-studio/release-notes/index.html) и [сообществе пользователей](https://t.me/YFM_Community) в Telegram появится уведомление о предстоящем релизе.

Через месяц после объявления версия `RC` становится `Latest`, а `Latest` переносится в `Deprecated`. Поддержка версии `Deprecated` осуществляется в течение следующего месяца, после чего модели в ветках `Deprecated` и `Latest` будут идентичны.

## Примеры использования {#examples}

* [Отправить базовый запрос с помощью Responses API](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/create-prompt.html)
* [Отправить асинхронный запрос](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/async-request.html)
* [Сгенерировать изображение с помощью YandexART](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/yandexart-request.html)

---
### Ссылки на другие страницы документации:
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
* [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
* [Обзор поколения моделей](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html)
* [Модели выделенного инстанса](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/dedicated-instance.html)
* [Пакетная обработка данных](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/batch-processing.html)
* [Вызов функций](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/function-call.html)
* [Режим рассуждений](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/chain-of-thought.html)
* [Форматирование ответов моделей](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/structured-output.html)
* [Эмбеддинги](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html)
* [Датасеты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/resources/dataset.html)
* [Дообучение](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html)
* [Токены](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html)
* [Квоты и лимиты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html)
* [Тарифы](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html)
* [История изменений](https://aistudio.yandex.ru/docs/ru/ai-studio/release-notes/index.html)

## 3.3 Модели выделенного инстанса

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/dedicated-instance.html

> **Примечание**
> Функциональность находится на стадии [Preview](https://yandex.cloud/ru/docs/overview/concepts/launch-stages).

AI Studio позволяет развернуть некоторые модели на **выделенном инстансе**. В отличие от самостоятельного развертывания моделей на ВМ в сервисе Yandex Compute Cloud, вам не нужно настраивать окружение и подбирать оптимальные параметры ВМ — AI Studio обеспечивает стабильный, надежный и эффективный инференс модели и следит за его работой в автоматическом режиме.

Выделенные инстансы имеют ряд преимуществ:
* Гарантируемые параметры производительности, на которые не влияет трафик других пользователей.
* Отсутствие дополнительных квот на отправление запросов и параллельные генерации, ограничения зависят только от выбранной конфигурации инстанса.
* Оптимизированный инференс модели, чтобы обеспечить эффективное использование оборудования.

Выделенные инстансы будут полезны, если вам необходимо обрабатывать большие объемы запросов без задержек. [Тарификация](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html) выделенного инстанса не зависит от объема входящих и исходящих токенов: оплачиваться будет только время его работы.

## Модели выделенного инстанса

Все развернутые модели доступны через API, совместимый с OpenAI, AI SDK и в AI Playground. Чтобы развернуть выделенный инстанс, понадобится [роль](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html) `ai.models.editor` или выше на каталог. Для обращения к модели достаточно роли `ai.languageModels.user`.

| Модель | Контекст | Лицензия |
| --- | --- | --- |
| **Qwen 2.5 VL 32B Instruct**<br>[Карточка модели](https://huggingface.co/Qwen/Qwen2.5-VL-32B-Instruct) | 32 768 | Лицензия [Apache 2.0](https://choosealicense.com/licenses/apache-2.0/) |
| **Qwen 2.5 7B Instruct**<br>[Карточка модели](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 32 768 | Лицензия [Apache 2.0](https://choosealicense.com/licenses/apache-2.0/) |
| **Gemma 3 4B it**<br>[Карточка модели](https://huggingface.co/google/gemma-3-4b-it) | 131 072 | [Условия использования Gemma](https://ai.google.dev/gemma/terms) |
| **Gemma 3 12B it**<br>[Карточка модели](https://huggingface.co/google/gemma-3-12b-it) | 65 536 | [Условия использования Gemma](https://ai.google.dev/gemma/terms) |
| **T-pro-it-2.0-FP8**<br>[Карточка модели](https://huggingface.co/t-tech/T-pro-it-2.0-FP8) | 32 768 | Лицензия [Apache 2.0](https://choosealicense.com/licenses/apache-2.0/) |

## Конфигурации выделенных инстансов

Каждая модель может быть доступна для развертывания на нескольких конфигурациях: **S**, **M** или **L**. Каждая конфигурация гарантирует определенные значения TTFT (*Time to first token*, время до первого токена), *Latency* (задержка — время, затраченное на генерацию ответа) и TPS (*Tokens per second*, количество токенов в секунду) для запросов с разной длиной контекста.

Рисунок ниже показывает зависимость задержек и количества токенов, обрабатываемых моделью, от количества параллельных генераций (Concurrency на рисунке): до определенного момента чем больше генераций модель будет обрабатывать параллельно, тем дольше будет длиться генерация и тем больше токенов будет сгенерировано за секунду.

## Примеры использования

* [Создать инстанс](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-instance.html)
* [Клонировать инстанс](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/clone-instance.html)
* [Получить информацию об инстансе](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/get-instance.html)
* [Остановить и запустить инстанс](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/start-stop-instance.html)
* [Удалить инстанс](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/delete-instance.html)

---
### Ссылки на другие страницы документации

* [Обзор](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html)
* [Модели базового инстанса](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html)
* [Пакетная обработка данных](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/batch-processing.html)
* [Вызов функций](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/function-call.html)
* [Режим рассуждений](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/chain-of-thought.html)
* [Форматирование ответов моделей](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/structured-output.html)
* [Эмбеддинги](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html)
* [Датасеты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/resources/dataset.html)
* [Дообучение](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html)
* [Токены](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html)
* [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)

## 3.4 Пакетная обработка данных

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/batch-processing.html

В пакетном режиме доступны следующие модели генерации текста (размеры контекста от 8 192 до 131 072 токенов). Пакетный режим позволяет обрабатывать большой массив данных за один запрос к модели через датасеты.

## Мультимодальные модели

В пакетном режиме также доступны мультимодальные модели (размеры контекста от 4 096 до 16 384 токенов).

## 3.5 Вызов функций

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/function-call.html

Большинство приложений для работы с искусственным интеллектом взаимодействуют с человеком напрямую, но не могут обращаться к внешним базам данных, API и другим инструментам. Возможности моделей можно расширить с помощью **вызова функций** (Function Calling) — специального параметра, позволяющего описать доступные внешние инструменты и интерпретировать результаты их работы.

При вызове функции модель не генерирует текст самостоятельно, а только подставляет параметры для внешнего инструмента.

> Например, у вас есть функция получения прогноза погоды, которую вы предлагаете модели использовать. Тогда при генерации ответа на запрос «Какая погода в Санкт-Петербурге?» модель сможет инициировать вызов этой функции, получить текущий прогноз погоды и сгенерировать ответ, используя полученное значение. Подробный пример см. в [пошаговой инструкции](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/function-call.html).

Все дополнительные инструменты, которые могут быть доступны для модели, зависят от разработчика приложения. Сама по себе модель не выполняет функции и не взаимодействует с инструментами напрямую. Она лишь генерирует запрос для внешнего инструмента в виде структурированных данных, который необходим для выполнения задачи. Выполнение этой функции и передача ее результата обратно в модель осуществляется на стороне пользователя или сервиса, который управляет процессом. После получения результата модель использует его для генерации итогового ответа.

Вызовы функций могут быть полезны во многих случаях, например:

*   **Выполнение строгой логики** — калькулятор, интерпретация кода на ВМ.
*   **Поиск актуальной информации** — погода, курсы валют, отслеживание маршрутов.
*   **Обращение к внешним системам** — получение и запись данных в ERP, CRM, базы данных.
*   **Визуализация** — составление таблиц, графиков, отчетов.
*   **Удаленное управление устройством** — создание и удаление файлов, запуск скриптов и программ.
*   **Автоматизация** — проверка дедлайнов, назначение задач сотрудникам.

## Как вызывать функции в API генерации текста

При работе с моделями через API генерации текста вы можете описать все доступные модели функции в поле `tools`. Определение каждой функции в поле `tools` должно содержать название функции, описание ее назначения или поведения и список параметров, которые модель должна вернуть для корректного применения функции. Описание параметров передаются в виде [JSON Schema](https://json-schema.org/):

```json
request_body = {
    "messages": [
        { "role": "system", "text": "<текст_инструкции>" },
        { "role": "user", "text": "<текст_запроса>" }
    ],
    "tools": [ {
        "function": {
            "name": "weatherTool",
            "description": "Получает прогноз погоды в городе через API", # Старайтесь делать описание функции подробным
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string", # Тип параметра
                        "description": "Название города, для которого нужно получить погоду." # Описание параметра
                    },
                    "units": {
                        "type": "string",
                        "enum": ["metric", "imperial"], # Список допустимых значений
                        "default": "metric", # Значение по умолчанию
                        "description": "Единицы измерения температуры. 'metric' для Цельсия, 'imperial' для Фаренгейта."
                    },
                    "days": {
                        "type": "integer",
                        "default": 1,
                        "minimum": 1,
                        "maximum": 5, # Ограничения для параметров
                        "description": "Количество дней, для которых нужно получить погоду, начиная с текущего дня."
                    },
                    "regions": {
                        "type": "array", # Массивы
                        "default": ["center"],
                        "maxItems": 3,
                        "description": "Части города, для которых нужно получить погоду. Например: 'center', 'west', 'west-east' и т.д."
                    }
                },
                "required": ["city"] # Список обязательных параметров, без которых функция не сможет работать
            }
        }
    } ]
}
```

Вы также можете указать базовые типы данных, валидацию строк, чисел и массивов и другие параметры. Более подробное описание JSON Schema см. на [официальном сайте](https://json-schema.org/learn/getting-started-step-by-step).

Наличие поля `tools` в вызове функции не гарантирует, что модель обязательно вызовет какой-то из инструментов. Если исходя из контекста модель решит воспользоваться дополнительным инструментом, в ответ на запрос пользователя придет сообщение с [полем ToolCallList](https://aistudio.yandex.ru/docs/ru/ai-studio/text-generation/api-ref/TextGeneration/completion.html#yandex.cloud.ai.foundation_models.v1.ToolCallList2), содержащим обращение к вызываемой функции и необходимые параметры в виде JSON Schema. Результат работы функции отправьте в сообщении в [поле ToolResultList](https://aistudio.yandex.ru/docs/ru/ai-studio/text-generation/api-ref/TextGeneration/completion.html#yandex.cloud.ai.foundation_models.v1.ToolResultList). После этого модель сгенерирует итоговый ответ, используя результаты вызова функции.

Если же модель, основываясь на контексте запроса, решит не использовать предложенные инструменты, итоговый ответ будет сгенерирован сразу.

## Примеры использования

*   [Вызвать функцию из модели](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/function-call.html)

## 3.6 Режим рассуждений

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/chain-of-thought.html

Генеративные модели не всегда одинаково хорошо справляются с задачами, требующими рассуждений, то есть разбиения задачи на этапы и последовательного выполнения цепочки вычислений, при котором исходными данными для каждого последующего вычисления являются результаты предыдущего.

Точность ответов модели можно повысить, заставив модель рассуждать и выполнять генерацию с учетом таких цепочек промежуточных вычислений. Это можно сделать с помощью промпта или специального [параметра генерации](https://aistudio.yandex.ru/docs/ru/ai-studio/text-generation/api-ref/TextGeneration/completion.html#yandex.cloud.ai.foundation_models.v1.ReasoningOptions).

## Параметр reasoning_option {#reasoning-option}

Задать настройки режима рассуждений с помощью параметра `reasoning_options` можно при [обращении](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html#addressing-models) через API или SDK к тем моделям, которые этот параметр поддерживают. Параметр `reasoning_options` может принимать следующие значения:

* `DISABLED` — режим рассуждений выключен. Значение по умолчанию. Если параметр `reasoning_options` не задан в запросе, режим рассуждений выключен.
* `ENABLED_HIDDEN` — режим рассуждений включен. Разные модели по-разному принимают решение, использовать ли этот режим для каждого конкретного запроса. Даже если при генерации ответа модель использует рассуждения, ответ не будет содержать непосредственно саму цепочку рассуждений модели.

Пример конфигурации запроса в режиме рассуждений:

### SDK
```python
model = sdk.models.completions('yandexgpt')
modelRequest = model.configure(
        reasoning_mode='enabled_hidden',
    ).run("Текст запроса")
```

### API
```json
{
  "modelUri": "gpt://<идентификатор_каталога>/yandexgpt",
  "completionOptions": {
    "stream": false,
    "temperature": 0.1,
    "maxTokens": "1000",
    "reasoningOptions": {
      "mode": "ENABLED_HIDDEN"
    }
  },
  "messages": [...]
}
```

При использовании моделью режима рассуждений может увеличиться объем выполняемых вычислений и общее количество итоговых [токенов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html) запроса: если рассуждения были использованы, ответ модели будет содержать поле `reasoningTokens` с ненулевым значением.

Режим рассуждений с помощью параметра `reasoning_options` доступен для модели YandexGPT Pro.

## Параметр reasoning_effort {#reasoning-effort}

Параметр `reasoning_effort` определяет, сколько токенов рассуждения модель должна сгенерировать перед тем, как сформировать ответ на запрос.

Поддерживаются значения:

* `low` — приоритет по скорости и экономии токенов.
* `medium` — баланс между скоростью и точностью рассуждений.
* `high` — приоритет более полного и тщательного рассуждения.

Пример использования параметра `reasoning_effort`:

### Python
```python
# Установите OpenAI SDK с помощью pip
# pip install openai

import openai
from openai import OpenAI

YANDEX_CLOUD_FOLDER = "<идентификатор_каталога>"
YANDEX_CLOUD_API_KEY = "<значение_API-ключа>"

def run():
    client = OpenAI(
        api_key=YANDEX_CLOUD_API_KEY,
        base_url="https://ai.api.cloud.yandex.net/v1",
        project=YANDEX_CLOUD_FOLDER
    )

    response = client.chat.completions.create(
        model=f"gpt://{YANDEX_CLOUD_FOLDER}/gpt-oss-120b",
        # или
        # model=f"gpt://{YANDEX_CLOUD_FOLDER}/gpt-oss-20b",
        messages=[
            {
                "role": "developer",
                "content": "Ты очень умный ассистент."
            },
            {
                "role": "user",
                "content": "Что под капотом LLM?"
            },
        ],
        reasoning_effort="low",
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    run()
```

---
**См. также:**
* [Вызов функций](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/function-call.html) (Предыдущая страница)
* [Форматирование ответов моделей](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/structured-output.html) (Следующая страница)
* [Документация AI Studio](https://aistudio.yandex.ru/docs/ru/index.html)

## 3.7 Форматирование ответов (Structured Output)

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/structured-output.html

По умолчанию модель возвращает ответ, отформатированный с помощью разметки [Markdown](https://ru.wikipedia.org/wiki/Markdown). Используйте текст промпта, чтобы получить ответ с дополнительным форматированием (например с [эмодзи](https://ru.wikipedia.org/wiki/%D0%AD%D0%BC%D0%BE%D0%B4%D0%B7%D0%B8)) или в другом формате ([JSON](https://ru.wikipedia.org/wiki/JSON), [XML](https://ru.wikipedia.org/wiki/XML) и т.п.)

### Пример

**Запрос:**
```json
{
  "modelUri": "gpt://<идентификатор_каталога>/yandexgpt/latest",
  "completionOptions": {
    "stream": false,
    "temperature": 0.6,
    "maxTokens": "2000",
    "reasoningOptions": {
      "mode": "DISABLED"
    }
  },
  "messages": [
    {
      "role": "system",
      "text": "Ты — умный ассистент."
    },
    {
      "role": "user",
      "text": "Назови любые три группы товаров в продовольственном магазине. Для каждой группы приведи три любые подгруппы, входящие в группу. Представь результат в формате JSON."
    }
  ]
}
```

**Результат:**
```json
{
  "result": {
    "alternatives": [
      {
        "message": {
          "role": "assistant",
          "text": "{\n  \"milk_products\": [\n    \"milk\",\n    \"cheese\",\n    \"yogurt\"\n  ],\n  \"bakery\": [\n    \"bread\",\n    \"buns\",\n    \"cakes\"\n  ],\n  \"fruits_and_vegetables\": [\n    \"apples\",\n    \"potatoes\",\n    \"carrots\"\n  ]\n}"
        },
        "status": "ALTERNATIVE_STATUS_FINAL"
      }
    ],
    "usage": {
      "inputTextTokens": "87",
      "completionTokens": "58",
      "totalTokens": "145"
    },
    "modelVersion": "07.03.2024"
  }
}
```

Модель вернула ответ в формате JSON, где перенос строки заменен на `\n`, а кавычки экранированы.

Если с помощью промпта вам не удается добиться желаемого результата, попробуйте [дообучить](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html) модель.

## Параметры API для сохранения структуры ответа

Некоторые модели генерации текста поддерживают дополнительное управление форматом ответа не только с помощью параметров запроса. Так вы можете использовать параметры форматирования ответа, чтобы указать, что ответ необходимо вернуть в формате JSON. На выбор доступны два варианта:

### 1. JSON с произвольной структурой

Чтобы получить ответ в формате JSON с произвольной структурой, укажите в объекте конфигурации модели `model.configure(response_format="json")`.

**Пример (SDK):**
```python
#!/usr/bin/env python3
from __future__ import annotations
import json
import pydantic
from yandex_ai_studio_sdk import AIStudio

def main() -> None:
    sdk = AIStudio(
        folder_id="<идентификатор_каталога>",
        auth="<API-ключ>",
    )

    model = sdk.models.completions("yandexgpt", model_version="rc")
    model = model.configure(response_format="json")

    text = """
    Назови любые три группы товаров в продовольственном магазине.
    Для каждой группы приведи три любые подгруппы, входящие в группу.
    Представь результат в формате JSON.
    """

    result = model.run(
        [
            {"role": "user", "text": text},
        ]
    )
    print("JSON result:", result[0].text)

if __name__ == "__main__":
    main()
```

> **Совет**
> Если вы хотите получить ответ в виде JSON с произвольной структурой, обязательно дополнительно укажите это словами в промпте. Иначе модель может добавлять дополнительные скобки, пробелы и отступы и генерировать лишние токены.

### 2. JSON, строго соответствующий заданной схеме

Для получения ответа, строго соответствующего схеме, используйте параметр `json_schema` в конфигурации.

**Пример (SDK):**
```python
#!/usr/bin/env python3
from __future__ import annotations
import json
import pydantic
from yandex_ai_studio_sdk import AIStudio

def main() -> None:
    sdk = AIStudio(
        folder_id="<идентификатор_каталога>",
        auth="<API-ключ>",
    )

    text = "Назови дату первого полета Гагарина."

    model = sdk.models.completions("yandexgpt", model_version="rc")
    model = model.configure(
        response_format={
            "json_schema": {
                "properties": {
                    "day": {
                        "title": "Day",
                        "description": "День месяца",
                        "type": "integer",
                    },
                    "month": {
                        "title": "Month",
                        "description": "Месяц, словом",
                        "type": "string",
                    },
                    "year": {
                        "title": "Year",
                        "description": "Год",
                        "type": "integer",
                    },
                },
                "required": ["day", "month", "year"],
                "type": "object",
            }
        }
    )

    result = model.run(
        [
            {"role": "user", "text": text},
        ]
    )
    print("JSON result:", result[0].text)

if __name__ == "__main__":
    main()
```

Строгая структура ответа необходима при работе с внешними инструментами с помощью [вызова функций](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/function-call.html).

---
**Ссылки на другие страницы документации:**
* [Документация AI Studio](https://aistudio.yandex.ru/docs/ru/index.html)
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
* [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
* [Обзор (Model Gallery)](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html)
* [Модели базового инстанса](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html)
* [Модели выделенного инстанса](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/dedicated-instance.html)
* [Пакетная обработка данных](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/batch-processing.html)
* [Вызов функций](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/function-call.html)
* [Режим рассуждений](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/chain-of-thought.html)
* [Эмбеддинги](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html)
* [Датасеты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/resources/dataset.html)
* [Дообучение](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html)
* [Токены](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html)
* [Публичные материалы](https://aistudio.yandex.ru/docs/ru/ai-studio/public-talks.html)
* [Термины и определения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html)
* [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)
* [Получить API-ключ](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/get-api-key.html)
* [Отключить логирование запросов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/disable-logging.html)
* [Тарифы AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html)

## 3.8 Классификаторы

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/index.html

Yandex AI Studio позволяет классифицировать передаваемые в промптах текстовые запросы. Классификация в [моделях](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/models.html) на базе YandexGPT реализована в [AI Studio Text Classification API](https://aistudio.yandex.ru/docs/ru/ai-studio/text-classification/api-ref/index.html).

В AI Studio доступна классификация трех типов:
* **Бинарная классификация** относит запрос к одному из двух возможных классов. Например, [спам](https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B0%D0%BC) или не спам.
* **Многоклассовая классификация** относит запрос к одному (и только к одному) из более чем двух классов. Например, центральный процессор компьютера может относиться только к одному поколению.
* **Классификация с несколькими метками** позволяет относить запрос одновременно к нескольким разным классам, которые не являются взаимоисключающими. Например, к одному и тому же посту в социальной сети может относиться одновременно несколько [хештегов](https://ru.wikipedia.org/wiki/%D0%A5%D0%B5%D1%88%D1%82%D0%B5%D0%B3).

Модели классификации доступны только в [синхронном режиме](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html#working-mode).

Сервис AI Studio предоставляет классификаторы двух видов:
* [по промпту](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/index.html#readymade) на базе YandexGPT Lite и YandexGPT Pro — доступны бинарная и многоклассовая классификации;
* [дообучаемые](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/index.html#trainable) классификаторы на базе YandexGPT Lite — доступны все поддерживаемые виды классификации.

Чтобы использовать модели классификаторов Yandex AI Studio, необходима [роль](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html#languageModels-user) `ai.languageModels.user` или выше на [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder).

## Классификаторы по промпту {#readymade}

Классификаторы по промпту AI Studio позволяют выполнять бинарную и многоклассовую классификацию, не требуют дообучения модели и управляются промптом. Метод [fewShotClassify](https://aistudio.yandex.ru/docs/ru/ai-studio/text-classification/api-ref/TextClassification/fewShotClassify.html) Text Classification API позволяет [использовать](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/readymade.html) два классификатора по промпту: Zero-shot и Few-shot. В метод `fewShotClassify` можно передать от двух до двадцати классов.

> **Совет**
> Задавайте осмысленные названия для классов `labels`: это обязательное условие получения корректных результатов классификации. Например: вместо классов `хм` и `фз` используйте классы `химия` и `физика`.

### Классификатор Zero-shot {#zero-shot}

Классификатор Zero-shot позволяет выполнять бинарную и многоклассовую классификацию, передавая в теле запроса только [идентификатор модели](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/models.html), описание задания, текст запроса и массив с именами классов.

Формат тела запроса для классификатора Zero-shot:

```json
{
  "modelUri": "string",
  "taskDescription": "string",
  "labels": [
    "string",
    "string",
    ...
    "string"
  ],
  "text": "string"
}
```

Где:
* `modelUri` — [идентификатор модели](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/models.html), которая будет использоваться для классификации сообщения. Параметр содержит [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id) Yandex Cloud.
* `taskDescription` — текстовое описание задания для классификатора.
* `labels` — массив классов.
* `text` — текстовое содержимое сообщения.

Для [запросов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/readymade.html) к классификаторам Zero-shot используйте эндпоинт `https://ai.api.cloud.yandex.net/foundationModels/v1/fewShotTextClassification`.

### Классификатор Few-shot {#few-shot}

Классификатор Few-shot позволяет выполнять бинарную и многоклассовую классификацию, передавая в модель несколько примеров классификации. Примеры запросов передаются в поле `samples` тела запроса и позволяют улучшить качество результатов, выдаваемых классификатором.

Формат тела запроса для классификатора Few-shot:

```json
{
  "modelUri": "string",
  "taskDescription": "string",
  "labels": [
    "string",
    "string",
    ...
    "string"
  ],
  "text": "string",
  "samples": [
    {
      "text": "string",
      "label": "string"
    },
    {
      "text": "string",
      "label": "string"
    },
    ...
    {
      "text": "string",
      "label": "string"
    }
  ]
}
```

Где:
* `modelUri` — [идентификатор модели](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/models.html), которая будет использоваться для классификации сообщения. Параметр содержит [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id) Yandex Cloud.
* `taskDescription` — текстовое описание задания для классификатора.
* `labels` — массив классов.
* `text` — текстовое содержимое сообщения.
* `samples` — массив с примерами запросов для классов, заданных в поле `labels`. Примеры запросов передаются в виде объектов, каждый из которых содержит один образец текстового запроса и имя класса, которому такой запрос следует относить.

Для [запросов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/readymade.html) к классификаторам Few-shot используйте эндпоинт `https://ai.api.cloud.yandex.net/foundationModels/v1/fewShotTextClassification`.

> **Важно**
> Вы можете передавать несколько примеров классификации в одном запросе. Все примеры в запросе не должны превышать 6000 токенов.

## Дообучаемые классификаторы {#trainable}

Если качество результатов классификаторов [Zero-shot](#zero-shot) и [Few-shot](#few-shot) вас не устраивает или вам нужна многоклассовая классификация, [дообучите собственный классификатор](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/tune-classifiers.html) на базе YandexGPT Lite. Дообучаемые классификаторы могут быть обучены всем поддерживаемым типам классификации.

Чтобы [выполнить](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/additionally-trained.html) запрос к дообученному классификатору, используйте метод [classify](https://aistudio.yandex.ru/docs/ru/ai-studio/text-classification/api-ref/TextClassification/classify.html) Text Classification API. В этом случае в модель требуется передать только [идентификатор модели](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/models.html) и текст запроса. Имена классов, по которым модель будет распределять запросы, должны быть заданы в процессе дообучения модели и в запросе не передаются.

Формат тела запроса для дообученного классификатора:

```json
{
  "modelUri": "string",
  "text": "string"
}
```

Где:
* `modelUri` — [идентификатор модели](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/models.html), которая будет использоваться для классификации сообщения. Параметр содержит [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id) Yandex Cloud и идентификатор дообученного классификатора.
* `text` — текстовое содержимое сообщения. Суммарное количество токенов на один запрос не должно превышать 8000.

Для [запросов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/additionally-trained.html) к дообучаемым классификаторам используйте эндпоинт `https://ai.api.cloud.yandex.net:443/foundationModels/v1/textClassification`.

Имена классов, по которым модель будет распределять запросы, должны быть заданы в процессе дообучения модели и в запросе не передаются.

## Формат ответа {#response}

Все типы классификаторов AI Studio возвращают результат в следующем формате:

```json
{
  "predictions": [
    {
      "label": "string",
      "confidence": "number"
    },
    {
      "label": "string",
      "confidence": "number"
    },
    ...
    {
      "label": "string",
      "confidence": "number"
    }
  ],
  "modelVersion": "string"
}
```

Где:
* `label` — имя класса.
* `confidence` — значение вероятности отнесения текста запроса к данному классу.

При многоклассовой классификации сумма значений полей вероятности (`confidence`) для всех классов всегда равна 1.
При классификации с несколькими метками значение поля вероятности (`confidence`) для каждого класса рассчитывается независимо (сумма значений не равна 1).

## Примеры использования {#examples}

* [Использовать дообученные классификаторы на базе YandexGPT](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/additionally-trained.html)
* [Использовать классификаторы по промпту на базе YandexGPT](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/readymade.html)

## 3.8.1 Модели классификаторов

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/models.html

Сервис Yandex AI Studio предоставляет доступ к моделям классификаторов на базе YandexGPT Lite и YandexGPT Pro, которые позволяют [классифицировать](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/index.html) передаваемые в промптах текстовые запросы. Классификация реализована в [AI Studio Text Classification API](https://aistudio.yandex.ru/docs/ru/ai-studio/text-classification/api-ref/index.html).

Если стандартных моделей вам недостаточно, вы можете [дообучить](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/tune-classifiers.html) классификатор на базе YandexGPT Lite, чтобы модель точнее классифицировала ваши запросы. Чтобы обратиться к дообученной модели классификатора, используйте метод [classify](https://aistudio.yandex.ru/docs/ru/ai-studio/text-classification/api-ref/TextClassification/classify.html) Text Classification API.

| Модель | URI | [Режимы работы](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html#working-mode) |
| --- | --- | --- |
| Классификатор по промпту на базе YandexGPT Lite | `cls://<идентификатор_каталога>/yandexgpt-lite/latest` | Синхронный |
| Классификатор по промпту на базе YandexGPT Pro | `cls://<идентификатор_каталога>/yandexgpt/latest` | Синхронный |
| Дообученный классификатор | `cls://<URI_базовой_модели>/<версия>@<суффикс_дообучения>` | Синхронный |

## Обращение к моделям

Вы можете обращаться к моделям классификаторов несколькими способами.

### SDK
При работе с моделями классификаторов через [Yandex AI Studio SDK](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk/index.html) используйте один из следующих форматов:

* **Название модели**, передается в виде строки.
  ```python
  model = (
    sdk.models.text_classifiers("yandexgpt-lite")
  )
  ```
* **Название и версия модели**, передаются в виде строк в полях `model_name` и `model_version` соответственно.
  ```python
  model = (
    sdk.models.text_classifiers(model_name="yandexgpt", model_version="latest")
  )
  ```
* **URI модели**, передается в виде строки, содержащей полный URI модели. Также используйте этот способ для обращения к дообученным моделям.
  ```python
  model = (
    sdk.models.text_classifiers("cls://b1gt6g8ht345********/yandexgpt/latest")
  )
  ```

### API
Чтобы [обратиться](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/readymade.html) к модели через [REST API](https://aistudio.yandex.ru/docs/ru/ai-studio/text-classification/api-ref/TextClassification/fewShotClassify.html) или [gRPC API](https://aistudio.yandex.ru/docs/ru/ai-studio/text-classification/api-ref/grpc/TextClassification/fewShotClassify.html), в поле `modelUri` тела запроса укажите URI модели, содержащий [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id). Сегмент `/latest` указывает на версию модели и является необязательным. Чтобы обратиться к модели классификатора на базе YandexGPT, используйте метод/вызов `fewShotClassify` Text Classification API.

**Пример:**
```json
{
  "modelUri": "cls://b1gt6g8ht345********/yandexgpt-lite/latest"
  ...
}
```

Для обращения к `latest` версии необязательно задавать версию модели явно, поскольку версия `latest` используется по умолчанию.

## См. также
* [Использовать классификаторы по промпту на базе YandexGPT](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/readymade.html)
* [Использовать дообученные классификаторы на базе YandexGPT](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/additionally-trained.html)
* [Поддерживаемые виды классификации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/index.html)
* [Эмбеддинги](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html)

## 3.9 Эмбеддинги

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html

Компьютеры обрабатывают любую информацию в виде чисел. Чтобы эффективно работать с текстами на естественных языках, модели искусственного интеллекта преобразовывают слова, фразы и предложения в числовые векторы фиксированного размера, которые сохраняют характеристики слов и связи между ними.

Процесс преобразования текста в такие векторы называется *векторизацией*, а результирующий вектор — *эмбеддингом*. Эмбеддинги хранят информацию о тексте и позволяют применять математические методы для обработки текстов. Так, с помощью эмбеддингов можно классифицировать информацию, сравнивать и сопоставлять тексты или организовать поиск по собственной базе знаний.

Если базовая модель эмбеддингов вам не подходит, вы можете [дообучить](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html) ее.

## Модели векторного представления текста

Сервис Yandex AI Studio предоставляет две модели векторизации текста.

| Назначение | URI | Размерность выходного вектора | [Режимы работы](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html#working-mode) |
| :--- | :--- | :--- | :--- |
| Векторизация больших текстов исходных данных, например статей документации. | `emb://<идентификатор_каталога>/text-search-doc/latest` | 256 | Синхронный |
| Векторизация коротких текстов: поисковых запросов, обращений и т. п. | `emb://<идентификатор_каталога>/text-search-query/latest` | 256 | Синхронный |
| Дообученные модели эмбеддингов | `gpt://<идентификатор_каталога>/text-embeddings/<версия>@<суффикс_дообучения>` | Зависит от параметров дообучения. По умолчанию — 256 | Синхронный |

Чтобы использовать модели векторного представления текста Yandex AI Studio, необходима [роль](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html#languageModels-user) `ai.languageModels.user` или выше на [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder).

## Обращение к моделям

Вы можете обращаться к моделям векторного представления текста несколькими способами.

### SDK
При работе с моделями векторного представления текста через [Yandex AI Studio SDK](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk/index.html) используйте один из следующих форматов:

* **Название модели**, передается в виде строки.
    ```python
    model = (
      sdk.models.text_embeddings("text-search-doc")
    )
    ```
* **Название и версия модели**, передаются в виде строк в полях `model_name` и `model_version` соответственно.
    ```python
    model = (
      sdk.models.text_embeddings(model_name="text-search-query", model_version="latest")
    )
    ```
* **URI модели**, передается в виде строки, содержащей полный [URI](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html#yandexgpt-embeddings) модели.
    ```python
    model = (
      sdk.models.text_embeddings("emb://b1gt6g8ht345********/text-search-query/latest")
    )
    ```

### API
Чтобы [обратиться](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/embeddings/search.html) к модели через [REST API](https://aistudio.yandex.ru/docs/ru/ai-studio/embeddings/api-ref/index.html) или [gRPC API](https://aistudio.yandex.ru/docs/ru/ai-studio/embeddings/api-ref/grpc/index.html), в поле `modelUri` тела запроса укажите [URI](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html#yandexgpt-embeddings) модели, содержащий [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id). Сегмент `/latest` указывает на версию модели и является необязательным.

Пример:
```json
{
  "modelUri": "emb://b1gt6g8ht345********/text-search-doc/latest",
  ...
}
```
Для обращения к `latest` версии необязательно задавать версию модели явно, поскольку версия `latest` используется по умолчанию.

## Пример использования эмбеддингов

Примитивный пример показывает, как с помощью эмбеддингов можно найти наиболее близкий ответ на вопрос по базе знаний. В массиве `doc_texts` собраны исходные данные для векторизации (база знаний), переменная `query_text` содержит поисковый запрос. После получения эмбеддингов можно вычислить расстояние между каждым вектором в базе знаний и вектором запроса и найти наиболее близкий текст.

### SDK (Python)
```python
#!/usr/bin/env python3
# pylint: disable=import-outside-toplevel

from __future__ import annotations
from yandex_ai_studio_sdk import AIStudio

doc_texts = [
    """Александр Сергеевич Пушкин (26 мая [6 июня] 1799, Москва — 29 января [10 февраля] 1837, Санкт-Петербург)
    — русский поэт, драматург и прозаик, заложивший основы русского реалистического направления,
    литературный критик и теоретик литературы, историк, публицист, журналист.""",
    """Ромашка — род однолетних цветковых растений семейства астровые,
    или сложноцветные, по современной классификации объединяет около 70 видов невысоких пахучих трав,
    цветущих с первого года жизни.""",
]
query_text = "когда день рождения Пушкина?"

def main():
    import numpy as np
    from scipy.spatial.distance import cdist

    sdk = AIStudio(
        folder_id="<идентификатор_каталога>",
        auth="<API-ключ>",
    )

    # Создаем эмбеддинг запроса
    query_model = sdk.models.text_embeddings("query")
    query_embedding = query_model.run(query_text)

    # Создаем эмбеддинг текстов
    doc_model = sdk.models.text_embeddings("doc")
    doc_embeddings = [doc_model.run(text) for text in doc_texts]

    query_embedding = np.array(query_embedding)

    # Вычисляем косинусные расстояния и находим ближайшие вектора
    dist = cdist([query_embedding], doc_embeddings, metric="cosine")
    sim = 1 - dist
    result = doc_texts[np.argmax(sim)]
    print(result)

if __name__ == "__main__":
    main()
```
Где:
* `<идентификатор_каталога>` — идентификатор [каталога](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder), в котором создан [сервисный аккаунт](https://yandex.cloud/ru/docs/iam/concepts/users/service-accounts).
* `<API-ключ>` — [API-ключ](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key) сервисного аккаунта для [аутентификации в API](https://aistudio.yandex.ru/docs/ru/ai-studio/api-ref/authentication.html).

**Результат:**
```text
Александр Сергеевич Пушкин (26 мая [6 июня] 1799, Москва — 29 января [10 февраля] 1837, Санкт-Петербург)
  — русский поэт, драматург и прозаик, заложивший основы русского реалистического направления,
  литературный критик и теоретик литературы, историк, публицист, журналист.
```

## Примеры использования
* [Использовать эмбеддинги в поиске по базе знаний](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/embeddings/search.html)
* [Дообучить модель эмбеддингов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/create-embeddings.html)

## Читайте также
* Примеры работы с AI SDK на [GitHub](https://github.com/yandex-cloud/yandex-ai-studio-sdk/tree/master/examples/sync/text_embeddings)
* [Дообучение моделей](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html)

## 3.10 Датасеты

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/resources/dataset.html

Датасеты в [Yandex AI Studio](https://aistudio.yandex.ru/) хранят наборы данных для [дообучения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html) и запуска моделей в пакетном режиме работы. Датасеты можно [создавать](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-dataset.html) в [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/), через API и [Yandex AI Studio SDK](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk/index.html).

Все датасеты создаются на основе файлов в формате [JSON Lines](https://jsonlines.org/) в кодировке [UTF-8](https://ru.wikipedia.org/wiki/UTF-8). Структура содержимого датасета зависит от его типа. Вы можете создать датасеты следующих типов:
*   Генерация текста — `TextToTextGenerationRequest` и `TextToTextGeneration`.
*   Классификация с несколькими метками и бинарная классификация — `TextClassificationMultilabel`.
*   Многоклассовая классификация — `TextClassificationMulticlass`.
*   Пары для дообучения эмбеддингов — `TextEmbeddingPairParams`.
*   Триплеты для дообучения эмбеддингов — `TextEmbeddingTripletParams`.
*   Визуально-текстовые датасеты — `ImageTextToTextGenerationRequest` и `ImageTextToTextGeneration`.

Актуальный список доступных типов датасетов вы можете получить, выполнив запрос:

```bash
grpcurl \
  -H "Authorization: Bearer <IAM-токен>" \
  ai.api.cloud.yandex.net:443 yandex.cloud.ai.dataset.v1.DatasetService.ListTypes
```

## Датасеты для генерации текста

AI Studio позволяет создать два типа датасетов для генерации текста.

### Запросы для генерации текста

Датасеты, содержащие только тексты запросов, подойдут для запуска моделей генерации текста в [пакетном режиме](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html#working-mode). Каждая строка содержит отдельный запрос, инициирующий генерацию текста, в формате JSON. В запросе может содержаться как только одно сообщение с ролью `user`, так и диалог с ролями `user` и `assistant`, а также (опционально) инструкция для модели:

```json
{"request": [{"role": "user", "text": "<Вопрос>"}]}
{"request": [{"role": "system", "text": "<инструкция>"}, {"role": "user", "text": "<Вопрос>"}]}
{"request": [{"role": "system", "text": "<инструкция>"}, {"role": "user", "text": "<Вопрос>"}, {"role": "assistant", "text": "<Реплика_1>"}, {"role": "user", "text": "<Реплика_2>"}, {"role": "assistant", "text": "<Реплика_3>"}]}
```

### Запросы и ответы генерации текста

Датасеты с вопросами и ответами используются для дообучения моделей. Также в этом формате возвращается ответ при обращении к моделям в пакетном режиме. Каждая строка содержит отдельный пример в формате JSON:

```json
{"request": [{"role": "user", "text": "<Вопрос>"}], "response": "<Ответ>"}
{"request": [{"role": "system", "text": "<инструкция>"}, {"role": "user", "text": "<Вопрос>"}], "response": "<Ответ>"}
{"request": [{"role": "system", "text": "<инструкция>"}, {"role": "user", "text": "<Вопрос>"}, {"role": "assistant", "text": "<Реплика_1>"}, {"role": "user", "text": "<Реплика_2>"}, {"role": "assistant", "text": "<Реплика_3>"}], "response": "<Ответ>"}
```

> **Совет**
> При дообучении модели указывайте одну и ту же инструкцию для каждого обучающего примера и используйте ее при обращении к дообученной модели. Это повысит эффективность дообучения.

Датасет для дообучения должен содержать примеры как минимум 10 запросов и эталонных ответов. Максимальная длина запроса — 8 000 [токенов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html), максимальная длина эталонного ответа — 2 000 токенов. Длина запроса и ответа не должна превышать 8 000 токенов.

Пример наполнения датасета для дообучения модели генерации текста:

```json
{"request": [{"role": "system", "text": "Твое имя Женя..."}, {"role": "user", "text": "Как тебя зовут?"}], "response": "Меня зовут Женя."}
```

**Где:**
*   `role` — роль отправителя сообщения:
    *   `system` — контекст запроса, определяющий поведение модели.
    *   `user` — пример пользовательского запроса к модели.
*   `text` — текстовое содержимое сообщения.
*   `response` — идеальный ответ модели.

## Датасеты для классификации текста

При создании датасетов для классификации текста старайтесь давать классам значащие имена.
При дообучении модели классификатора на базе YandexGPT действуют следующие ограничения:

| Вид ограничения | Минимальное значение | Максимальное значение |
| --- | --- | --- |
| Количество примеров в датасете | 100 | 50 000 |
| Количество классов | 1 | 100 |
| Количество примеров для одного класса в датасете | 1 | — |
| Длина имени класса в символах | — | 100 |
| Количество токенов в тексте классифицируемого запроса | — | 8 000 |

Рекомендуется дообучать модели на датасетах, содержащих не менее 1 000 примеров и не менее 100 примеров для каждого класса.

### Многоклассовая классификация

Датасеты для многоклассовой классификации должны содержать примеры текстов и их принадлежности к классам. Каждая строка содержит отдельный пример в формате JSON. Каждый пример может быть отнесен только к одному классу.

```json
{"text":"<текст_1>","<класс_1>":0,"<класс_2>":0,"<класс_3>":1}
{"text":"<текст_2>","<класс_1>":1,"<класс_2>":0,"<класс_3>":0}
```

Пример наполнения датасета:
```json
{"text":"ну ничего себе и как это произошло","гнев":0,"страх":0,"радость":0,"грусть":0,"удивление":1}
```

### Классификация с несколькими метками

Датасеты для классификации с несколькими метками должны содержать примеры текстов и их принадлежности к классам, при этом каждый текст может относиться одновременно к нескольким классам.

```json
{"text":"<текст_1>","<класс_1>":0,"<класс_2>":0,"<класс_3>":1}
{"text":"<текст_2>","<класс_1>":1,"<класс_2>":0,"<класс_3>":1}
```

### Бинарная классификация

Датасеты для бинарной классификации должны содержать примеры текстов и признаки их принадлежности к классу. Каждая строка датасета содержит отдельный пример в формате JSON.

```json
{"text":"<текст_1>","<класс>":1}
{"text":"<текст_2>","<класс>":0}
```

## Датасеты для эмбеддингов

Датасеты для дообучения эмбеддингов могут содержать пары текстов, близких по значению, или триплеты с текстом, близким по смыслу текстом и текстом, не имеющим отношения к основному.

**Структура датасета с парами:**
```json
{"anchor":"<основной_текст_1>","positive":"<близкий_текст_1>"}
```

**Структура датасета с триплетами:**
```json
{"anchor":"<основной_текст_1>","positive":"<близкий_текст_1>","negative":"<негативный_пример_1>"}
```

**Где:**
*   `anchor` — основной текст.
*   `positive` — текст, близкий по смыслу основному.
*   `negative` — текст, не имеющий отношения к основному.

## Визуально-текстовые датасеты

Визуально-текстовые датасеты понадобятся при работе с [мультимодальными моделями](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html) в пакетном режиме.

### Датасеты запросов
```json
{"request": [{"role": "user", "content": [{"type": "text", "text": "Вопрос"}, {"type": "image", "image": "Base64"}]}]}
```

### Датасеты ответов
```json
{"request": [{"role": "user", "content": [{"type": "text", "text": "Вопрос"}, {"type": "image", "image": "Base64"}]}], "response": "Ответ"}
```

## Примеры использования
*   [Дообучить модель генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/create.html)
*   [Дообучить модель классификации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/tune-classifiers.html)
*   [Создать датасет для дообучения модели генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-dataset-gpt.html)
*   [Создать датасет для дообучения модели классификации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-dataset-classifier.html)

## 3.11 Дообучение

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html

[Yandex AI Studio](https://aistudio.yandex.ru/) позволяет дообучать по методу [LoRA](https://arxiv.org/abs/2106.09685) (*Low-Rank Adaptation of Large Language Models*) модель генерации текста YandexGPT Lite, [классификаторы](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/index.html) на базе YandexGPT Lite и модель [эмбеддингов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html).

> **Примечание**
> Функциональность находится на стадии [Preview](https://yandex.cloud/ru/docs/overview/concepts/launch-stages).

## Возможности дообучения моделей генерации текста

Модели генерации текста не получится дообучить новой информации, например базе знаний службы поддержки. Однако вы можете обучить модель отдавать ответ в определенном формате или анализировать текст. Так, модель можно обучить:

* пересказывать и изменять формулировки текстов;
* генерировать вопросы к тексту и ответы на них;
* форматировать ответы в определенной стилистике или формате;
* классифицировать тексты, обращения и диалоги;
* извлекать сущности из текста;
* дообучать модели классификации и эмбедингов.

## Процесс дообучения в AI Studio

Требования к данным для дообучения см. в разделах [Датасеты для генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/resources/dataset.html#generating), [Датасеты для классификации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/resources/dataset.html#classifier) и [Датасеты для эмбеддингов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/resources/dataset.html#embeddings).

Подготовленные данные необходимо загрузить в Yandex Cloud в виде *[датасета](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/resources/dataset.html)*. По умолчанию вы можете загрузить до 5 ГБ данных для дообучения в один датасет. Со всеми ограничениями вы можете ознакомиться в разделе [Квоты и лимиты в Yandex AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html).

После загрузки датасета запустите дообучение, указав его тип и, опционально, задав параметры. Дообучение займет от 1 часа до 1 суток в зависимости от объема данных и загруженности системы.

Примеры дообучения моделей доступны в разделах [Дообучить модель генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/create.html), [Дообучить модель классификации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/tune-classifiers.html) и [Дообучить модель эмбеддингов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/create-embeddings.html).

Для дообучения моделей в AI Studio вам понадобится [роль](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html) `ai.editor`. Она позволит загрузить данные и запустить дообучение.

## Запросы к дообученным моделям

После завершения обучения вы получите идентификатор дообученной модели. Этот идентификатор нужно передавать в поле `modelUri` тела запроса. Обращаться к дообученной модели генерации текста можно через [API генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/text-generation/api-ref/index.html), из Yandex DataSphere и других приложений. Чтобы отправить запрос дообученному классификатору, используйте метод [classify](https://aistudio.yandex.ru/docs/ru/ai-studio/text-classification/api-ref/TextClassification/classify.html) Text Classification API. Вы также можете использовать [Yandex AI Studio SDK](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk/index.html) для работы с дообученными моделями.

> **Примечание**
> Для корректной работы дообученной модели указывайте инструкцию, использованную при обучении, в сообщении с ролью отправителя `system`.

Чтобы отправлять запросы через API в ноутбуках [DataSphere](https://datasphere.yandex.cloud/), добавьте пользовательский или сервисный аккаунт, от имени которого будут выполняться запросы, в список участников проекта DataSphere. Аккаунт должен иметь роль `ai.languageModels.user`.

## Примеры использования

* [Дообучить модель генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/create.html)
* [Дообучить модель классификации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/tune-classifiers.html)
* [Создать датасет для дообучения модели генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-dataset-gpt.html)
* [Создать датасет для дообучения модели классификации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-dataset-classifier.html)

## 3.12 Токены

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html

Нейросети работают с текстами, представляя слова и предложения в виде *токенов* — смысловых отрывков или часто встречающихся последовательностей символов, характерных для естественного языка. Токены позволяют нейросетям находить закономерности и обрабатывать естественный язык.

Каждая модель использует свой токенизатор для обработки текстов, поэтому количество токенов в одном и том же тексте будет отличаться. При работе с моделями через OpenAI-совместимые API количество использованных токенов возвращается в каждом ответе модели в поле `usage`. Если же вы хотите предварительно оценить, сколько токенов содержится в тексте, воспользуйтесь токенизатором выбранной модели.

Модели Яндекса используют токенизатор, специально оптимизированный для работы с текстами на русском языке. Это позволяет увеличить среднее количество символов в токене и уменьшить стоимость обработки текста. Вы можете бесплатно [оценить](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/evaluate-request.html) размер любого текста в токенах в представлении моделей Яндекса с помощью специальных методов [Tokenizer](https://aistudio.yandex.ru/docs/ru/ai-studio/text-generation/api-ref/Tokenizer/index.html) или [Yandex AI Studio SDK](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk/index.html).

Чтобы использовать токенизатор в AI Studio, необходима [роль](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html#languageModels-user) `ai.languageModels.user` или выше на [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder).

## Пример

> **Примечание**
> Все примеры приведены для иллюстрации и не отражают итоговое количество токенов, которое будет израсходовано в реальных задачах. Коэффициенты получены с помощью расчетов, для оценки количества токенов в тексте использованы токенайзеры, доступные в интернете.

* **Текст на русском**: Управление генеративными моделями осуществляется с помощью промптов. Эффективный промпт должен содержать контекст запроса (инструкцию) для модели и непосредственно задание, которое модель должна выполнить, учитывая переданный контекст. Чем конкретнее составлен промпт, тем более точными будут результаты работы модели.
Кроме промпта на результаты генерации моделей будут влиять и другие параметры запроса. Используйте AI Playground, доступный в интерфейсе AI Studio, чтобы протестировать ваши запросы.
**Количество символов в тексте**: 501.

| | YandexGPT Pro | Qwen3 235B | gpt-oss-120b |
| --- | --- | --- | --- |
| Количество токенов в тексте | 96 | 139 | 109 |
| Среднее количество символов в токене | 5,2 | 3,6 | 4,6 |

* **Текст на английском языке**: Generative models are managed using prompts. A good prompt should contain the context of your request to the model (instruction) and the actual task the model should complete based on the provided context. The more specific your prompt, the more accurate will be the results returned by the model.
Apart from the prompt, other request parameters will impact the model's output too. Use Foundation Models Playground available from the management console to test your requests.
**Количество символов в промпте**: 477.

| | Alice AI LLM | Qwen3 235B | gpt-oss-120b |
| --- | --- | --- | --- |
| Количество токенов в тексте | 89 | 87 | 87 |
| Среднее количество символов в токене | 5,36 | 5,48 | 5,48 |

## Токенизировать текст для YandexGPT Pro

1. Создайте файл `tbody.json`, содержащий параметры запроса:

```json
{
  "modelUri": "gpt://<идентификатор_каталога>/yandexgpt",
  "text": "Управление генеративными моделями осуществляется с помощью промптов. Эффективный промпт должен содержать контекст запроса (инструкцию) для модели и непосредственно задание, которое модель должна выполнить, учитывая переданный контекст. Чем конкретнее составлен промпт, тем более точными будут результаты работы модели."
}
```

Где `<идентификатор_каталога>` — [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id) Yandex Cloud, на который у вашего аккаунта есть роль `ai.languageModels.user` или выше.

2. Отправьте запрос к модели:

```bash
export IAM_TOKEN=<IAM-токен>
curl --request POST \
  --header "Authorization: Bearer ${IAM_TOKEN}" \
  --data "@tbody.json" \
  "https://ai.api.cloud.yandex.net/foundationModels/v1/tokenize"
```

Где:
* `<IAM-токен>` — значение [IAM-токена](https://yandex.cloud/ru/docs/iam/concepts/authorization/iam-token), полученного для вашего аккаунта.
* `tbody.json` — файл в формате JSON, содержащий параметры запроса.

<details>
<summary>Результат</summary>

```json
{
  "tokens": [
    {
      "id": "1",
      "text": "<s>",
      "special": true
    },
    {
      "id": "19078",
      "text": " Управление",
      "special": false
    },
    {
      "id": "13612",
      "text": " генеративными",
      "special": false
    },
    ...
    {
      "id": "2",
      "text": "</s>",
      "special": true
    }
  ],
  "modelVersion": "06.12.2023"
}
```
</details>

---
**Ссылки на другие страницы документации:**
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
* [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
* [Обзор Model Gallery](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html)
* [Модели базового инстанса](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html)
* [Модели выделенного инстанса](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/dedicated-instance.html)
* [Пакетная обработка данных](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/batch-processing.html)
* [Вызов функций](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/function-call.html)
* [Режим рассуждений](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/chain-of-thought.html)
* [Форматирование ответов моделей](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/structured-output.html)
* [Эмбеддинги](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html)
* [Датасеты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/resources/dataset.html)
* [Дообучение](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html)
* [Обзор AI-агентов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/index.html)

---


# 4. Agent Atelier


## 4.1 Обзор AI-агентов

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/index.html

AI-агенты — это современный подход к построению приложений на основе искусственного интеллекта и нейросетей. Агенты расширяют возможности больших языковых моделей и служат основой для построения чат-ботов, ассистентов и голосовых интерфейсов, помогая автоматизировать разнообразные рутинные задачи.

Агенты состоят из четырех ключевых компонентов:
* **LLM** — сама языковая модель с зафиксированными настройками.
* **Инструкция (prompt)** — описывает поведение и роль агента.
* **Инструменты (tools)** — позволяют агенту использовать внешние возможности, например API, функции или поиск по интернету.
* **Память (memory)** — отвечает за хранение контекста и истории взаимодействия.

Такая архитектура позволяет создавать текстовые и голосовые агенты, которые ведут себя более естественно и автономно, чем классические чат-боты.

## Разработка агентов в AI Studio

AI Studio имеет все необходимое для создания AI-агентов: модели с поддержкой [вызова функций](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/function-call.html) и [форматирования ответа](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/structured-output.html), готовые настраиваемые [инструменты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/index.html#tools) для RAG-сценариев поиска в интернете и поиска по файлам, а также MCP Hub, который позволяет подключать внешние API через MCP-серверы.

AI Studio позволяет создавать агентов разными способами:
* в [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/);
* с помощью [конструктора спецификаций](https://console.yandex.cloud/link/serverless-integrations/workflows/workflows) Yandex Workflows;
* с помощью Responses API или Realtime API;
* через опенсорс-фреймворки, например OpenAI SDK, LangGraph или LangChain.

## Инструменты

Агенты могут автоматически вызывать инструменты, чтобы получить дополнительную информацию для генерации или выполнить необходимые действия. В AI Studio доступны следующие готовые инструменты:
* **File Search Tool** – реализует сценарии RAG и позволяет AI-агенту искать информацию для ответа в ваших файлах (базе знаний). Вы можете загрузить документы базы знаний в интерфейсе AI Studio, через Vector Store API или через [Files API](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/filesearch.html) и создать поисковый индекс. [Поисковые индексы](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore.html) хранят информацию из документов в векторном виде и позволяют агентам использовать ее при ответе.
* **Web Search Tool** — позволяет агенту искать информацию в интернете через поисковую базу Яндекса, чтобы обогащать ответ актуальными сведениями по теме запроса. Подробнее про использование [инструмента поиска в интернете](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/websearch.html).
* **MCP Tool** — отвечает за подключение к MCP-серверам для работы со сторонними API. В разделе MCP Hub вы можете создавать и настраивать подключения к новым и уже существующим MCP-серверам, а также следить за их состоянием.
* **[Code Interpreter](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/code-interpreter.html)** — позволяет агенту писать, воспроизводить и отлаживать Python-код в виртуальной тестовой среде. Поддерживает сохранение состояния при выполнении и работу с файлами и визуализацией. Подходит для задач, где важно проверять и преобразовывать данные, а не ограничиваться текстовыми рассуждениями.

## API создания агентов

AI Studio предоставляет два OpenAI-совместимых API для разработки различных типов агентов. Оба API сохраняют данные о состоянии клиента между запросами и решают одни и те же задачи — подключают модели, инструменты и память, — но оптимизированы под разные типы взаимодействия в зависимости от агента.
* **Responses API** – это API для текстовых сценариев. Агенты, созданные с помощью Responses API, учитывают контекст переписки и могут автоматически вызывать подключенные инструменты. Responses API поддерживает работу со всеми [текстовыми моделями](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html).
* **Realtime API** — это API для реализации голосовых сценариев. API предназначен для работы со специализированными мультимодальными моделями, которые принимают аудио на вход и синтезируют ответ в виде аудио. Realtime API поддерживает все доступные инструменты, включая Retrieval и WebSearch.

## Конструктор рабочих процессов

Конструктор рабочих процессов позволяет собирать сложные сценарии на базе AI с помощью готовых шагов автоматизации и управления. Конструктор подойдет тем, кто предпочитает визуальные редакторы и платформы Low-code.

Подробнее о рабочих процессах и шагах автоматизации см. в [документации Yandex Workflows](https://yandex.cloud/ru/docs/serverless-integrations/concepts/workflows/workflow).

---
### Ссылки на другие страницы документации:
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
* [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
* [Текстовые агенты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/text-agents.html)
* [Голосовые агенты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/realtime.html)
* [Управление контекстом диалога](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/conversations-api.html)
* [Code Interpreter](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/code-interpreter.html)
* [Публичные материалы](https://aistudio.yandex.ru/docs/ru/ai-studio/public-talks.html)
* [Термины и определения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html)
* [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)
* [Токены](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html)
* [Обзор технологий SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/overview.html)
* [О сервисе Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/concepts/index.html)
* [О сервисе Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/concepts/ocr/index.html)
* [О сервисе Translate](https://aistudio.yandex.ru/docs/ru/translate/concepts/index.html)

## 4.2 Текстовые агенты

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/text-agents.html

Текстовые агенты — это инструмент Yandex AI Studio для создания интеллектуальных приложений с поддержкой контекста и внешних интеграций. Агенты могут взаимодействовать через чат, формы, API и другие интерфейсы.

Возможности: ведение диалога с учетом истории; генерация ответов в заданном формате; автоматический вызов инструментов; работа с документами; поиск в интернете; использование внешних API через MCP-серверы; сохранение состояния.

## Инструменты текстовых агентов

- **File Search Tool** — RAG по документам и базам знаний
- **Web Search Tool** — поиск в интернете через базу Яндекса
- **Code Interpreter Tool** — выполнение кода в изолированной среде
- **MCP Tool** — подключение к сторонним API через MCP-серверы

## API для создания текстовых агентов

Используется Responses API — OpenAI-совместимый API для текстовых сценариев.

## Способы создания

- Agent Atelier (прототипирование)
- Responses API (программная интеграция)
- Yandex Workflows (low-code)
- OpenAI SDK, LangChain, LangGraph

## 4.3 Голосовые агенты (Realtime API)

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/realtime.html

Голосовые агенты в Yandex AI Studio используют Realtime API для создания голосовых интерфейсов. Realtime API работает через WebSocket и поддерживает потоковую обработку аудио.

## Модель

Используется модель `speech-realtime-250923` для голосового взаимодействия в реальном времени.

## Голоса

Доступны различные голоса для синтеза речи.

## Сессии

Работа происходит через сессии WebSocket, в рамках которых происходит обмен событиями.

## События

API использует событийную модель для управления потоком аудио и текста.

## Инструменты голосовых агентов

- **Вызов функций** — вызов пользовательских функций во время разговора
- **Поиск в интернете** — поиск информации в реальном времени
- **Поиск по файлам** — поиск по загруженным документам
- **MCP** — подключение к внешним сервисам через MCP-серверы

## 4.4 Управление контекстом диалога

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/conversations-api.html

При работе с Responses API для управления контекстом вы можете [соединять ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/manage-context.html#previous-response) друг с другом, [передавать историю сообщений](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/manage-context.html#manual) в каждом запросе или [использовать Conversations API](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/manage-context.html#conversations-api), чтобы хранить диалог как долгоживущий объект со стабильным идентификатором.

Conversations API воссоздает состояние диалога с помощью сохраненных элементов:
* сообщения пользователя и ассистента;
* вызовы инструментов (`tool calls`);
* другие служебные сообщения.

Редактирование элементов и обнуление диалога в настоящий момент не поддерживаются. Чтобы перезагрузить диалог, создайте новый объект `conversation`.

## Пример

В многошаговом диалоге объект `conversation` передается в следующие запросы, чтобы сохранять состояние и разделять контекст между ответами:

```python
import openai

YANDEX_CLOUD_FOLDER = "<идентификатор_каталога>"
YANDEX_CLOUD_API_KEY = "<API-ключ>"
YANDEX_CLOUD_MODEL = "yandexgpt"

client = openai.OpenAI(
    api_key=YANDEX_CLOUD_API_KEY,
    base_url="https://ai.api.cloud.yandex.net/v1",
    project=YANDEX_CLOUD_FOLDER
)

# Создаем conversation
conv = client.conversations.create()

# Первое сообщение с системной инструкцией и пользовательским вводом
r1 = client.responses.create(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    conversation=conv.id,
    input=[
        {"role": "system", "content": "Ты мой ассистент"},
        {"role": "user", "content": "Привет! Запомни: меня зовут Настя."}
    ]
)
print("assistant:", r1.output_text)

# Продолжаем в том же conversation
r2 = client.responses.create(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    conversation=conv.id,
    input="Как меня зовут?"
)
print("assistant:", r2.output_text)
```

---
**Ссылки на другие страницы:**
* Предыдущая: [Голосовые агенты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/realtime.html)
* Следующая: [Code Interpreter](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/code-interpreter.html)

## 4.5 Code Interpreter

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/code-interpreter.html

> **Примечание**
> Функциональность находится на стадии [Preview](https://yandex.cloud/ru/docs/overview/concepts/launch-stages).

**Code Interpreter** — это встроенный инструмент [Yandex AI Studio](https://aistudio.yandex.ru/), позволяющий модели писать и выполнять Python-код в изолированной тестовой среде. Он используется в задачах, где одних текстовых рассуждений недостаточно и требуется фактическое выполнение вычислений.

Инструмент исполнения кода особенно полезен в следующих сценариях:
* анализ данных;
* программирование и отладка логики;
* математические вычисления;
* работа с файлами и изображениями.

> **Примечание**
> Сессии с Code Interpreter являются контекстно-нагруженными (код, данные, результаты выполнения). Для них рекомендуется использовать модели с большим контекстным окном, например Qwen.

## Основные возможности

### Выполнение Python-кода
Code Interpreter предоставляет модели полноценную среду выполнения Python, встроенную в процесс рассуждения. В рамках одной сессии модель может:
* писать Python-код для решения задачи;
* выполнять код в изолированной среде;
* получать точные и детерминированные результаты;
* анализировать возникающие ошибки;
* вносить изменения в код и повторно запускать его до получения корректного результата.

Ключевая особенность инструмента — итеративность. Выполнение кода не является разовым действием: модель может последовательно уточнять логику, исправлять ошибки и усложнять решение, опираясь на результаты предыдущих запусков. Благодаря этому Code Interpreter особенно хорошо подходит для задач, в которых важны проверка гипотез вычислениями, пошаговый анализ, высокая точность и воспроизводимость результатов.

### Работа с файлами и данными
Code Interpreter интегрирован с Files API и использует его как основной механизм передачи и хранения данных.
С помощью инструмента агент может:
* загружать и обрабатывать файлы различных форматов (CSV, JSON, XLSX, TXT и др.);
* создавать в процессе выполнения кода новые файлы — таблицы, датасеты, отчеты, графики и изображения;
* использовать файлы, переданные пользователем во входных данных запроса, как исходные данные для анализа и вычислений.

Все файлы, переданные в запросе через Files API, сохраняются в [контейнер](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/code-interpreter.html#containers) и остаются доступны модели на протяжении всего жизненного цикла этого контейнера без необходимости повторной загрузки.

Созданные моделью файлы возвращаются как аннотации, содержащие имя файла и его идентификатор (`file_id`). Полученный идентификатор может быть использован для скачивания файла через Files API.

## Генерация изображений и графиков
Code Interpreter позволяет не только выполнять вычисления, но и визуализировать результаты работы. Инструмент может использоваться для:
* построения различных типов графиков;
* визуализации числовых и категориальных данных;
* наглядного представления промежуточных и финальных результатов;
* сохранения визуализаций в виде файлов изображений.

Результаты работы модели сохраняются в полноценные визуальные артефакты, которые можно скачать и использовать на следующих шагах обработки или отображать в интерфейсе клиента.

## Контейнеры
Контейнер — это полностью изолированная виртуальная среда, в которой Code Interpreter выполняет Python-код. Он не имеет доступа к внешним ресурсам и самостоятельно хранит временные данные и состояние выполнения вычислений.

Контейнер можно создать двумя способами:
* **Автоматический режим (Auto)** — контейнер создается при вызове Responses API с инструментом Code Interpreter и доступен по адресу `/v1/containers`. При создании можно указать список файлов для загрузки.
  * Время жизни — 20 минут после последней активности. При перезапуске вычислений данные предыдущего запроса удаляются.
* **Ручное создание контейнера (Explicit)** — контейнер создается заранее через эндпоинт `/v1/containers`, после чего его идентификатор (`container_id`) передается в конфигурации инструмента.
  * Время жизни после последней активности настраивается пользователем через параметр `expire_after`, но не может составлять более 20 минут. При перезапуске вычислений данные предыдущего запроса не удаляются.

Данные всех видов контейнеров автоматически выгружаются во внешнее хранилище через Files API. Ссылки на файлы доступны в аннотации `container_file_citation`.

## См. также
* [Выполнить задачу с помощью Code Interpreter](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/use-code-interpreter.html)
* [Управление контекстом диалога](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/conversations-api.html)
* [Обзор AI Search](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/index.html)

---


# 5. AI Search


## 5.1 Обзор AI Search

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/index.html

[AI Search](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/index.html) — это набор инструментов и технологий AI Studio, которые позволяют моделям генерировать ответы на основе проверенных данных, например корпоративных документов, внутренних баз знаний или информации из интернета.

AI Search предоставляет инструменты для поиска по двум типам источников:
* собственные данные пользователя (документы, инструкции, FAQ) — [инструмент File Search](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/filesearch.html);
* выбранные домены в интернете — [инструмент Web Search](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/websearch.html).

Вы можете использовать оба инструмента при создании [голосовых агентов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/realtime.html) с помощью Realtime API или в Responses API при создании текстовых агентов и обращений к моделям генерации текста, чтобы формировать точные, актуальные и проверяемые ответы. Оба инструмента могут быть подключены одновременно, но модель сама решает, что нужно использовать, в зависимости от запроса пользователя, описания инструментов и заданного промпта.

## Как работает AI Search

Модели могут использовать для генерации текста только ту информацию, которая была заложена в них при обучении или передана в контексте запроса. Поэтому, чтобы выбранная вами модель из Model Gallery могла сгенерировать ответ с учетом вашей информации, данные необходимо подготовить и передать в контексте запроса. Обогащение контекста выполняется в несколько этапов:

1. **Индексация данных.** По умолчанию AI Studio автоматически подготавливает данные для поиска. Вам необходимо только загрузить файлы в интерфейсе AI Studio или через Files API и создать поисковый индекс Vector Store. После этого AI Studio разобьет данные на чанки (chunks) нужного размера — фрагменты текста от нескольких строк до нескольких абзацев — а затем [токенизирует](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html) их и сохранит в поисковом индексе.
   Чтобы исключить возможную потерю смысла при подготовке файлов, вы можете [самостоятельно разбить](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-prechunked-search-agent.html) данные на чанки и загрузить их в AI Studio в формате [JSONL](https://jsonlines.org/). Максимальная длина одного чанка — 8 000 символов.
2. **Формирование поискового запроса.** В зависимости от поставленной задачи и описанных в промпте условий использования инструментов поиска модель формулирует запрос к инструментам поиска по файлам или поиска в интернете.
3. **Получение найденных фрагментов.** Использованный инструмент возвращает наиболее релевантную информацию из поискового индекса в виде чанков и добавляет ее в контекст модели.
4. **Генерация ответа.** Модель использует найденную информацию как факты для ответа, сохраняя тональность, стиль и инструкции из промпта.

## Примеры использования

* [Создать текстового агента с поиском в интернете](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-websearch-text-agent.html)
* [Создать текстового агента с поиском по файлам](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-filesearch-text-agent.html)
* [Создать агента с поиском по заранее созданным чанкам](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-prechunked-search-agent.html)

---

**Другие страницы документации:**
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
* [Поисковые индексы Vector Store](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore.html)
* [Инструмент поиска по файлам](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/filesearch.html)
* [Инструмент поиска в интернете](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/websearch.html)
* [Code Interpreter](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/code-interpreter.html)
* [Термины и определения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html)
* [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)

## 5.2 Поисковые индексы Vector Store

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore.html

Поисковые индексы Vector Store позволяют хранить и индексировать документы для семантического поиска.

## Создание индекса

Для создания поискового индекса необходимо указать параметры индексирования.

## Загрузка файлов

Файлы загружаются в индекс и автоматически разбиваются на фрагменты.

## Индексирование

После загрузки файлы индексируются с использованием эмбеддингов.

## Логика разбиения на фрагменты

Документы автоматически разбиваются на фрагменты оптимального размера для поиска.

## Метаданные

К каждому фрагменту можно прикрепить метаданные для фильтрации.

## Использование

Vector Store используется совместно с инструментом File Search для RAG-сценариев.

## Управление

Управление индексами доступно через API и веб-интерфейс.

## Сценарии использования

- Поиск по базам знаний
- Вопросно-ответные системы
- Контекстная генерация ответов

## 5.3 Инструмент поиска по файлам

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/filesearch.html

Инструмент поиска по файлам расширяет возможности моделей, позволяя выполнять гибридный поиск по файлам пользователя при формировании ответа. Инструмент можно подключить в Responses API и Realtime API.

Чтобы в Responses API разрешить модели искать информацию в файлах, укажите инструмент `file_search` и идентификатор [поискового индекса Vector Store](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/manage-searchindex.html). Поисковый индекс содержит информацию о файлах, которые будут использоваться для поиска.

Найденные чанки с релевантной информацией будут добавлены в контекст модели, что увеличит количество потребленных токенов. Если поисковый индекс большой, ограничьте количество возвращаемых результатов с помощью параметра `max_num_results`, чтобы контекст модели не переполнялся слишком быстро. Стоимость использования инструмента см. в разделе [Правила тарификации для Yandex AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html).

### Пример использования на Python

```python
response = client.responses.create(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    # SpeechKit Voice Profiler — несуществующий, по крайней мере пока, продукт, описание которого было загружено в Vector Store для примера.
    instructions="Ты помогаешь пользователю с документацией. При вопросах про SpeechKit Voice Profiler используй поисковый индекс.",
    input="Расскажи про продукт SpeechKit Voice Profiler",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [<идентификатор_поискового_индекса>],
        "max_num_results": 3
    }]
)
```

> **Важно**
> Одновременно к модели может быть подключен только один поисковый индекс.

## Аннотации

Ответ с результатами поиска по файлам содержит объект `annotations`. Используйте его, чтобы отследить и показать пользователю источники данных. Поле `filename` объекта `annotations` содержит имя файла, в котором была найдена использованная информация, а `file_id` — его идентификатор. Остальные поля объекта заполняются значениями по умолчанию, чтобы сохранить совместимость с OpenAI:

```json
"annotations": [
  {
    "file_id": "...",
    "filename": "Yandex SpeechKit Voice Profiler.docx",
    "index": 0,
    "type": "file_citation"
  }
 ...
]
```

## Возможные сценарии использования инструмента

Инструмент поиска по файлам может быть полезен при решении многих задач:
* **Корпоративный ассистент**: ответы по внутренним документам и регламентам организации.
* **Техподдержка по продукту**: поиск по технической документации, SDK и FAQ со ссылками на фрагменты.
* **Юридическая консультация**: ответы по внутренним юридическим документам с указанием цитат и источников в ответе.
* **Подготовка новых сотрудников**: ответы на вопросы стажера по внутренним политикам и архитектуре проекта.
* **Продажи**: поиск успешных сделок в директории с презентациями и коммерческими предложениями.

## Примеры использования

* [Создать текстового агента с поиском по файлам](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-filesearch-text-agent.html)

## Ссылки на другие страницы документации
* [Поисковые индексы Vector Store](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore.html)
* [Правила тарификации для Yandex AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html)
* [Инструмент поиска в интернете](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/websearch.html)
* [Документация AI Studio](https://aistudio.yandex.ru/docs/ru/index.html)

## 5.4 Инструмент поиска в интернете

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/websearch.html

Инструмент поиска в интернете позволяет модели получать информацию из открытых источников и использовать ее для формирования более точных и актуальных ответов. Поиск может выполняться как по всему интернету, так и по ограниченному списку сайтов. Инструмент можно подключить в Responses API и Realtime API. Стоимость использования инструмента см. в разделе [Правила тарификации для Yandex AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html).

> **Совет**
> При каждом вызове инструмента веб-поиска расходуются [квоты на синхронные запросы](https://aistudio.yandex.ru/docs/ru/search-api/concepts/limits.html#search-api-quotas) Yandex Search API. Учитывайте ограничения сервиса Yandex Search API при интенсивном использовании инструмента.

Если инструмент подключен, модель самостоятельно принимает решение, нужна ли дополнительная информация для формирования ответа. Чтобы разрешить модели искать информацию в интернете при генерации ответов, в параметрах запроса укажите инструмент `web_search`. При подключении инструмента через Responses API доступны следующие опциональные параметры:

*   `allowed_domains` — массив, содержащий до 5 доменов для поиска. Если список доменов не будет задан, поиск будет выполняться по всему интернету.
*   `user_location` — ограничение региона поиска. Если необходимо, укажите [код региона](https://aistudio.yandex.ru/docs/ru/search-api/reference/regions.html) в поле `region`.
*   `search_context_size` — объем полученного из поиска контекста. Регулирует полноту и детализацию ответа и потребление токенов при использовании инструмента. Доступны значения `low`, `medium`, `high`. По умолчанию — `medium`.

### Python

```python
response = client.responses.create(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    input="Сделай краткий обзор последних новостей об LLM в 2025 году — только факты, без домыслов.",
    tools=[
        {
            "type": "web_search",
            "filters": {
                "allowed_domains": [
                    "habr.ru"
                ],
                "user_location": {
                    "region": "213",
                },
            },
            "search_context_size": "medium", # варианты: low | medium | high
        }
    ],
    temperature=0.3,
    max_output_tokens=1000
)
```

Ответ, обогащенный поиском в интернете, содержит объект `annotations`. Используйте его, чтобы отследить и показать пользователю источники данных. Поле `url` объекта `annotations` содержит адрес сайта, на котором была найдена использованная информация. Все остальные поля объекта заполняются значениями по умолчанию, чтобы сохранить совместимость с OpenAI:

```json
"annotations": [
  {
    "end_index": 0,
    "start_index": 0,
    "title": "",
    "type": "url_citation",
    "url": "www.rbc.ru"
  },
  {
    "end_index": 0,
    "start_index": 0,
    "title": "",
    "type": "url_citation",
    "url": "ria.ru"
  }
]
```

## Возможные сценарии использования инструмента

Инструмент поиска в интернете может быть полезен при решении многих задач:
*   **Актуализация справочной информации**: составить резюме, что поменялось в правилах магазина приложений на этой неделе.
*   **Конкурентный обзор**: собрать новинки и сценарии конкурентов на основе информации, опубликованной на их сайтах.
*   **Проверка фактов в пресс-релизе**: сверить цитаты и цифры перед публикацией.
*   **Радар трендов**: собрать быстрый обзор новостей на заданную тему за сутки или неделю для дайджеста.
*   **Подготовка к встрече**: сделать описание компании клиента перед созвоном.

## Примеры использования

*   [Создать текстового агента с поиском в интернете](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-websearch-text-agent.html)

---
### Ссылки на другие страницы документации

*   [Инструмент поиска по файлам](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/filesearch.html)
*   [Обзор MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/index.html)
*   [Правила тарификации для Yandex AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html)
*   [Квоты на синхронные запросы Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/concepts/limits.html#search-api-quotas)
*   [Код региона Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/reference/regions.html)

---


# 6. MCP Hub


## 6.1 Обзор MCP Hub

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/index.html

> **Примечание**
> Функциональность находится на стадии [Preview](https://yandex.cloud/ru/docs/overview/concepts/launch-stages).

Yandex AI Studio позволяет использовать [MCP-серверы](https://yandex.cloud/ru/docs/glossary/mcp) в AI-агентах для взаимодействия с внешними системами, чтобы получать дополнительный контекст или выполнять действия, например, через вызов внешнего [API](https://ru.wikipedia.org/wiki/API).

**MCP Hub** — это функциональность AI Studio, предназначенная для создания, управления и мониторинга MCP-серверов. MCP Hub позволяет как подключать внешние MCP-серверы, так и создавать собственные MCP-серверы с нуля или из предварительно настроенных шаблонов.

Чтобы обращаться к MCP-серверам в MCP Hub, необходима [роль](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html#serverless-mcpGateways-invoker) `serverless.mcpGateways.invoker` или выше. Чтобы обращаться к внешним MCP-серверам и MCP-серверам, созданным из шаблона, дополнительно необходима [роль](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html#serverless-mcpGateways-anonymousInvoker) `serverless.mcpGateways.anonymousInvoker` или выше.

## MCP-серверы

MCP-серверы позволяют подключать к [большим языковым моделям (LLM)](https://yandex.cloud/ru/docs/glossary/llm) сторонние инструменты, такие как API, базы знаний и различные сервисы, которые предоставляют моделям доступ к внешней информации и дают возможность выполнять сложные задачи. Для взаимодействия моделей с этими внешними инструментами в MCP-серверах используется протокол [MCP (Model Context Protocol)](https://modelcontextprotocol.io/docs/getting-started/intro).

> **Примечание**
> Один MCP-сервер может содержать до 50 инструментов.

Протокол MCP позволяет:
* интегрировать большие языковые модели в корпоративные системы, сервисы и внутренние базы знаний;
* обеспечить стандартизированный доступ моделей к внешним данным и инструментам;
* упростить разработку и масштабирование решений на базе LLM.

## Транспортные механизмы протокола MCP

Протокол MCP предусматривает использование одного из следующих транспортных механизмов:
* [Streamable HTTP](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#streamable-http) — современный и актуальный транспортный механизм. AI-агент сможет получать обновления (события) с сервера без необходимости поддерживать постоянное HTTP-соединение.
* [HTTP with SSE](https://modelcontextprotocol.io/specification/2024-11-05/basic/transports#http-with-sse) — устаревший транспортный механизм. AI-агент сможет получать обновления с сервера через одно постоянное HTTP-соединение.

## Сценарии использования MCP-серверов

Использование MCP-серверов позволяет реализовывать следующие сценарии:
* подключение моделей к [CRM](https://ru.wikipedia.org/wiki/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F_%D0%B2%D0%B7%D0%B0%D0%B8%D0%BC%D0%BE%D0%BE%D1%82%D0%BD%D0%BE%D1%88%D0%B5%D0%BD%D0%B8%D1%8F%D0%BC%D0%B8_%D1%81_%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%D0%B0%D0%BC%D0%B8)-, [ERP](https://ru.wikipedia.org/wiki/ERP)-системам или внутренним хранилищам;
* автоматизация бизнес-процессов и рабочих сценариев с использованием [AI](https://ru.wikipedia.org/wiki/%D0%98%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9_%D0%B8%D0%BD%D1%82%D0%B5%D0%BB%D0%BB%D0%B5%D0%BA%D1%82);
* создание специализированных AI-ассистентов (юридических, медицинских, технических и др.);
* интеграция с внешними API для получения актуальной информации, например, новостей, курсов валют и т.п.

## Добавление MCP-серверов в MCP Hub

MCP Hub предлагает три способа добавления MCP-серверов: подключение существующего внешнего сервера, создание нового сервера из шаблона и создание нового сервера с нуля.

Чтобы создать MCP-сервер, у пользователя должна быть [роль](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html#serverless-mcpGateways-editor) `serverless.mcpGateways.editor` или выше.

## Подключение внешнего MCP-сервера

Этот способ удобен, когда у вас уже есть развернутый внешний MCP-сервер, например, на [smithery.ai](https://smithery.ai/), из [Yandex Cloud Marketplace](https://aistudio.yandex.ru/marketplace) или на [виртуальной машине](https://yandex.cloud/ru/docs/compute/concepts/vm) Yandex Compute Cloud. Чтобы [добавить](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/connect-external.html) в MCP Hub такой MCP-сервер, укажите его адрес и данные для аутентификации, после чего он будет доступен для подключения к вашим агентам.

Подробнее см. в разделе [Подключить внешний MCP-сервер к MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/connect-external.html).

Вместо MCP Hub для обращения к внешнему MCP-серверу из AI-агента вы можете использовать Responses API. Для этого достаточно просто указать URL-адрес сервера и [API-ключ](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key) с заданной [областью действия](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key#scoped-api-keys) `yc.serverless.mcpGateways.invoke`.

<details>
<summary>Пример подключения MCP-сервера через Responses API:</summary>

```python
from openai import OpenAI

# Создаем клиента
client = OpenAI(
    api_key="<API-ключ>",
    base_url="https://ai.api.cloud.yandex.net/v1",
    project="<идентификатор_каталога>"
)

# Пример вызова MCP через Responses API
response = client.responses.create(
    model="gpt://<идентификатор_каталога>/yandexgpt",
    input=[
        {
            "role": "user",
            "content": "Найди клиента с именем Иван Иванов в CRM"
        }
    ],
    # MCP-инструменты, доступные модели
    tools=[
        {
            "server_label": "crm_lookup",
            "server_url": "<URL_MCP-сервера>",
            "type": "mcp",
            "metadata": {
                "description": "Поиск клиента в CRM по имени"
            }
        }
    ]
)

print(response.output_text)
```
</details>

## Создание MCP-сервера из шаблона

AI Studio предлагает набор шаблонов MCP-серверов от внешних партнеров Yandex Cloud, которые вы можете использовать в ваших AI-агентах для доступа к сервисам этих партнеров. Чтобы [добавить](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/create-from-template.html) в MCP Hub такой MCP-сервер, выберите нужный шаблон и укажите данные для аутентификации, после чего сервер будет доступен для подключения к вашим агентам.

Подробнее см. в разделе [Создать MCP-сервер в MCP Hub из шаблона](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/create-from-template.html).

Список доступных шаблонов см. в разделе [Шаблоны MCP-серверов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/templates.html).

## Создание MCP-сервера с нуля

В MCP Hub вы также можете самостоятельно [создать новый MCP-сервер](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/create-brand-new.html), содержащий следующие **инструменты**:

* [Функция](https://yandex.cloud/ru/docs/functions/concepts/function) Yandex Cloud Functions позволяет запускать ваш код на одном из поддерживаемых языков программирования с необходимыми зависимостями в обслуживаемой [среде выполнения](https://yandex.cloud/ru/docs/functions/concepts/runtime/index). При увеличении количества вызовов функции происходит ее автоматическое [масштабирование](https://yandex.cloud/ru/docs/functions/concepts/function#scaling) — создание дополнительных экземпляров.
* HTTPS-запрос позволяет обращаться к внешним [API](https://ru.wikipedia.org/wiki/API). Если у вас есть сервис с действующим API, вы можете преобразовать этот API в формат MCP. Опишите имеющиеся API-методы, и они автоматически конвертируются для использования в агентах.
* [Рабочий процесс](https://yandex.cloud/ru/docs/serverless-integrations/concepts/workflows/workflow) Yandex Workflows позволяет создавать и подключать к агенту сложные процессы, состоящие из различных взаимодействующих между собой инструментов и сервисов и реализующие собственную логику управления и обработки ошибок.

Подробнее см. в разделе [Создать MCP-сервер в MCP Hub с нуля](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/create-brand-new.html).

## Общие настройки MCP-серверов

MCP-серверы в MCP Hub могут быть приватными или публичными.

К созданному в [каталоге](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder) приватному MCP-серверу без аутентификации могут обращаться только AI-агенты, которые вызваны пользователем или сервисным аккаунтом с назначенной [ролью](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html#serverless-mcpGateways-invoker), разрешающей обращаться к MCP-серверам в этом каталоге. Другим агентам для обращения к приватному MCP-серверу требуется аутентификация — [IAM-токен](https://yandex.cloud/ru/docs/iam/concepts/authorization/iam-token) или [API-ключ](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key) сервисного аккаунта с заданной [областью действия](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key#scoped-api-keys) `yc.serverless.mcpGateways.invoke`.

К публичным MСP-серверам могут обращаться любые агенты без аутентификации.

В настройках MCP-сервера вы можете включить опцию [логирования](https://yandex.cloud/ru/docs/logging/concepts/log-group), чтобы сохранять информацию об обращениях к серверу в журнале.

## См. также

* [Шаблоны MCP-серверов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/templates.html)
* [Подключить внешний MCP-сервер к MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/connect-external.html)
* [Создать MCP-сервер в MCP Hub из шаблона](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/create-from-template.html)
* [Создать MCP-сервер в MCP Hub с нуля](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/create-brand-new.html)
* [Посмотреть информацию об MCP-сервере в MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/get-server-info.html)
* [Удалить MCP-сервер из MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/delete-server.html)

---
Предыдущая: [Инструмент поиска в интернете](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/websearch.html)
Следующая: [Шаблоны MCP-серверов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/templates.html)

## 6.2 Шаблоны MCP-серверов

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/templates.html

> [!NOTE]
> Функциональность находится на стадии [Preview](https://yandex.cloud/ru/docs/overview/concepts/launch-stages).

[Yandex AI Studio](https://aistudio.yandex.ru/) предлагает набор шаблонов MCP-серверов от внешних партнеров Yandex Cloud, которые вы можете использовать в ваших AI-агентах для доступа к сервисам этих партнеров. Чтобы добавить в [MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/index.html) такой MCP-сервер, выберите нужный шаблон и укажите данные для аутентификации, после чего сервер будет доступен для подключения к вашим агентам.

## Контур.Фокус {#kontur}

MCP-сервер [Контур.Фокус](https://focus.kontur.ru/) предназначен для проверки контрагентов — российских юридических лиц и индивидуальных предпринимателей. Позволяет получать информацию о контрагенте и экспресс-отчет о его состоянии, а также оценку его благонадежности по нескольким критериям. Поиск осуществляется по [ИНН](https://ru.wikipedia.org/wiki/%D0%98%D0%B4%D0%B5%D0%BD%D1%82%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B9_%D0%BD%D0%BE%D0%BC%D0%B5%D1%80_%D0%BD%D0%B0%D0%BB%D0%BE%D0%B3%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D1%89%D0%B8%D0%BA%D0%B0) контрагента. Кроме того, этот MCP-сервер позволяет выполнять поиск организаций и ИП по руководителю, адресу, сайту и другим параметрам. Для получения информации используются методы `req`, `search`, `scoring` и `briefReport`.

Чтобы получить токен доступа, обратитесь на [сайт](https://focus.kontur.ru/) сервиса.

## amoCRM {#amocrm}

MCP-сервер [amoCRM](https://www.amocrm.ru/) позволяет AI-агентам работать с информацией из amoCRM — получать в [CRM](https://ru.wikipedia.org/wiki/%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F_%D0%B2%D0%B7%D0%B0%D0%B8%D0%BC%D0%BE%D0%BE%D1%82%D0%BD%D0%BE%D1%88%D0%B5%D0%BD%D0%B8%D1%8F%D0%BC%D0%B8_%D1%81_%D0%BA%D0%BB%D0%B8%D0%B5%D0%BD%D1%82%D0%B0%D0%BC%D0%B8)-системе сведения о компаниях, лидах, контактах, создавать и редактировать данные, создавать заметки, просматривать пайплайны и задачи.

Чтобы получить доступ к CRM, AI-агент должен передать MCP-серверу аутентификационные данные:
* Токен доступа в заголовке `X-Auth-Token`. Чтобы получить токен доступа, воспользуйтесь [инструкцией](https://www.amocrm.ru/developers/content/oauth/step-by-step#get_access_token) производителя.
* Имя аккаунта в заголовке `X-Account-Name`.

## Яндекс Трекер {#tracker}

> [!IMPORTANT]
> Чтобы отправлять запросы к API Яндекс Трекер от имени сервисного аккаунта, сначала обратитесь в [службу поддержки Трекер](https://yandex.ru/support/tracker/ru/feedback) с указанием [идентификатора облака](https://yandex.cloud/ru/docs/resource-manager/operations/cloud/get-id) и [идентификатора сервисного аккаунта](https://yandex.cloud/ru/docs/iam/operations/sa/get-id). В противном случае запросы к API будут завершаться ошибкой с кодом `401 Unauthorized`.

MCP-сервер [Яндекс Трекер](https://360.yandex.ru/business/tracker/) позволяет AI-агенту полноценно работать с задачами и другими сущностями Яндекс Трекер. Поддерживаются инструменты получения информации о задаче, проекте, портфеле и цели.

Реализованы следующие инструменты:
* получение связей задачи;
* создание задачи, комментария к задаче, цели;
* изменение статуса задачи, параметров задачи, параметров цели;
* массовое изменение задач, статусов задач, проектов, портфелей и целей;
* массовый перевод задач в другую очередь.

Чтобы получить доступ к Трекер, передайте MCP-серверу аутентификационные данные:
* Токен доступа в заголовке `token` с указанием префикса (`OAuth/Bearer`).
* Идентификатор организации или идентификатор [облачной организации](https://yandex.cloud/ru/docs/organization/concepts/organization) соответственно в заголовках `x-org-id` или `x-cloud-org-id`.

Подробнее о получении аутентификационных данных см. в [документации](https://yandex.ru/support/tracker/ru/concepts/access) Яндекс Трекер.

## Яндекс Поиск {#search-api}

MCP-сервер использует сервис [Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/concepts/index.html) и позволяет AI-агентам (таким как AI Studio, Claude или Cursor) использовать [API](https://yandex.cloud/ru/docs/search-api/api-ref/authentication) Яндекса для поиска в интернете и безопасно находить актуальную информацию.

Чтобы получить доступ к Yandex Search API, необходим [API-ключ](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key). Подробнее см. в [репозитории на GitHub](https://github.com/yandex/yandex-search-mcp-server).

## SourceCraft {#sourcecraft}

MCP-сервер для работы с платформой разработки [SourceCraft](https://sourcecraft.dev/portal/docs/ru) позволяет управлять задачами, комментариями и метками, работать с репозиториями, предложениями изменений и рецензентами.

Чтобы получить доступ к SourceCraft, необходимо передать заголовок с [персональным токеном](https://sourcecraft.dev/portal/docs/ru/sourcecraft/security/pat).

## См. также

* [MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/index.html)
* [Создать MCP-сервер в MCP Hub из шаблона](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/create-from-template.html)

---


# 7. API и интеграции


## 7.1 Особенности реализации API

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/api.html

[Yandex AI Studio](https://aistudio.yandex.ru/) предоставляет большой выбор API для создания различных приложений и решения бизнес-задач с помощью моделей искусственного интеллекта. Все API можно разделить на две группы:

* OpenAI-совместимые API, которые обеспечивают единый интерфейс для работы с моделями, текстовыми и голосовыми агентами, файлами и поиском.
* Специализированные API, разработанные в [Yandex Cloud](https://yandex.cloud/) для генерации текста и изображений, [классификации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/index.html), [дообучения моделей](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html) и [пакетной обработки](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/batch-processing.html).

## OpenAI-совместимые API

Выбирайте OpenAI-совместимые API для создания агентов, реализации RAG-сценариев и простых запросов к моделям.

| API | Технология | Описание |
| --- | --- | --- |
| [Models API](https://aistudio.yandex.ru/docs/ru/ai-studio/models/index.html) | REST | Получение списка доступных моделей и их идентификаторов |
| [Chat Completions API](https://aistudio.yandex.ru/docs/ru/ai-studio/chat/index.html) | REST | Генерация текста по промпту без управления диалогом |
| [Conversations API](https://aistudio.yandex.ru/docs/ru/ai-studio/conversations/index.html) | REST | Работа с историей диалога и контекстом |
| [Responses API](https://aistudio.yandex.ru/docs/ru/ai-studio/responses/index.html) | REST | Создание агентов. Позволяет генерировать текст, вызывать инструменты, получать структурированные ответы, реализовывать RAG-сценарии и создавать мультиагентные системы |
| [Realtime API](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/realtime.html) | WebSocket | Потоковая генерация текста и аудио с низкой задержкой для сценариев с голосовым входом |
| [Files API](https://aistudio.yandex.ru/docs/ru/ai-studio/files/index.html) | REST | Загрузка, хранение и работа с файлами для RAG-сценариев |
| [Embeddings API](https://aistudio.yandex.ru/docs/ru/ai-studio/embeddings/index.html) | REST | Получение эмбеддингов для семантических задач |
| [Vector stores API](https://aistudio.yandex.ru/docs/ru/ai-studio/vectorStores/index.html) | REST | Индексация данных и извлечение данных для RAG |

## Специализированные API Yandex Cloud

Используйте специализированные API AI Studio для работы с моделями YandexGPT Lite, YandexGPT Pro, YandexART, пакетной обработки, классификации текстов, дообучения моделей и управления MCP-серверами.

API Yandex Cloud спроектированы на основе механизма gRPC. Для описания методов и структур данных в API используется [Protocol Buffers (proto 3)](https://developers.google.com/protocol-buffers/docs/proto3).

В отличие от большинства API сервисов Yandex Cloud, API для работы с моделями не поддерживают ресурсно-ориентированный подход, так как не оперируют ресурсами. Запросы к моделям AI Studio не идемпотентны.

| API | Технология | Описание |
| --- | --- | --- |
| Text Generation API | [gRPC](https://aistudio.yandex.ru/docs/ru/ai-studio/text-generation/api-ref/grpc/index.html) [REST](https://aistudio.yandex.ru/docs/ru/ai-studio/text-generation/api-ref/index.html) | Генерация текстов по промпту, вызов функций, поддержка структурированного ответа |
| Image Generation API | [gRPC](https://aistudio.yandex.ru/docs/ru/ai-studio/image-generation/api-ref/grpc/index.html) [REST](https://aistudio.yandex.ru/docs/ru/ai-studio/image-generation/api-ref/index.html) | Генерация изображений по текстовому описанию |
| Batch Inference API | [gRPC](https://aistudio.yandex.ru/docs/ru/ai-studio/batch-inference/api-ref/grpc/index.html) | Асинхронная обработка большого количества запросов |
| Text Classification API | [gRPC](https://aistudio.yandex.ru/docs/ru/ai-studio/text-classification/api-ref/grpc/index.html) [REST](https://aistudio.yandex.ru/docs/ru/ai-studio/text-classification/api-ref/index.html) | Классификация, модерация, определение тематик |
| Embeddings API | [gRPC](https://aistudio.yandex.ru/docs/ru/ai-studio/embeddings/api-ref/grpc/index.html) [REST](https://aistudio.yandex.ru/docs/ru/ai-studio/embeddings/api-ref/index.html) | Векторное представление текста |
| Files API | [gRPC](https://aistudio.yandex.ru/docs/ru/ai-studio/files/api-ref/grpc/index.html) [REST](https://aistudio.yandex.ru/docs/ru/ai-studio/files/api-ref/index.html) | Загрузка и хранение файлов и данных |
| Dataset API | [gRPC](https://aistudio.yandex.ru/docs/ru/ai-studio/dataset/api-ref/grpc/index.html) | Управление датасетами для обучения |
| Tuning API | [gRPC](https://aistudio.yandex.ru/docs/ru/ai-studio/tuning/api-ref/grpc/index.html) | Дообучение моделей под предметную область |
| MCP Gateway API | [gRPC](https://aistudio.yandex.ru/docs/ru/ai-studio/mcp-gateway/api-ref/grpc/index.html) [REST](https://aistudio.yandex.ru/docs/ru/ai-studio/mcp-gateway/api-ref/index.html) | Создание, получение списка и удаление MCP-серверов |

## Читайте также

* [Документация gRPC](https://grpc.io/docs/)
* [Документация Protocol Buffers](https://developers.google.com/protocol-buffers/docs/proto3)
* [Концепции API Yandex Cloud](https://yandex.cloud/ru/docs/api-design-guide/concepts/general#resource-oriented-design)

---
**Навигация:**
* Предыдущая: [Удалить MCP-сервер](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/delete-server.html)
* Следующая: [Аутентификация в API](https://aistudio.yandex.ru/docs/ru/ai-studio/api-ref/authentication.html)

## 7.2 Аутентификация в API

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/api-ref/authentication.html

Для работы с API Yandex AI Studio необходимо выполнить аутентификацию. Доступны два основных способа в зависимости от типа используемого аккаунта.

---

## Способ 1: Аккаунт на Яндексе, федеративный или локальный аккаунт

1. Получите IAM-токен для [аккаунта на Яндексе](https://yandex.cloud/ru/docs/iam/operations/iam-token/create), [федеративного](https://yandex.cloud/ru/docs/iam/operations/iam-token/create-for-federation) или [локального](https://yandex.cloud/ru/docs/iam/operations/iam-token/create-for-local) аккаунта.
2. Получите [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id), на который у вашего аккаунта есть хотя бы минимальная роль для работы с нужной функциональностью:
    * `ai.languageModels.user` или выше — для работы с моделями генерации текста.
    * `ai.imageGeneration.user` или выше — для работы с YandexART.
    * `ai.assistants.editor` и `ai.languageModels.user` или выше — для работы с Responses API.
    * `ai.models.user` или выше — для работы с Realtime API.
    * `serverless.mcpGateways.editor` или выше — чтобы управлять MCP-серверами.

   Идентификатор каталога понадобится, чтобы получить URI модели.

3. При обращении к AI Studio через API в заголовке `Authorization` каждого запроса указывайте IAM-токен:

```http
Authorization: Bearer <IAM-токен>
```

---

## Способ 2: Сервисный аккаунт

Для работы с моделями AI Studio сервисный аккаунт должен иметь хотя бы минимальную соответствующую роль:
* `ai.languageModels.user` или выше — для работы с моделями генерации текста.
* `ai.imageGeneration.user` или выше — для работы с YandexART.
* `ai.assistants.editor` и `ai.languageModels.user` или выше — для работы с Responses API.
* `ai.models.user` или выше — для работы с Realtime API.
* `serverless.mcpGateways.editor` или выше — чтобы управлять MCP-серверами. API MCP Hub поддерживает только аутентификацию с IAM-токеном.

API AI Studio поддерживают два способа аутентификации с сервисным аккаунтом:

### С помощью IAM-токена
1. [Получите IAM-токен](https://yandex.cloud/ru/docs/iam/operations/iam-token/create-for-sa).
2. Полученный IAM-токен передавайте в заголовке `Authorization` в следующем формате:

```http
Authorization: Bearer <IAM-токен>
```

### С помощью API-ключей
Используйте [API-ключи](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key), если у вас нет возможности автоматически запрашивать [IAM-токен](https://yandex.cloud/ru/docs/iam/concepts/authorization/iam-token).
1. [Получите API-ключ](https://yandex.cloud/ru/docs/iam/operations/authentication/manage-api-keys#create-api-key).
2. Полученный API-ключ передавайте в заголовке `Authorization` в следующем формате:

```http
Authorization: Api-Key <API-ключ>
```

Идентификатор родительского каталога сервисного аккаунта понадобится, чтобы получить URI модели.

---

## Ссылки на другие страницы документации
* [Обзор API](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/api.html)
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
* [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
* [Публичные материалы](https://aistudio.yandex.ru/docs/ru/ai-studio/public-talks.html)
* [Термины и определения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html)
* [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)
* [Overview (Chat)](https://aistudio.yandex.ru/docs/ru/ai-studio/chat/index.html)

## 7.3 Заголовки для диагностики ошибок

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/api-ref/support-headers.html

Если у вас возникла ошибка при отправке запросов в API и вам нужна помощь, обратитесь в [техническую поддержку](https://yandex.cloud/ru/docs/support/overview). Техническая поддержка сможет быстрее решить вашу проблему, если вы будете использовать дополнительные заголовки HTTP-запросов и ответов.

## Заголовки запросов

При отправке HTTP-запросов используйте следующие заголовки:

*   `x-client-request-id` — уникальный идентификатор запроса. Рекомендуем использовать [UUID](https://ru.wikipedia.org/wiki/UUID). Сообщите этот идентификатор технической поддержке, чтобы мы смогли найти конкретный запрос в системе и помочь вам. Вы можете сгенерировать UUID [онлайн](https://uuid.js.org/) или воспользоваться библиотекой для используемого языка программирования.
*   `x-data-logging-enabled` — флаг, разрешающий сохранять данные, переданные пользователем в запросе. По умолчанию все запросы к AI Studio логируются. Вместе с указанием идентификатора запроса при обращении в техническую поддержку, логирование поможет решить вашу проблему. Вы можете [отключить](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/disable-logging.html) логирование, если в запросе необходимо передать чувствительную информацию.

## Примеры

Например, эти заголовки помогут найти ваш асинхронный запрос к модели:

### cURL

```bash
export FOLDER_ID=<идентификатор_каталога>
export IAM_TOKEN=<IAM-токен>
curl \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer ${IAM_TOKEN}" \
  --header "x-folder-id: ${FOLDER_ID}" \
  --data "@<путь_до_файла_json>" \
  "https://ai.api.cloud.yandex.net/foundationModels/v1/completionAsync"
```

Где:
*   `FOLDER_ID` — идентификатор каталога, на который у вашего аккаунта есть роль `ai.languageModels.user` или выше.
*   `IAM_TOKEN` — IAM-токен, полученный [перед началом работы](https://aistudio.yandex.ru/docs/ru/ai-studio/api-ref/support-headers.html#before-begin).

## Заголовки ответов

Каждый ответ сервера содержит заголовки, которые позволят получить еще больше информации о ходе выполнения запроса:

*   `x-request-id` — уникальный идентификатор ответа.
*   `x-server-trace-id` — уникальный идентификатор логов выполнения запроса.

Чтобы получить значения `x-request-id` и `x-server-trace-id`, ваше приложение должно логировать заголовки ответов сервера. Пример реализации доступа к заголовкам протокола [gRPC](https://yandex.cloud/ru/docs/glossary/grpc) приведен в [документации библиотеки grpc-go](https://github.com/grpc/grpc-go/blob/master/Documentation/grpc-metadata.md).

---
**Ссылки на другие страницы документации:**
*   [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
*   [Коды ошибок](https://aistudio.yandex.ru/docs/ru/ai-studio/troubleshooting/error-codes.html)
*   [Обзор технологий SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/overview.html)
*   [Отключить логирование запросов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/disable-logging.html)

## 7.4 Пошаговые инструкции

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/operations/index.html

На этой странице собраны ссылки на инструкции по работе с [Yandex AI Studio](https://aistudio.yandex.ru/).

## Инструкции по использованию API

*   [Переход с AI Assistant API на Responses API](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/assistant-responses-migration.html)

### Responses API

*   [Отправить базовый запрос с помощью Responses API](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/create-prompt.html)
*   [Отправить запрос в фоновом режиме с помощью Responses API](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/background-request.html)
*   [Управлять контекстом диалога](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/manage-context.html)
*   [Создать простого текстового агента с вызовом функции](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-function-text-agent.html)
*   [Создать текстового агента с поиском в интернете](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-websearch-text-agent.html)
*   [Создать текстового агента с поиском по файлам](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-filesearch-text-agent.html)
*   [Выполнить задачу с помощью Code Interpreter](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/use-code-interpreter.html)

### Realtime API

*   [Создать голосового агента через Realtime API на базе WebSocket](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-voice-agent.html)

### Completions API

*   [Отправить базовый запрос](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/completions-basic.html)
*   [Отправить запрос мультимодальной модели](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/multimodels-request.html)
*   [Отправить запрос с вызовом функций](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/completions-function.html)
*   [Отправить структурированный запрос](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/completions-structured.html)

### Models API

*   [Получить список моделей AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/models/get.html)

### Files API

*   [Создать агента с поиском по заранее созданным чанкам](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/create-prechunked-search-agent.html)

### Vector stores API

*   [Управлять поисковым индексом Vector Store](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/agents/manage-searchindex.html)

### Text Generation API

*   [Отправить запрос к инстансу](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/request-instance.html)
*   [Отправить асинхронный запрос](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/async-request.html)
*   [Вызвать функцию из модели](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/function-call.html)
*   [Запустить модель в пакетном режиме](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/batch/create.html)
*   [Оценить размер в токенах](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/evaluate-request.html)

### Embeddings API

*   [Использовать эмбеддинги в поиске по базе знаний](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/embeddings/search.html)

### Image Generation API

*   [Сгенерировать изображение с помощью YandexART](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/yandexart-request.html)

### Text Classification API

*   [Использовать классификаторы по промпту на базе YandexGPT](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/readymade.html)
*   [Использовать дообученные классификаторы на базе YandexGPT](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/additionally-trained.html)

### Tuning API

*   [Дообучить модель генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/create.html)
*   [Дообучить модель классификации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/tune-classifiers.html)
*   [Дообучить модель эмбеддингов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/create-embeddings.html)

### Dataset API

*   [Создать датасет](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-dataset.html)
*   [Создать датасет для дообучения модели генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-dataset-gpt.html)
*   [Создать датасет для дообучения модели классификации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-dataset-classifier.html)
*   [Удалить датасет](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/delete-dataset.html)

### MCP Gateway API

*   [Подключить внешний MCP-сервер к MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/connect-external-api.html)
*   [Создать MCP-сервер в MCP Hub с нуля](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/create-brand-new-api.html)
*   [Посмотреть информацию об MCP-сервере в MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/get-server-info-api.html)
*   [Удалить MCP-сервер из MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/delete-server-api.html)

---

## Инструкции по использованию интерфейса AI Studio

### Model Gallery

*   [Запустить модель в пакетном режиме](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/batch/create-ui.html)
*   [Сгенерировать изображение с помощью YandexART](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/yandexart-request-ui.html)
*   [Создать датасет](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-dataset-ui.html)
*   [Создать датасет для дообучения модели генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-dataset-gpt-ui.html)
*   [Создать датасет для дообучения модели классификации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-dataset-classifier-ui.html)
*   [Удалить датасет](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/delete-dataset-ui.html)
*   [Дообучить модель генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/create-ui.html)
*   [Дообучить модель классификации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/tune-classifiers-ui.html)
*   [Дообучить модель эмбеддингов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/tuning/create-embeddings-ui.html)
*   [Создать инстанс](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/create-instance.html)
*   [Получить информацию об инстансе](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/get-instance.html)
*   [Изменить инстанс](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/edit-instance.html)
*   [Клонировать инстанс](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/clone-instance.html)
*   [Остановить и запустить инстанс](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/start-stop-instance.html)
*   [Управлять метками инстанса](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/labels-instance.html)
*   [Удалить инстанс](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/resources/delete-instance.html)

### Agent Atelier

*   [Подключить внешний MCP-сервер к MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/connect-external.html)
*   [Создать MCP-сервер в MCP Hub из шаблона](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/create-from-template.html)
*   [Создать MCP-сервер в MCP Hub с нуля](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/create-brand-new.html)
*   [Посмотреть информацию об MCP-сервере в MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/get-server-info.html)
*   [Удалить MCP-сервер из MCP Hub](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/mcp-servers/delete-server.html)

## 7.5 Отключение логирования запросов

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/operations/disable-logging.html

По умолчанию модели сохраняют все данные запросов. Если в запросах вы передаете персональные или конфиденциальные данные либо другую чувствительную информацию, отключите логирование. Для этого добавьте в заголовок запроса REST или метаинформацию вызова gRPC опцию `x-data-logging-enabled: false`. Запросы, переданные с отключенной опцией логирования, не будут сохраняться на серверах Yandex Cloud.

Чтобы отключить логирование запросов:

---

## SDK

При инициализации объекта класса `AIStudio` в параметре `enable_server_data_logging` установите значение `False`. В этом случае Yandex AI Studio SDK будет добавлять опцию `x-data-logging-enabled: false` в метаинформацию каждого gRPC-вызова.

### Например:

```python
...
sdk = AIStudio(
    folder_id="<идентификатор_каталога>",
    auth="<API-ключ>",
    enable_server_data_logging=False,
)
...
```

**Где:**

* `<идентификатор_каталога>` — [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id), в котором создан [сервисный аккаунт](https://yandex.cloud/ru/docs/iam/concepts/users/service-accounts).
* `<API-ключ>` — [API-ключ](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key) сервисного аккаунта, необходимый для [аутентификации в API](https://aistudio.yandex.ru/docs/ru/ai-studio/api-ref/authentication.html). Вы также можете использовать другие варианты аутентификации. Подробнее см. в разделе [Аутентификация в Yandex AI Studio SDK](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk/index.html#authentication).

---

## cURL

> **Примечание**
> Чтобы воспользоваться примерами, установите cURL.
> Пример ниже разработан для выполнения в операционных системах MacOS и Linux. Чтобы выполнить его в системе Windows, ознакомьтесь с особенностями работы с Bash в Microsoft Windows.

Добавьте к REST-запросу заголовок `x-data-logging-enabled: false`. Например:

```bash
export FOLDER_ID=<идентификатор_каталога>
export IAM_TOKEN=<IAM-токен>

curl \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer ${IAM_TOKEN}" \
  --header "x-data-logging-enabled: false" \
  --header "x-folder-id: ${FOLDER_ID}" \
  --data "@<путь_до_файла_json>" \
  "<эндпоинт_модели>"
```

**Где:**

* `FOLDER_ID` — идентификатор каталога, на который у вашего аккаунта есть необходимые права.
* `IAM_TOKEN` — IAM-токен, необходимый для аутентификации.

---

## OpenAI API

```python
from openai import OpenAI

client = OpenAI(
    api_key="<API-ключ>",
    base_url="https://ai.api.cloud.yandex.net/v1",
    project="<идентификатор_каталога>",
    default_headers={
        "x-data-logging-enabled": "false"
    }
)

completion = client.chat.completions.create(
    model=f"<URI_модели>",
    ...
)
...
```

**Где:**

* `<API-ключ>` — [API-ключ](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key) сервисного аккаунта, необходимый для аутентификации в OpenAI API. Вы также можете использовать [IAM-токен](https://yandex.cloud/ru/docs/iam/operations/iam-token/create).
* `<идентификатор_каталога>` — [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id), в котором создан [сервисный аккаунт](https://yandex.cloud/ru/docs/iam/concepts/users/service-accounts).
* `<URI_модели>` — уникальный идентификатор модели из [списка моделей](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html), доступных для работы в синхронном режиме. Содержит [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id), в котором создан [сервисный аккаунт](https://yandex.cloud/ru/docs/iam/concepts/users/service-accounts).

---

## Ссылки на другие страницы документации

### AI Studio
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
* [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
* [Публичные материалы](https://aistudio.yandex.ru/docs/ru/ai-studio/public-talks.html)
* [Термины и определения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html)
* [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)
* [Получить API-ключ](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/get-api-key.html)
* [Квоты и лимиты AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html)
* [Тарифы AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html)
* [История изменений AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/release-notes/index.html)

### SpeechKit
* [Обзор технологий SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/overview.html)
* [Поддерживаемые форматы аудио](https://aistudio.yandex.ru/docs/ru/speechkit/formats.html)
* [Интеграция телефонии](https://aistudio.yandex.ru/docs/ru/speechkit/concepts/ivr-integration.html)
* [Квоты и лимиты SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/concepts/limits.html)
* [Тарифы SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/pricing.html)
* [История изменений SpeechKit: распознавание](https://aistudio.yandex.ru/docs/ru/speechkit/release-notes-stt.html)
* [История изменений SpeechKit: синтез](https://aistudio.yandex.ru/docs/ru/speechkit/release-notes-tts.html)

### Yandex Search API
* [О сервисе Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/concepts/index.html)
* [Начало работы](https://aistudio.yandex.ru/docs/ru/search-api/quickstart/index.html)
* [Квоты и лимиты Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/concepts/limits.html)
* [Тарифы Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/pricing.html)
* [История изменений Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/release-notes/index.html)

### Vision OCR
* [О сервисе Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/concepts/ocr/index.html)
* [Начало работы](https://aistudio.yandex.ru/docs/ru/vision/quickstart.html)
* [Вопросы и ответы Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/qa/index.html)
* [Квоты и лимиты Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/concepts/limits.html)
* [Тарифы Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/pricing.html)
* [История изменений Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/release-notes.html)

### Translate
* [О сервисе Translate](https://aistudio.yandex.ru/docs/ru/translate/concepts/index.html)
* [Начало работы](https://aistudio.yandex.ru/docs/ru/translate/quickstart.html)
* [Квоты и лимиты Translate](https://aistudio.yandex.ru/docs/ru/translate/concepts/limits.html)
* [Тарифы Translate](https://aistudio.yandex.ru/docs/ru/translate/pricing.html)

### Навигация
* Предыдущая: [Получить API-ключ](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/get-api-key.html)
* Следующая: [Обзор (Guardrails)](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html)

## 7.6 Переход с AI Assistant API на Responses API

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/assistant-responses-migration.html

AI Assistant API позволял создавать AI-ассистентов, которые хранили контекст взаимодействия с пользователем в тредах, могли использовать инструменты Retrieval и WebSearch, а также получать промежуточные ответы модели.

Для новых и текущих проектов мы рекомендуем использовать Responses API — простой и гибкий интерфейс, который позволяет сохранять контекст диалога. Responses API предоставляет [встроенные инструменты](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/index.html#tools) поиска по файлам и поиска в интернете, позволяет использовать собственные функции, вызывать внешние инструменты через MCP-серверы и обеспечивает высокую производительность.

> **Важно**
> С 10 декабря 2025 года функциональность AI Assistant API в Yandex AI Studio перестанет поддерживаться и будет полностью отключена 26 января 2026 года. Переведите все свои актуальные проекты на Responses API до 26 января 2026 года.

С помощью этого руководства вы сможете преобразовать существующих AI-ассистентов, построенных на основе AI Assistant API, в AI-агентов на базе Responses API.

[AI-агент](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/index.html) в Responses API — это экземпляр модели с заданной конфигурацией: инструкцией, настроенными инструментами и контекстом взаимодействия. AI-агент определяет поведение модели и способ ее взаимодействия с пользователем и другими системами.

## Различия между AI Assistant API и Responses API {#differences}

Понятия и инструменты, использующиеся в AI Assistant API и Responses API, различаются:

| AI Assistant API | Responses API |
| --- | --- |
| **Assistant** — AI-ассистент как ресурс сервиса. | При работе через API отдельный ресурс не создается, все настройки передаются непосредственно в методе `responses.create()`. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) конфигурацию AI-агента можно сохранить с уникальным идентификатором и затем использовать в Responses API. |
| **Thread** — тред диалога. | Не существует тредов, содержащих контекст всех сообщений. Историю переписки можно передавать как контекст в поле `previous_response_id`. |
| **Run** — запуск AI-ассистента для треда. | Объект `response` — результат выполнения метода `responses.create()`. Каждый объект `response` — это аналог запуска (`Run`) AI Assistant API, в котором содержится готовый ответ. |
| **Retrieval** — инструмент поиска по поисковым индексам. | [Встроенный инструмент](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/filesearch.html) `file_search` для поиска по файлам. Для поиска необходимо указать массив индексов Vector Store. |
| **WebSearch** — инструмент поиска в интернете. | [Встроенный инструмент](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/tools/websearch.html) `web_search` для поиска в интернете. Можно указать домен и регион поиска. |
| **Streaming** — получение промежуточных ответов модели. | Метод `client.responses.stream()`. |

## Концептуальные различия {#basic-differences}

Основные концептуальные отличия Responses API и AI Assistant API:

1. **В Responses API не существует ассистентов как отдельных ресурсов сервиса AI Studio.**

| AI Assistant API | Responses API |
| --- | --- |
| В AI Assistant API необходимо создать AI-ассистента один раз. После этого его можно запускать в разных тредах. | В Responses API для каждого запроса необходимо указывать: модель `model`; инструкции `instructions`; используемые инструменты `tools`; параметры модели (`temperature`, `max_output_tokens` и т.д.) |

Для адаптации вашего кода на Responses API воспользуйтесь одним из двух вариантов сохранения настроек модели:
* Вынесите конфигурацию AI-ассистента из AI Assistant API в код вашего приложения.
* В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) в разделе **Agent Atelier** задайте и сохраните конфигурацию модели. После этого вы сможете использовать ее в коде вашего приложения, указывая идентификатор сохраненного агента.

2. **Контекст передается не в тредах, а в сообщениях в поле `previous_response_id`.**

| AI Assistant API | Responses API |
| --- | --- |
| В AI Assistant API контекст хранится в тредах (`thread`), и каждый запуск (`run`) перечитывает его. | В Responses API реализован механизм, который позволяет передать идентификатор предыдущего сообщения в поле `previous_response_id`, чтобы учитывать историю сообщений. |

> **Примечание**
> Срок хранения сообщений ограничен и составляет 30 дней с момента их создания методом `responses.create()`.

3. **Инструменты встроены в Responses API и не требуют подключения дополнительных библиотек.**

| AI Assistant API | Responses API |
| --- | --- |
| `Retrieval` и `WebSearch` в AI Assistant API настраиваются глобально как инструменты ассистента и используют внешние источники и отдельные поисковые индексы. | В Responses API сценарии поиска по файлам и поиска в интернете реализованы через поле `tools`, которое позволяет задавать разный набор инструментов для каждого запроса. Доступны следующие значения поля:<br>• `{"type": "file_search"}`<br>• `{"type": "web_search"}` |

## Как перенести простого текстового ассистента на Responses API {#migrate-simple-assistant}

### Схема работы AI-ассистента через AI Assistant API {#simple-assistant-api}

Работа с ассистентом в AI Assistant API состоит из следующих этапов:
1. Создание AI-ассистента, в котором хранятся настройки модели, инструменты и базовые инструкции.
2. Создание треда (контейнера для диалога).
3. Создание сообщения в треде (сообщение пользователя).
4. Запуск ассистента для обработки треда.
5. Опрос состояния запуска, чтобы дождаться завершения его выполнения.
6. Получение сообщения из треда (ответ модели).

### Схема работы с AI-агентом через Responses API {#simple-responses-api}

В Responses API AI-агент — это набор параметров в коде, а контекст предыдущего диалога передается через поле `previous_response_id`.

Логика вашего приложения должна сохранять идентификатор `response.id` как аналог треда в AI Assistant API. Чтобы получить ответ с учетом истории переписки, передавайте идентификатор последнего сообщения `response.id` в поле `previous_response_id` с каждым последующим сообщением пользователя.

#### Пример работы простого текстового AI-агента на Responses API:

**Python SDK**

```python
from openai import OpenAI

YANDEX_CLOUD_FOLDER = "<идентификатор_каталога>"
YANDEX_CLOUD_MODEL = "<URI_модели>"
YANDEX_CLOUD_API_KEY = "<API-ключ_сервисного_аккаунта>"
# или YANDEX_CLOUD_IAM_TOKEN = "<IAM-токен>"

previous_id = None # храним ID последнего ответа ассистента

client = OpenAI(
    api_key=YANDEX_CLOUD_API_KEY,
    project=YANDEX_CLOUD_FOLDER,
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
)

print("Чат с агентом (для выхода введите 'выход')\n")

while True:
    user_input = input("Вы: ")
    if user_input.lower() in ("exit", "quit", "выход"):
        print("Чат завершен.")
        break

    response = client.responses.create(
        model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
        input=[{"role": "user", "content": user_input}],
        instructions="Ты - текстовый агент, который ведет диалог и дает информативные ответы на вопросы пользователя.",
        previous_response_id=previous_id, # передаем контекст, если он есть
    )

    # сохраняем ID для следующего шага
    previous_id = response.id

    # выводим ответ агента
    print("Агент:", response.output_text)
```

## Как перенести на Responses API ассистента с инструментами {#migrate-tooled-assistant}

Процесс переноса AI-ассистента на Responses API зависит от подключенных инструментов и режима получения результатов генерации.

### Сценарии RAG с Retrieval {#rag-tools}

В сценариях поиска по файлам и внутренним базам знаний используются поисковые индексы AI Assistant API и инструмент `Retrieval`. AI-ассистент генерирует ответы на основе загруженных в индексы документов и возвращает метаданные использованных файлов.

В AI Assistant API инструмент `Retrieval` был привязан к ассистенту:

**SDK**

```python
# Сначала создается инструмент для работы с существующим поисковым индексом.
tool = sdk.tools.search_index(
    search_index,
    call_strategy={
        "type": "function",
        "function": {"name": "guide", "instruction": instruction},
    },
)

# Затем создается ассистент, использующий этот инструмент.
assistant = sdk.assistants.create(
    "yandexgpt",
    instruction="Ты — помощник по внутренней документации компании. Отвечай вежливо. Если информация не содержится...",
    tools=[tool],
)

thread = sdk.threads.create()
```

Чтобы перенести AI-ассистента с подключенным инструментом `Retrieval`, выполните следующие действия:
1. Все документы подключенного поискового индекса загрузите в [векторное хранилище](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore.html), с которым работает Responses API.
2. При формировании запроса в вашем приложении добавляйте настройки инструмента `file_search`:

**Python SDK**

```python
import openai
import json

YANDEX_CLOUD_FOLDER = "<идентификатор_каталога>"
YANDEX_CLOUD_MODEL = "<URI_модели>"
VECTOR_STORE_ID = "<идентификатор_хранилища_Vector_Store>"
YANDEX_CLOUD_API_KEY = "<API-ключ_сервисного_аккаунта>"
# или YANDEX_CLOUD_IAM_TOKEN = "<IAM-токен>"

client = openai.OpenAI(
    api_key=YANDEX_CLOUD_API_KEY,
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
    project=YANDEX_CLOUD_FOLDER,
)

response = client.responses.create(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    instructions="Ты - умный ассистент. Если спрашивают про ... - ищи в подключенном индексе",
    tools=[
        {
            "type": "file_search",
            "vector_store_ids": [VECTOR_STORE_ID],
        }
    ],
    input="что такое ...",
)

print("Текст ответа:")
print(response.output_text)
print("\n" + "=" * 50 + "\n")

# Полный ответ
print("Полный ответ (JSON):")
print(json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
```

### Сценарии с поиском в интернете {#websearch-tool}

В AI Assistant API настройки инструмента `WebSearch` задавались при создании AI-ассистента:

**cURL**

```json
{
  "folderId": "<идентификатор_каталога>",
  "modelUri": "gpt://<идентификатор_каталога>/yandexgpt-lite/latest",
  "instruction": "Ты - умный помощник финансовой компании. Отвечай вежливо. Для ответов на вопросы воспользуйся поиском в интернете.",
  "tools": [
    {
      "genSearch": {
        "options": {
          "site": {
            "site": [
              "https://cbr.ru/",
              "https://yandex.ru/finance/currencies"
            ]
          },
          "enableNrfmDocs": true
        },
        "description": "Инструмент для получения информации об официальных курсах валют."
      }
    }
  ]
}
```

В Responses API параметры инструмента `web_search` передаются непосредственно в запросе.

Чтобы перенести AI-ассистента с инструментом `WebSearch`, в запросе передавайте настройки инструмента `web_search`:

**Python SDK**

```python
import openai
import json

YANDEX_CLOUD_FOLDER = "<идентификатор_каталога>"
YANDEX_CLOUD_MODEL = "<URI_модели>"
YANDEX_CLOUD_API_KEY = "<API-ключ_сервисного_аккаунта>"
# или YANDEX_CLOUD_IAM_TOKEN = "<IAM-токен>"

client = openai.OpenAI(
    api_key=YANDEX_CLOUD_API_KEY,
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
    project=YANDEX_CLOUD_FOLDER,
)

response = client.responses.create(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    input="Сделай краткий обзор последних новостей об LLM в 2025 году - только факты, без домыслов.",
    # Передаем настройки инструментов
    tools=[
        {
            "type": "web_search",
            "filters": {
                "allowed_domains": [
                    "habr.ru",
                ],
                "user_location": {
                    "region": "213",
                }
            }
        }
    ],
    temperature=0.3,
    max_output_tokens=1000,
)
```

### Получение промежуточных результатов генерации ответа {#streaming}

AI Assistant API позволял получать промежуточные результаты генерации ответа. Например, в (AI SDK) использовался метод `run_stream()`:

**SDK**

```python
run = assistant.run_stream(thread)

# Промежуточные результаты по мере генерации моделью ответа
for event in run:
    print(event._message.parts)

# Все поля окончательного результата
print(f"{event=}")
```

Responses API также позволяет получать промежуточные результаты генерации, например, с помощью метода `responses.stream()`:

**Python SDK**

```python
import openai

YANDEX_CLOUD_FOLDER = "<идентификатор_каталога>"
YANDEX_CLOUD_MODEL = "<URI_модели>"
YANDEX_CLOUD_API_KEY = "<API-ключ_сервисного_аккаунта>"
# или YANDEX_CLOUD_IAM_TOKEN = "<IAM-токен>"

client = openai.OpenAI(
    api_key=YANDEX_CLOUD_API_KEY,
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
    project=YANDEX_CLOUD_FOLDER,
)

# Создаем стриминговый запрос
with client.responses.stream(
    model=f"gpt://{YANDEX_CLOUD_FOLDER}/{YANDEX_CLOUD_MODEL}",
    input="Напиши короткий тост на день рождения, дружелюбный и смешной.",
) as stream:
    for event in stream:
        # Дельты текстового ответа
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
        # Событие, показывающее, что ответ завершен
        # elif event.type == "response.completed":
        #     print("\n---\nОтвет завершен")

# Если необходимо, можно забрать текст ответа целиком
# final_response = stream.get_final_response()
# print("\nПолный текст ответа:\n", final_response.output_text)
```

---


# 8. Yandex AI Studio SDK


## 8.1 Обзор SDK

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/sdk/index.html

Yandex AI Studio предоставляет библиотеку инструментов и примеров готового кода для разработки продуктов на языке Python — Yandex AI Studio SDK. AI SDK обеспечивает стандартизированный способ взаимодействия с фундаментальными моделями и упрощает интеграцию с другими сервисами Yandex Cloud.

Библиотека AI SDK реализует синхронный и асинхронный интерфейсы Python на основе gRPC-вызовов API сервисов AI Studio. В AI SDK доступны следующие возможности:

* [генерация текста и изображений](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html) с помощью всех поддерживаемых [моделей](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models.html);
* работа с [эмбеддингами](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html);
* работа с [классификаторами на базе YandexGPT](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/index.html);
* [дообучение](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/index.html) моделей генерации текста и классификаторов;
* интеграция с [LangChain](https://www.langchain.com/).

Полный перечень поддерживаемых функций, исходный код библиотеки и примеры использования доступны на [GitHub](https://github.com/yandex-cloud/yandex-ai-studio-sdk).

## Установка {#install}

Установить библиотеку AI SDK можно с помощью менеджера пакетов [pip](https://pip.pypa.io/en/stable/):

```bash
pip install yandex-ai-studio-sdk
```

## Аутентификация в Yandex AI Studio SDK {#authentication}

Аутентификация в Yandex AI Studio SDK выполняется путем передачи в модель объекта `AIStudio`, который содержит поля:

* `folder_id` — [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id), в котором вы будете работать с моделями.
* `auth` — ключ, токен или другие данные для аутентификации, позволяющие идентифицировать субъекта.

Значение поля `auth` может быть задано явно или получено автоматически из окружения.

### Значение задано явно

Заданное явно значение поля `auth` может принимать одно из значений:

* `string` — в форме строки можно передать:
    * [IAM-токен](https://yandex.cloud/ru/docs/iam/concepts/authorization/iam-token) пользовательского или [сервисного аккаунта](https://yandex.cloud/ru/docs/iam/concepts/users/service-accounts);
    * секретную часть [API-ключа](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key) сервисного аккаунта;
    * [OAuth-токен](https://yandex.cloud/ru/docs/iam/concepts/authorization/oauth-token) пользовательского аккаунта.
    SDK автоматически определит тип аутентификационных данных.
* Объект одного из следующих [классов](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk-ref/auth.html#authentication-methods-classes):
    * [APIKeyAuth](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk-ref/auth.html#yandex_ai_studio_sdk.auth.APIKeyAuth) — позволяет явно задать аутентификацию по передаваемому API-ключу.
      Например: `auth = APIKeyAuth('<api_ключ>')`.
    * [EnvIAMTokenAuth](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk-ref/auth.html#yandex_ai_studio_sdk.auth.EnvIAMTokenAuth) — позволяет явно задать аутентификацию по IAM-токену, заданному в переменной окружения `YC_TOKEN` или любой другой.
      Например: `auth = EnvIAMTokenAuth()` или `auth = EnvIAMTokenAuth("env_var")`.
      SDK при каждом запросе заново получает IAM-токен из этой переменной окружения, поэтому вы можете вне SDK самостоятельно периодически обновлять IAM-токен в переменной окружения. Этот вариант аутентификации является оптимальным для использования с [сервисным агентом](https://yandex.cloud/ru/docs/datasphere/operations/community/create-ssa) в Yandex DataSphere, если для этого сервиса включен [доступ](https://yandex.cloud/ru/docs/iam/concepts/service-control) к другим ресурсам в облаке пользователя.
    * [IAMTokenAuth](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk-ref/auth.html#yandex_ai_studio_sdk.auth.IAMTokenAuth) — позволяет явно задать аутентификацию по передаваемому IAM-токену.
      Например: `auth = IAMTokenAuth('<iam_токен>')`.
    * [MetadataAuth](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk-ref/auth.html#yandex_ai_studio_sdk.auth.MetadataAuth) — позволяет явно задать аутентификацию от имени сервисного аккаунта, заданного в [метаданных](https://yandex.cloud/ru/docs/compute/concepts/vm-metadata) виртуальной машины Yandex Compute Cloud.
      Например: `auth = MetadataAuth()`.
    * [NoAuth](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk-ref/auth.html#yandex_ai_studio_sdk.auth.NoAuth) — позволяет указать, что аутентификационные данные не будут передаваться.
      Например: `auth = NoAuth()`.
    * [OAuthTokenAuth](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk-ref/auth.html#yandex_ai_studio_sdk.auth.OAuthTokenAuth) — позволяет явно задать аутентификацию по передаваемому OAuth-токену.
      Например: `auth = OAuthTokenAuth('<oauth_токен>')`.
    * [YandexCloudCLIAuth](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk-ref/auth.html#yandex_ai_studio_sdk.auth.YandexCloudCLIAuth) — позволяет явно задать аутентификацию от имени [пользователя](https://yandex.cloud/ru/docs/iam/concepts/users/accounts) или сервисного аккаунта, [заданного](https://yandex.cloud/ru/docs/cli/operations/index#auth) в профиле Yandex Cloud CLI на компьютере пользователя.
      Например: `auth = YandexCloudCLIAuth()`.

Эти классы вы можете получить, импортировав из библиотеки AI Studio SDK. Например:
```python
from yandex_ai_studio_sdk.auth import APIKeyAuth
```

> **Примечание**
> [Время жизни](https://yandex.cloud/ru/docs/iam/concepts/authorization/iam-token#lifetime) IAM-токена — не более 12 часов. Учитывайте это, выполняя запросы с аутентификацией по IAM-токену, заданному в строке, объекте класса `IAMTokenAuth` или переменной окружения `YC_TOKEN`.

### Значение получено из окружения

Если поле `auth` явно не задано, то SDK автоматически попытается выбрать один из вариантов аутентификации в следующем порядке:

1. Если задана переменная окружения `YC_API_KEY`, для аутентификации будет использован указанный в ней API-ключ.
2. Если задана переменная окружения `YC_IAM_TOKEN`, для аутентификации будет использован указанный в ней IAM-токен.
3. Если задана переменная окружения `YC_OAUTH_TOKEN`, для аутентификации будет использован переданный в ней OAuth-токен.
4. Если такие переменные окружения не заданы, SDK попытается выполнить аутентификацию по IAM-токену сервисного аккаунта, заданного в метаданных виртуальной машины.
5. Если задана переменная окружения `YC_TOKEN`, для аутентификации будет использован указанный в ней IAM-токен.
   SDK при каждом запросе заново получает IAM-токен из этой переменной окружения, поэтому вы можете вне SDK самостоятельно периодически обновлять IAM-токен в переменной окружения `YC_TOKEN`.
6. Если предыдущие варианты не сработали, SDK попытается выполнить аутентификацию от имени пользователя или сервисного аккаунта, заданного в профиле Yandex Cloud CLI на компьютере пользователя.

## Использование {#usage}

В качестве входных данных для запроса AI SDK может принимать:

* Строку. Например: `"Что такое небо?"`.
* Словарь — структуру данных, аналогичную [JSON](https://ru.wikipedia.org/wiki/JSON). Например: `{"role": "role", "text": "text"}`.
* Объект [класса](https://github.com/yandex-cloud/yandex-ai-studio-sdk/blob/master/src/yandex_ai_studio_sdk/_models/completions/message.py) `TextMessage` AI SDK. Например: `result[0]`.
  Объект `result` класса `TextMessage` представляет собой массив альтернатив, содержащихся в ответах модели. С помощью такого объекта можно передать предыдущий ответ модели в последующем запросе.
* Массив, содержащий любое сочетание указанных выше типов данных. Например: `["text", {"role": "role", "text": "text"}]`.

Пример ниже отправит в модель YandexGPT Pro запрос c промптом в форме строки «Что такое небо?».

```python
from yandex_ai_studio_sdk import AIStudio

sdk = AIStudio(
    folder_id="<идентификатор_каталога>",
    auth="<аутентификационные_данные>",
)

model = sdk.models.completions("yandexgpt")
model = model.configure(temperature=0.5)
result = model.run("Что такое небо?")

print(f'{result=}')
print(f'{result[0]=}')
print(f'{result.alternatives[0].role=}')
print(f'{result.alternatives[0].text=}')
print(f'{result.alternatives[0].status=}')
```

Где:
* `folder_id` — [идентификатор каталога](https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id), в котором создан [сервисный аккаунт](https://yandex.cloud/ru/docs/iam/concepts/users/service-accounts).
* `auth` — ключ, токен или другие данные для [аутентификации](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk/index.html#authentication), позволяющие идентифицировать субъекта.

Результат:
1. Переменная `result` содержит массив альтернатив, содержащихся в ответах модели:
   `GPTModelResult(alternatives=(Alternative(role='assistant', text='Небо — это пространство над поверхностью Земли или другой планеты...', status=<AlternativeStatus.FINAL: 3>),), usage=Usage(input_tokens=10, completion_tokens=49, total_tokens=59), model_version='18.01.2024')`
2. Элемент массива `result[0]` содержит объект [класса](https://github.com/yandex-cloud/yandex-ai-studio-sdk/blob/master/src/yandex_ai_studio_sdk/_models/completions/message.py) `TextMessage` AI SDK, который в свою очередь содержит поля `role`, `text` и `status`:
   `Alternative(role='assistant', text='Небо — это пространство над поверхностью Земли или другой планеты...', status=<AlternativeStatus.FINAL: 3>)`
3. Поле `result.alternatives[0].role` содержит одно из значений роли отправителя сообщения:
    * `user` — предназначена для отправки пользовательских сообщений к модели.
    * `system` — позволяет задать контекст запроса и определить поведение модели.
    * `assistant` — используется для ответов, которые генерирует модель.
4. Поле `result.alternatives[0].text` содержит текст сообщения:
   `Небо — это пространство над поверхностью Земли или другой планеты, которое мы видим, когда смотрим вверх...`
5. Поле `result.alternatives[0].status` содержит статус сообщения. Возможные значения статуса:
    * `UNSPECIFIED` — статус не определен.
    * `PARTIAL` — часть сгенерированного текста, который может измениться в ходе дальнейшей генерации.
    * `TRUNCATED_FINAL` — итоговый сгенерированный текст, но результат превышает установленные ограничения.
    * `FINAL` — итоговый сгенерированный текст в пределах установленных ограничения.
    * `CONTENT_FILTER` — генерация остановлена из-за наличия конфиденциальных данных или этически ненадлежащих тем в промпте или сгенерированном тексте.

Дополнительные примеры использования AI SDK см. в [пошаговых инструкциях для Yandex AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/index.html).

## 8.2 Миграция с Yandex Cloud ML SDK

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/operations/sdk-migration.html

В недавнем [релизе](https://aistudio.yandex.ru/docs/ru/ai-studio/release-notes/index.html#270126) Yandex Cloud ML SDK был переименован в Yandex AI Studio SDK. Чтобы продолжать пользоваться всеми функциями библиотеки, перейдите на AI SDK.

### Политика управления версиями:
* `yandex-cloud-ml-sdk 0.18` — последняя настоящая версия ML SDK в PyPI;
* `yandex-cloud-ml-sdk 0.19.0` — оболочка, которая перенаправляет запросы на `yandex-ai-studio-sdk`;
* `yandex-ai-studio-sdk 0.19.0` — первая версия AI SDK.

### Чтобы перейти на AI SDK:

1. **Обновите библиотеку:**

```bash
pip install --upgrade yandex-cloud-ml-sdk
```

2. **Измените названия пакетов и классов, выполнив команды в директории вашего проекта:**

```bash
grep -rl 'YCloudML' . | xargs sed -i 's/YCloudML/AIStudio/g'
grep -rl 'yandex-cloud-ml-sdk' . | xargs sed -i 's/yandex-cloud-ml-sdk/yandex-ai-studio-sdk/g'
grep -rl 'yandex_cloud_ml_sdk' . | xargs sed -i 's/yandex_cloud_ml_sdk/yandex_ai_studio_sdk/g'
```

## Была ли статья полезна?

---

### Ссылки на другие страницы документации:
* **Навигация:**
    * Предыдущая: [О Yandex AI Studio SDK](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk/index.html)
    * Следующая: [Overview](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk-ref/index.html)
* **Разделы AI Studio:**
    * [Документация AI Studio](https://aistudio.yandex.ru/docs/ru/index.html)
    * [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
    * [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
    * [Публичные материалы](https://aistudio.yandex.ru/docs/ru/ai-studio/public-talks.html)
    * [Термины и определения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html)
    * [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)
    * [Квоты и лимиты (AI Studio)](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html)
    * [Правила тарификации (AI Studio)](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html)
* **Другие сервисы:**
    * [Обзор технологий SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/overview.html)
    * [О сервисе Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/concepts/index.html)
    * [О сервисе Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/concepts/ocr/index.html)
    * [О сервисе Translate](https://aistudio.yandex.ru/docs/ru/translate/concepts/index.html)

---


# 9. Безопасность


## 9.1 Управление доступом

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html

Все операции в Yandex AI Studio проверяются в сервисе [Yandex Identity and Access Management](https://yandex.cloud/ru/docs/iam/). Если у субъекта нет необходимых разрешений, сервис вернет ошибку.

Чтобы выдать разрешения к ресурсу, [назначьте роли](https://yandex.cloud/ru/docs/iam/operations/roles/grant) на этот ресурс субъекту, который будет выполнять операции. Роли можно назначить [аккаунту на Яндексе](https://yandex.cloud/ru/docs/iam/concepts/users/accounts#passport), [сервисному аккаунту](https://yandex.cloud/ru/docs/iam/concepts/users/service-accounts), [локальному пользователю](https://yandex.cloud/ru/docs/iam/concepts/users/accounts#local), [федеративному пользователю](https://yandex.cloud/ru/docs/iam/concepts/federations), [группе пользователей](https://yandex.cloud/ru/docs/organization/operations/manage-groups), [системной группе](https://yandex.cloud/ru/docs/iam/concepts/access-control/system-group) или [публичной группе](https://yandex.cloud/ru/docs/iam/concepts/access-control/public-group). Подробнее читайте в разделе [Как устроено управление доступом в Yandex Cloud](https://yandex.cloud/ru/docs/iam/concepts/access-control/).

## На какие ресурсы можно назначить роль

Роль можно назначить на [организацию](https://yandex.cloud/ru/docs/organization/concepts/organization), [облако](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#cloud) и [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder). Роли, назначенные на организацию, облако или каталог, действуют и на вложенные ресурсы.

## Какие роли действуют в сервисе

### Сервисные роли

#### ai.playground.user
Роль позволяет использовать AI Playground в консоли управления Yandex Cloud, а также получать список всех доступных моделей.

#### ai.languageModels.user
Роль позволяет использовать модели [генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models), [векторного представления текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings#yandexgpt-embeddings) и [классификаторов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/models) в сервисе Yandex AI Studio, а также просматривать информацию об [облаке](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#cloud), [каталоге](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder) и [квотах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits#yandexgpt-quotas) сервиса.

#### ai.imageGeneration.user
Роль позволяет использовать модели генерации изображений YandexART в сервисе Yandex AI Studio, а также просматривать информацию об [облаке](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#cloud), [каталоге](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder) и [квотах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits#yandexgpt-quotas) сервиса.

#### ai.assistants.auditor
Роль позволяет просматривать информацию о загруженных [файлах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore#file-uploading) и [поисковых индексах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore) Vector Store, а также о [квотах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits#yandexgpt-quotas) сервиса Yandex AI Studio, об [облаке](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#cloud) и [каталоге](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder).

#### ai.assistants.viewer
Роль позволяет просматривать информацию о файлах и поисковых индексах Vector Store, а также выполнять поиск по таким индексам.
Пользователи с этой ролью могут:
* просматривать информацию о загруженных [файлах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore#file-uploading) и содержимое таких файлов;
* просматривать информацию о [поисковых индексах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore) Vector Store, а также выполнять поиск по таким индексам;
* просматривать информацию о [квотах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits#yandexgpt-quotas) сервиса Yandex AI Studio;
* просматривать информацию об [облаке](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#cloud);
* просматривать информацию о [каталоге](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder).
Включает разрешения, предоставляемые ролью `ai.assistants.auditor`.

#### ai.assistants.editor
Роль позволяет использовать AI-агентов, а также управлять файлами и поисковыми индексами Vector Store.
Пользователи с этой ролью могут:
* использовать [AI-агентов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/);
* просматривать информацию о загруженных [файлах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore#file-uploading), а также загружать, изменять, просматривать и удалять такие файлы;
* просматривать информацию о [поисковых индексах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore) Vector Store, создавать, изменять и удалять поисковые индексы, а также выполнять поиск по ним;
* просматривать информацию о [квотах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits#yandexgpt-quotas) сервиса Yandex AI Studio;
* просматривать информацию об [облаке](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#cloud);
* просматривать информацию о [каталоге](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder).
Включает разрешения, предоставляемые ролью `ai.assistants.viewer`.

#### ai.assistants.admin
Роль позволяет использовать AI-агентов, а также управлять файлами и поисковыми индексами Vector Store. (Аналогично editor в рамках описания возможностей в этой статье).
Включает разрешения, предоставляемые ролью `ai.assistants.editor`.

#### ai.datasets.auditor
Роль позволяет просматривать метаданные [датасетов](https://aistudio.yandex.ru/docs/ru/ai-studio/dataset/api-ref/grpc/).

#### ai.datasets.viewer
Роль позволяет просматривать информацию о [датасетах](https://aistudio.yandex.ru/docs/ru/ai-studio/dataset/api-ref/grpc/).
Включает разрешения, предоставляемые ролью `ai.datasets.auditor`.

#### ai.datasets.user
Роль позволяет просматривать информацию о [датасетах](https://aistudio.yandex.ru/docs/ru/ai-studio/dataset/api-ref/grpc/) и использовать их для [дообучения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/#fm-tuning) моделей в AI Studio.
Включает разрешения, предоставляемые ролью `ai.datasets.viewer`.

#### ai.datasets.editor
Роль позволяет просматривать информацию о [датасетах](https://aistudio.yandex.ru/docs/ru/ai-studio/dataset/api-ref/grpc/), создавать, изменять и удалять датасеты, а также использовать их для [дообучения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/#fm-tuning) моделей в AI Studio.
Включает разрешения, предоставляемые ролью `ai.datasets.user`.

#### ai.datasets.admin
Включает разрешения, предоставляемые ролью `ai.datasets.editor`.

#### ai.models.auditor
Роль позволяет просматривать метаданные [моделей генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models) Yandex AI Studio.

#### ai.models.viewer
Роль позволяет просматривать информацию о [моделях генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models) Yandex AI Studio.
Включает разрешения, предоставляемые ролью `ai.models.auditor`.

#### ai.models.user
Роль позволяет использовать AI-агентов и модели генерации текста и изображений, векторного представления...
Пользователи с этой ролью могут:
* просматривать информацию о [моделях генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models) Yandex AI Studio;
* использовать [AI-агентов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/), а также модели генерации текста и изображений, модели [векторного представления текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings#yandexgpt-embeddings) и [классификаторов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/models) в сервисе Yandex AI Studio;
* использовать сервис Yandex Translate для [перевода текста](https://aistudio.yandex.ru/docs/ru/translate/quickstart);
* использовать сервис Yandex Vision OCR для [анализа изображений](https://aistudio.yandex.ru/docs/ru/vision/concepts/ocr/);
* использовать сервис Yandex SpeechKit для [распознавания](https://aistudio.yandex.ru/docs/ru/speechkit/stt/) и [синтеза](https://aistudio.yandex.ru/docs/ru/speechkit/tts/) речи.
Включает разрешения, предоставляемые ролью `ai.models.viewer`.

#### ai.models.editor
Роль позволяет управлять дообучением моделей Yandex AI Studio, а также использовать сервисы...
Пользователи с этой ролью могут:
* просматривать информацию о [моделях генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models) Yandex AI Studio;
* [дообучать](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/tuning/#fm-tuning) модели Yandex AI Studio, а также создавать, изменять и удалять дообученные модели;
* использовать [AI-агентов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/), а также модели генерации текста и изображений, модели [векторного представления текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings#yandexgpt-embeddings) и [классификаторов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/classifier/models) в сервисе Yandex AI Studio;
* использовать сервис Yandex Translate для [перевода текста](https://aistudio.yandex.ru/docs/ru/translate/quickstart);
* использовать сервис Yandex Vision OCR для [анализа изображений](https://aistudio.yandex.ru/docs/ru/vision/concepts/ocr/);
* использовать сервис Yandex SpeechKit для [распознавания](https://aistudio.yandex.ru/docs/ru/speechkit/stt/) и [синтеза](https://aistudio.yandex.ru/docs/ru/speechkit/tts/) речи.
Включает разрешения, предоставляемые ролью `ai.models.user`.

#### ai.models.admin
Включает разрешения, предоставляемые ролью `ai.models.editor`.

#### ai.guardrails.auditor
Роль позволяет просматривать метаданные [правил модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails#rules) ответов моделей.

#### ai.guardrails.viewer
Роль позволяет просматривать информацию о [правилах модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails#rules) ответов моделей.
Включает разрешения, предоставляемые ролью `ai.guardrails.auditor`.

#### ai.guardrails.user
Роль позволяет применять [правила модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails#rules) ответов моделей и просматривать метаданные таких правил.

#### ai.guardrails.editor
Роль позволяет просматривать информацию о [правилах модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails#rules) ответов моделей, а также создавать, применять, изменять и удалять такие правила.
Включает разрешения, предоставляемые ролями `ai.guardrails.viewer` и `ai.guardrails.user`.

#### ai.guardrails.admin
Включает разрешения, предоставляемые ролью `ai.guardrails.editor`.

#### serverless.mcpGateways.auditor
Роль позволяет просматривать информацию об [MCP-серверах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/#servers) и назначенных [правах доступа](https://yandex.cloud/ru/docs/iam/concepts/access-control/roles) к ним.

#### serverless.mcpGateways.viewer
Включает разрешения, предоставляемые ролью `serverless.mcpGateways.auditor`.

#### serverless.mcpGateways.invoker
Роль позволяет обращаться к [MCP-серверам](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/#servers), в том числе через MCP Hub.

#### serverless.mcpGateways.anonymousInvoker
Роль позволяет обращаться к [MCP-серверам](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/#servers), в том числе через MCP Hub.

#### serverless.mcpGateways.editor
Роль позволяет создавать, изменять и удалять [MCP-серверы](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/#servers), просматривать информацию о них и назначенных [правах доступа](https://yandex.cloud/ru/docs/iam/concepts/access-control/roles) к ним.
Включает разрешения, предоставляемые ролью `serverless.mcpGateways.viewer`.

#### serverless.mcpGateways.admin
Роль позволяет управлять MCP-серверами и доступом к ним.
Пользователи с этой ролью могут:
* просматривать информацию об [MCP-серверах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/#servers), а также создавать, изменять и удалять их;
* просматривать информацию о назначенных [правах доступа](https://yandex.cloud/ru/docs/iam/concepts/access-control/roles) к MCP-серверам, а также изменять такие права доступа;
* обращаться через MCP Hub к MCP-серверам, в том числе внешним.
Включает разрешения, предоставляемые ролями `serverless.mcpGateways.editor`, `serverless.mcpGateways.invoker` и `serverless.mcpGateways.viewer`.

#### ai.auditor
Роль позволяет просматривать информацию о квотах сервисов [Yandex Translate](https://aistudio.yandex.ru/docs/ru/translate/concepts/limits#translate-quotas), [Yandex Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/concepts/limits#vision-quotas), [Yandex SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/concepts/limits#speechkit-quotas) и [Yandex AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits#yandexgpt-quotas), о загруженных [файлах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore#file-uploading), [поисковых индексах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/search/vectorstore) Vector Store, [датасетах](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/resources/dataset) и [моделях генерации текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/models) Yandex AI Studio, просматривать метаданные [правил модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails#rules) ответов моделей, а также информацию об [облаке](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#cloud) и [каталоге](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder).
Включает разрешения, предоставляемые ролями `ai.assistants.auditor`, `ai.datasets.auditor`, `ai.models.auditor` и `ai.guardrails.auditor`.

#### ai.viewer
Включает разрешения, предоставляемые ролями `ai.assistants.viewer`, `ai.datasets.viewer`, `ai.models.viewer`, `ai.guardrails.viewer` и `ai.auditor`.

#### ai.editor
Включает разрешения, предоставляемые ролями `ai.assistants.editor`, `ai.datasets.editor`, `ai.models.editor`, `ai.guardrails.editor`, `ai.viewer`, `serverless.mcpGateways.editor`, `ai.languageModels.user`, `ai.imageGeneration.user`, `ai.playground.user` и `serverless.mcpGateways.invoker`.

#### ai.admin
Включает разрешения, предоставляемые ролями `ai.editor`, `serverless.mcpGateways.admin`, `ai.assistants.admin`, `ai.datasets.admin` и `ai.models.admin`.

### Примитивные роли

Примитивные роли позволяют пользователям совершать действия во [всех сервисах](https://yandex.cloud/ru/docs/overview/concepts/services) Yandex Cloud.

#### auditor
Роль предоставляет разрешения на чтение конфигурации и метаданных любых ресурсов Yandex Cloud без возможности доступа к данным сервисов.

#### viewer
Роль предоставляет разрешения на чтение информации о любых [ресурсах](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy) Yandex Cloud.
Включает разрешения, предоставляемые ролью `auditor`.

#### editor
Роль предоставляет разрешения на управление любыми [ресурсами](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy) Yandex Cloud, кроме назначения ролей другим пользователям.
Включает разрешения, предоставляемые ролью `viewer`.

#### admin
Роль позволяет назначать любые роли, а также предоставляет разрешения на управление любыми [ресурсами](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy) Yandex Cloud.
Включает разрешения, предоставляемые ролью `editor`.

## См. также
* [Как назначить роль](https://yandex.cloud/ru/docs/iam/operations/roles/grant)
* [Как отозвать роль](https://yandex.cloud/ru/docs/iam/operations/roles/revoke)
* [Подробнее об управлении доступом в Yandex Cloud](https://yandex.cloud/ru/docs/iam/concepts/access-control/index)
* [Подробнее о наследовании ролей](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#access-rights-inheritance)

## 9.2 Создание API-ключа

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/operations/get-api-key.html

[Yandex AI Studio](https://aistudio.yandex.ru/) является частью платформы Yandex Cloud и использует ее систему аутентификации и авторизации. Вы можете отправлять запросы к моделям AI Studio, Yandex Translate, Yandex Vision OCR или SpeechKit через API от имени своего пользовательского аккаунта, используя [IAM-токен](https://yandex.cloud/ru/docs/iam/concepts/authorization/iam-token) для аутентификации. Это наиболее безопасный способ для быстрых экспериментов, поскольку время жизни IAM-токена не превышает 12 часов.

Для работы с API мы рекомендуем использовать [сервисный аккаунт](https://yandex.cloud/ru/docs/iam/concepts/users/service-accounts) с [API-ключом](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key).

Чтобы создать API-ключ:

## Интерфейс AI Studio

1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) нажмите **Создать API-ключ** в правом верхнем углу.
2. (Опционально) Измените описание API-ключа, чтобы вы легко могли найти его после.
3. Выберите срок действия API-ключа.
4. Нажмите кнопку **Создать**.
5. Сохраните идентификатор и секретный ключ.

> **Внимание**
> Не передавайте никому свой API-ключ. После закрытия диалога значение ключа будет недоступно.

Сервис автоматически создаст сервисный аккаунт с минимально необходимыми [ролями](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html#ai-models-user) и API-ключ для него с [областью действия](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key#scoped-api-keys) для работы со всеми компонентами и сервисами AI Studio.

### Какие роли получит сервисный аккаунт

Созданный сервисный аккаунт имеет следующие роли:

| Роль | Описание |
| :--- | :--- |
| `ai.editor` | Доступ к Yandex Translate, Yandex Vision OCR, Yandex SpeechKit и Yandex AI Studio |
| `serverless.mcpGateways.invoker` | Доступ к MCP-серверам, в том числе через MCP Hub |
| `serverless.mcpGateways.anonymousInvoker` | Доступ к внешним MCP-серверам |
| `serverless.workflows.executor` | Доступ к выполнению рабочих процессов Yandex Workflows |
| `search-api.webSearch.user` | Доступ к Yandex Search API с использованием API v2 |

### Какую область действия получит API-ключ

Созданный API-ключ имеет следующие области действия:

| Область действия | Описание |
| :--- | :--- |
| `yc.ai.imageGeneration.execute` | Доступ к генерации изображений |
| `yc.ai.languageModels.execute` | Доступ к генерации текста с помощью моделей |
| `yc.ai.speechkitStt.execute` | Доступ к распознаванию речи |
| `yc.ai.speechkitTts.execute` | Доступ к синтезу речи |
| `yc.ai.translate.execute` | Доступ к переводу текста |

Теперь вы можете отправлять запросы во все API сервисов AI Studio, используя созданный API-ключ.

---

### Ссылки на другие страницы документации

*   [Документация AI Studio](https://aistudio.yandex.ru/docs/ru/index.html)
*   [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
*   [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
*   [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)
*   [Отключить логирование запросов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/disable-logging.html)
*   [Обзор технологий SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/overview.html)
*   [О сервисе Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/concepts/index.html)
*   [О сервисе Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/concepts/ocr/index.html)
*   [О сервисе Translate](https://aistudio.yandex.ru/docs/ru/translate/concepts/index.html)
*   [Тарифы AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html)
*   [Квоты и лимиты AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html)
*   [История изменений AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/release-notes/index.html)

## 9.3 Модерация ответов

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html

> **Примечание**
> Функциональность находится на стадии [Preview](https://yandex.cloud/ru/docs/overview/concepts/launch-stages).

**Модерация ответов** — это функциональность AI Studio, позволяющая проверять запросы к генеративным моделям и ответы моделей на соответствие [правилам модерации](#rules). При выявлении нарушений на этапе проверки запроса он не направляется в модель, при выявлении нарушений в ответе модели такой ответ не отображается конечному пользователю. В обоих случаях конечному пользователю возвращается [сообщение](#message), предусмотренное правилом модерации, без возникновения технической ошибки.

## Правила модерации {#rules}

**Правила модерации** состоят из [классификатора](#classifier), привязанного набора [словарей](#dictionaries) и текста [сообщения](#message), которое будет возвращаться конечному пользователю при блокировке контента правилом.

Каждый запрос к модели, к которой применяется правило модерации, и каждый ответ такой модели проверяются по заданным словарям и классификатору. При обнаружении нежелательного или подозрительного контента правило срабатывает, а конечному пользователю возвращается предусмотренное правилом сообщение.

По умолчанию для всех [собственных моделей Яндекса](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html#yandex) применяется **системное правило модерации**, в которое входит классификатор в типовой конфигурации и набор системных словарей. Системное правило модерации обеспечивает типовую модерацию запросов к модели и ее ответов. Для опенсорс-моделей системное правило модерации по умолчанию отключено, но вы можете [применить](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-guardrails.html#apply-to-instance) его для инстансов таких моделей вручную.

Помимо системного правила, к запросам и ответам могут применяться **пользовательские правила модерации**, для которых классификатор и набор словарей вы можете настраивать самостоятельно.

В случае применения пользовательского правила модерации системное правило модерации для этого инстанса модели отключается. В этом случае пользователь самостоятельно определяет параметры модерации контента и несет ответственность за последствия такого выбора, включая связанные риски.

> **Важно**
> В моделях генерации изображений YandexART системное правило модерации отключить нельзя.

При каждом изменении и срабатывании правила модерации система генерирует [аудитное событие](https://aistudio.yandex.ru/docs/ru/ai-studio/at-ref.html). Вы можете настроить сбор аудитных событий и использовать их при [настройке](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-guardrails.html) и отладке правил. Подробнее читайте в разделе [Настроить выгрузку аудитных логов AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/analyze-logs.html).

## Ответ модели при срабатывании правила {#response}

При срабатывании правила модерации [ответ модели](https://aistudio.yandex.ru/docs/ru/ai-studio/responses/getResponse.html#200) будет содержать следующие значения полей, указывающие на блокировку запроса пользователя или ответа модели правилом модерации:
* значение `incomplete` в поле `response.status`;
* значение `content_filter` в поле `response.incomplete_details.reason`;
* текст [сообщения](#message) о блокировке контента в поле `response.output`.

> **Важно**
> Если запрос завершился срабатыванием правила модерации, то этот запрос нельзя использовать в [поле](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/assistant-responses-migration.html#simple-responses-api) `previous_response_id`.

**Пример полного ответа модели с заблокированным содержимым:**

```python
Response(
    id='53d71984-2691-48e9-bc7e-********2b74',
    created_at=1772185325.0,
    error=None,
    incomplete_details=IncompleteDetails(
        reason='content_filter',
        valid=True
    ),
    instructions='Ты креативный ассистент. Помогаешь с генерацией идей.',
    metadata={},
    model='gpt://b1gmk1eb9116********/yandexgpt',
    object='response',
    output=[
        ResponseOutputMessage(
            id='2c0e9325-48e2-4bb9-97c4-********ac05',
            content=[
                ResponseOutputText(
                    annotations=[],
                    text='Я не могу обсуждать эту тему. Давайте поговорим о чём-нибудь ещё.',
                    type='output_text',
                    logprobs=None
                )
            ],
            role='assistant',
            status='completed',
            type='message'
        )
    ],
    usage=Usage(
        completion_tokens=0,
        prompt_tokens=0,
        total_tokens=0,
        completion_tokens_details=CompletionTokensDetails(
            accepted_prediction_tokens=0,
            audio_tokens=0,
            reasoning_tokens=0,
            rejected_prediction_tokens=0
        ),
        prompt_tokens_details=PromptTokensDetails(
            audio_tokens=0,
            cached_tokens=0
        )
    )
)
```

## Настройка правил модерации {#rule-settings}

> **Примечание**
> Управлять правилами модерации и словарями может пользователь с [ролью](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html#ai-guardrails-editor) `ai.guardrails.editor` или выше на каталог, в котором находится инстанс.

Правила модерации [настраиваются](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-guardrails.html) в [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) и применяются для инстансов, при этом для одного инстанса можно [применить](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-guardrails.html#apply-to-instance) только одно правило модерации.

## Словари {#dictionaries}

Каждый запрос к модели и ее ответ проверяются [правилом модерации](#rules) на наличие определенных нежелательных фраз. Списки нежелательных фраз объединяются в регистронезависимые словари, которые привязываются к правилу модерации. Помимо фраз словари также могут содержать [регулярные выражения](https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D0%B3%D1%83%D0%BB%D1%8F%D1%80%D0%BD%D1%8B%D0%B5_%D0%B2%D1%8B%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F) в формате [re2](https://github.com/google/re2/wiki/Syntax), которые позволяют более гибко и эффективно находить в тексте нежелательные слова или фразы.

Системное правило модерации использует **системные словари**, которые могут использоваться также и пользовательскими правилами модерации. При этом посмотреть состав системных словарей нельзя.

Собственные наборы нежелательных фраз и регулярных выражений вы можете объединять в **пользовательские словари**.

Правило модерации срабатывает при обнаружении фразы или соответствия регулярному выражению, которые входят в словари, привязанные к правилу.

К одному правилу модерации может быть привязано не более 50 словарей, при этом один словарь может быть привязан одновременно к нескольким разным правилам модерации.

Каждый словарь может содержать не более 1 000 фраз и не более десяти регулярных выражений. Длина одной фразы или регулярного выражения не может превышать 100 символов.

В настоящий момент при срабатывании правила модерации по словарю можно лишь блокировать контент, вызывающий подозрения. В будущем появится возможность при срабатывании правила по словарю только логировать подозрительные запросы и ответы модели, не блокируя контент.

## Классификатор {#classifier}

Каждый запрос к модели и ее ответ направляются в преднастроенный классификатор, который определяет допустимость взаимодействия с пользователем на данную тему. Правило модерации срабатывает, если классификатор определяет, что тема взаимодействия является нежелательной.

Для каждого правила модерации вы можете настроить пороги срабатывания по классификатору. При этом для запросов пользователя и для ответов модели пороги срабатывания настраиваются раздельно. Возможные значения порогов срабатывания:
* `OFF` — классификатор не применяется в правиле модерации.
* `LOW` — минимальный порог срабатывания, при котором блокируются только самые очевидные нарушения, выявленные классификатором (например, грубые слова).
* `MEDIUM` — сбалансированный порог срабатывания (значение по умолчанию). Обеспечивает баланс между безопасностью и свободоой общения.
* `HIGH` — строгий порог срабатывания. Блокирует больше контента, включая неоднозначные или спорные фразы.
* `MAXIMUM` — максимальный порог срабатывания, при котором блокируется любой потенциально сомнительный контент.

В настоящий момент при срабатывании правила модерации по классификатору можно лишь блокировать контент, вызывающий подозрения. В будущем появится возможность при срабатывании правила по классификатору только логировать подозрительные запросы и ответы модели, не блокируя контент.

## Сообщение пользователю {#message}

При блокировании контента правилом модерации конечный пользователь вместо ответа модели получает заданный правилом текст сообщения. Максимальная длина сообщения — 1 000 символов.

Текст сообщения в системном правиле модерации:
```text
Я не могу обсуждать эту тему. Давайте поговорим о чём-нибудь ещё.
```

## См. также {#see-also}
* [Управлять правилами модерации в AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-guardrails.html)
* [Управлять словарями правил модерации в AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-dictionaries.html)
* [Настроить выгрузку аудитных логов AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/analyze-logs.html)

## 9.4 Управление правилами модерации

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-guardrails.html

> **Примечание**
> Функциональность находится на стадии [Preview](https://yandex.cloud/ru/docs/overview/concepts/launch-stages).

> **Примечание**
> Управлять правилами модерации и словарями может пользователь с [ролью ai.guardrails.editor](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html#ai-guardrails-editor) или выше на каталог, в котором находится инстанс.

## Создать правило модерации

Чтобы создать новое [правило модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#rules):

> **Совет**
> Чтобы создать новое правило модерации на основе существующего, в строке списка с существующим правилом нажмите значок **...** и выберите **Клонировать**. В этом случае создаваемое правило будет содержать те же [настройки](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#rule-settings), что и исходное правило.

### Интерфейс AI Studio

1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) выберите [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder), в котором находится нужный инстанс.
2. На панели слева разверните раздел **Управление** и выберите **Безопасность**.
3. Перейдите на вкладку **Правила модерации ответов**.
4. Нажмите кнопку **Создать правило модерации ответов** и в открывшемся окне:
    4.1. Нажмите значок редактирования и задайте имя нового правила.
    4.2. (Опционально) Нажмите **Добавить описание**, чтобы добавить для создаваемого правила произвольное описание.
    4.3. (Опционально) Нажмите **Добавить метку**, чтобы добавить [метку](https://yandex.cloud/ru/docs/resource-manager/concepts/labels) для создаваемого правила.
4.4. В блоке **Классификатор**:
    4.4.1. Задайте порог срабатывания [классификатора](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#classifier) для запросов пользователя и для ответов модели:
    * `OFF` — классификатор не применяется в правиле модерации.
    * `LOW` — минимальный порог срабатывания, при котором блокируются только самые очевидные нарушения, выявленные классификатором (например, грубые слова).
    * `MEDIUM` — сбалансированный порог срабатывания (значение по умолчанию). Обеспечивает баланс между безопасностью и свободой общения.
    * `HIGH` — строгий порог срабатывания. Блокирует больше контента, включая неоднозначные или спорные фразы.
    * `MAXIMUM` — максимальный порог срабатывания, при котором блокируется любой потенциально сомнительный контент.
4.5. (Опционально) Разверните блок **Словари** и в появившейся форме выберите [словари](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#dictionaries) фраз и регулярных выражений, на соответствие которым правило будет проверять запросы к моделям и их ответы.
    * К одному правилу модерации можно привязать одновременно до 50 словарей.
    * При необходимости нажмите **Создать словарь**, чтобы [создать](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-dictionaries.html#create) новый словарь.
4.6. В блоке **Действие при срабатывании**:
    4.6.1. В поле **Сообщение при срабатывании** укажите текст [сообщения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#message), которое будет выводиться конечному пользователю при блокировании контента правилом модерации.
4.7. Нажмите **Создать**.

## Применить правило модерации для инстанса

Чтобы применить [правило модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#rules) для инстанса:

### Интерфейс AI Studio

1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) выберите [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder), в котором находится нужный инстанс.
2. На панели слева разверните раздел **Model Gallery** и выберите **Инстансы**.
3. В открывшемся списке выберите нужный инстанс и перейдите на вкладку **Обзор**.
4. В поле **Правила модерации** нажмите значок редактирования и выберите правило модерации, которое хотите применить.
    * При необходимости воспользуйтесь поиском по имени или описанию, чтобы быстрее найти нужное правило.
    * Для одного инстанса можно применить только одно пользовательское правило модерации.
5. В открывшемся окне подтвердите ваше согласие с возможными рисками и последствиями изменения правил безопасности.

## Изменить правило модерации

Чтобы изменить [правило модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#rules):

### Интерфейс AI Studio

1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) выберите [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder), в котором находится нужное правило.
2. На панели слева разверните раздел **Управление** и выберите **Безопасность**.
3. Перейдите на вкладку **Правила модерации ответов**.
4. В строке с нужным пользовательским правилом нажмите значок **...** и выберите **Редактировать**.
    * При необходимости воспользуйтесь строкой поиска по имени или описанию, чтобы быстрее найти нужное правило в списке.
5. В открывшемся окне:
    5.1. (Опционально) В строке с именем правила нажмите значок редактирования и задайте новое имя.
    5.2. (Опционально) Измените существующее описание правила или нажмите **Добавить описание**, чтобы добавить новое описание.
    5.3. (Опционально) Измените существующие [метки](https://yandex.cloud/ru/docs/resource-manager/concepts/labels) или нажмите **Добавить метку**, чтобы добавить новую метку для правила.
    5.4. (Опционально) В блоке **Классификатор**:
        5.4.1. Измените порог срабатывания [классификатора](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#classifier) для запросов пользователя и для ответов модели:
        * `OFF`, `LOW`, `MEDIUM`, `HIGH`, `MAXIMUM` (описания аналогичны разделу создания).
    5.5. (Опционально) В блоке **Словари** измените список [словарей](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#dictionaries).
    5.6. (Опционально) В блоке **Действие при срабатывании**:
        5.6.1. В поле **Сообщение при срабатывании** измените текст [сообщения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#message).
6. Нажмите **Сохранить**.

## Удалить правило модерации

Чтобы удалить [правило модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#rules):

### Интерфейс AI Studio

1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) выберите [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder), в котором находится нужное правило.
2. На панели слева разверните раздел **Управление** и выберите **Безопасность**.
3. Перейдите на вкладку **Правила модерации ответов**.
4. В строке с нужным пользовательским правилом нажмите значок **...** и выберите **Удалить**.
    * При необходимости воспользуйтесь строкой поиска по имени или описанию, чтобы быстрее найти нужное правило в списке.
5. В открывшемся окне подтвердите удаление.

## См. также

* [Модерация ответов в AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html)
* [Управлять словарями правил модерации в AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-dictionaries.html)
* [Настроить выгрузку аудитных логов AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/analyze-logs.html)

## 9.5 Управление словарями правил модерации

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-dictionaries.html

> **Примечание**
> Функциональность находится на стадии [Preview](https://yandex.cloud/ru/docs/overview/concepts/launch-stages).

> **Примечание**
> Управлять правилами модерации и словарями может пользователь с [ролью](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html#ai-guardrails-editor) `ai.guardrails.editor` или выше на каталог, в котором находится инстанс.

## В этой статье:
* [Создать словарь](#create)
* [Привязать словарь к правилу модерации](#attach)
* [Отвязать словарь от правила модерации](#detach)
* [Изменить словарь](#update)
* [Удалить словарь](#delete)

---

## Создать словарь {#create}

Чтобы создать новый [словарь](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#dictionaries):

> **Совет**
> Чтобы создать новый словарь на основе существующего, в строке списка с существующим словарем нажмите значок **...** и выберите **Клонировать**.
> В этом случае создаваемый словарь уже будет содержать все фразы и регулярные выражения, сохраненные в исходном словаре, и вы сможете просто дополнить или сократить имеющийся список.

### Интерфейс AI Studio
1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) выберите [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder), в котором находится нужный инстанс.
2. На панели слева разверните раздел **Управление** и выберите **Безопасность**.
3. Перейдите на вкладку **Словари**.
4. Нажмите кнопку **Создать словарь** и в открывшемся окне:
    4.1. Нажмите значок редактирования и задайте имя нового словаря.
    4.2. (Опционально) нажмите **+ Добавить описание**, чтобы добавить для создаваемого словаря произвольное описание.
    4.3. В блоке **Фразы**:
        4.3.1. В поле для ввода введите фразу, наличие которой в запросе или ответе будет вызывать срабатывание привязанного к словарю [правила модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#rules).
        4.3.2. Нажмите **+ Добавить**, чтобы добавить в словарь дополнительные фразы.
        *В один словарь вы можете добавить до 1 000 фраз, каждая длиной не более 100 символов.*
    4.4. (Опционально) Разверните блок **Регулярные выражения** и в появившейся форме:
        4.4.1. В поле для ввода введите [регулярное выражение](https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D0%B3%D1%83%D0%BB%D1%8F%D1%80%D0%BD%D1%8B%D0%B5_%D0%B2%D1%8B%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F) в формате [re2](https://github.com/google/re2/wiki/Syntax).
        *При обнаружении в запросе или ответе соответствия этому регулярному выражению будет срабатывать привязанное к словарю правило модерации.*
        4.4.2. Нажмите **+ Добавить**, чтобы добавить в словарь дополнительные регулярные выражения.
        *В один словарь вы можете добавить до 10 регулярных выражений, каждое длиной не более 100 символов.*
5. Нажмите **Создать**.

Созданный словарь вы можете привязать к одному или нескольким правилам модерации.

---

## Привязать словарь к правилу модерации {#attach}

Чтобы привязать [словарь](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#dictionaries) к пользовательскому [правилу модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#rules):

### Интерфейс AI Studio
1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) выберите [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder), в котором находится нужное правило модерации.
2. На панели слева разверните раздел **Управление** и выберите **Безопасность**.
3. Перейдите на вкладку **Правила модерации ответов** и в строке с нужным правилом нажмите значок **...** и выберите **Редактировать**.
    *При необходимости воспользуйтесь строкой поиска по имени или описанию, чтобы быстрее найти в списке нужное правило модерации, или [создайте](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-guardrails.html#create) новое правило.*
4. В открывшемся окне с настройками правила в блоке **Словари** выберите словарь, который вы хотите привязать к правилу модерации.
5. Нажмите **Сохранить**.

---

## Отвязать словарь от правила модерации {#detach}

Чтобы отвязать [словарь](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#dictionaries) от пользовательского [правила модерации](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#rules):

### Интерфейс AI Studio
1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) выберите [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder), в котором находится нужное правило модерации.
2. На панели слева разверните раздел **Управление** и выберите **Безопасность**.
3. Перейдите на вкладку **Правила модерации ответов** и в строке с нужным правилом нажмите значок **...** и выберите **Редактировать**.
    *При необходимости воспользуйтесь строкой поиска по имени или описанию, чтобы быстрее найти нужное правило модерации.*
4. В открывшемся окне с настройками правила в блоке **Словари** отмените выбор словаря, который вы хотите отвязать от правила модерации.
5. Нажмите **Сохранить**.

---

## Изменить словарь {#update}

Чтобы изменить [словарь](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#dictionaries):

### Интерфейс AI Studio
1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) выберите [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder), в котором находится нужный словарь.
2. На панели слева разверните раздел **Управление** и выберите **Безопасность**.
3. Перейдите на вкладку **Словари**.
4. В строке с нужным пользовательским словарем нажмите значок **...** и выберите **Редактировать**.
    *При необходимости воспользуйтесь строкой поиска по имени или описанию, чтобы быстрее найти нужный словарь в списке.*
5. В открывшемся окне:
    5.1. (Опционально) В строке с именем словаря нажмите значок редактирования и задайте новое имя.
    5.2. (Опционально) Измените существующее описание словаря или нажмите **+ Добавить описание**, чтобы добавить новое описание.
    5.3. (Опционально) В блоке **Фразы**:
        5.3.1. В строках с фразами используйте значок корзины, чтобы удалить фразы из списка.
        5.3.2. Нажмите **+ Добавить**, чтобы добавить в словарь новые фразы.
        *Один словарь может содержать до 1 000 фраз, каждая длиной не более 100 символов.*
    5.4. (Опционально) В блоке **Регулярные выражения**:
        5.4.1. В строках с [регулярными выражениями](https://ru.wikipedia.org/wiki/%D0%A0%D0%B5%D0%B3%D1%83%D0%BB%D1%8F%D1%80%D0%BD%D1%8B%D0%B5_%D0%B2%D1%8B%D1%80%D0%B0%D0%B6%D0%B5%D0%BD%D0%B8%D1%8F) используйте значок корзины, чтобы удалить регулярные выражения из списка.
        5.4.2. Нажмите **+ Добавить**, чтобы добавить в словарь новые регулярные выражения в формате [re2](https://github.com/google/re2/wiki/Syntax).
        *Один словарь может содержать до 10 регулярных выражений, каждое длиной не более 100 символов.*
6. Нажмите **Сохранить**.

---

## Удалить словарь {#delete}

Чтобы удалить [словарь](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html#dictionaries):

### Интерфейс AI Studio
1. В [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/) выберите [каталог](https://yandex.cloud/ru/docs/resource-manager/concepts/resources-hierarchy#folder), в котором находится нужный словарь.
2. На панели слева разверните раздел **Управление** и выберите **Безопасность**.
3. Перейдите на вкладку **Словари**.
4. В строке с нужным пользовательским словарем нажмите значок **...** и выберите **Удалить**.
    *При необходимости воспользуйтесь строкой поиска по имени или описанию, чтобы быстрее найти нужный словарь в списке.*
5. В открывшемся окне подтвердите удаление.

---

## См. также
* [Модерация ответов в AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/security/guardrails.html)
* [Управлять правилами модерации в AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/manage-guardrails.html)
* [Настроить выгрузку аудитных логов AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/security/analyze-logs.html)

---


# 10. Квоты и лимиты

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html

В сервисе Yandex AI Studio действуют следующие ограничения:
* **Квоты** — организационные ограничения, которые можно изменить по запросу в техническую поддержку.
* **Лимиты** — технические ограничения, обусловленные особенностями архитектуры Yandex Cloud. Изменение лимитов невозможно.

Если вам необходимо больше ресурсов, отправьте [запрос в техническую поддержку](https://center.yandex.cloud/support) и расскажите, какие потребляемые квоты нужно увеличить и на сколько.

## Квоты

| Вид ограничения | Значение |
| --- | --- |
| **Векторизация текста** | |
| Количество запросов на векторизацию текста, в секунду | 10 |
| **Выделенные инстансы** | |
| Количество одновременных выделенных инстансов | 1 |
| **Генерация текста** | |
| Количество одновременных генераций в синхронном режиме | 10 |
| Количество запросов в секунду, асинхронный режим (запрос) | 10 |
| Количество запросов в секунду, асинхронный режим (получение ответа) | 50 |
| Количество запросов в час, асинхронный режим (запрос) | 5 000 |
| Количество запросов в секунду на токенизацию | 50 |
| **Пакетный режим работы моделей** | |
| Количество запусков в час | 10 |
| Количество запусков в сутки | 100 |
| **Классификация текста** | |
| Количество запросов на классификацию текста в секунду | 1 |
| **Генерация изображений** | |
| Количество запросов на генерацию в минуту | 500 |
| Количество запросов на генерацию в сутки | 5 000 |
| Количество запросов результата в секунду | 50 |
| **Дообучение моделей** | |
| Количество запусков дообучений в сутки | 10 |
| Количество запусков дообучений в час | 3 |
| **Датасеты** | |
| Количество загруженных датасетов | 100 |
| Максимальный размер одного датасета | 5 ГБ |
| Общий объем датасетов | 300 ГБ |
| **MCP-серверы** | |
| Количество MCP-серверов в облаке | 30 |
| Количество инструментов в одном сервере | 50 |
| **Голосовые агенты (модель [speech-realtime-250923](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html))** | |
| Количество одновременных сессий с моделью | 10 |
| Количество запросов на создание сессии в секунду | 10 |
| **AI-агенты** | |
| Количество одновременных запусков Code Interpreter | 3 |

## Лимиты

| Вид ограничения | Значение |
| --- | --- |
| Срок хранения результатов асинхронных запросов на сервере | 3 суток |
| **Векторизация текста** | |
| Количество токенов на вход | 2 048 |
| Размерность выходного вектора | 256 |
| **Генерация текста** | |
| Максимальное количество токенов в ответе в [AI Playground](https://aistudio.yandex.cloud/platform/) | 1 000 |
| **Классификация текста** | |
| Количество классов в классификаторах по промпту | 20 |
| Количество классов в дообученных классификаторах | 100 |
| **Генерация изображений** | |
| Максимальная длина промпта | 500 символов |
| **AI-агенты** | |
| Максимальное количество агентов | 1 000 |
| Максимальное количество загруженных файлов | 10 000 |
| Максимальный размер файла | 128 МБ |
| Количество файлов в одной загрузке | 100 |
| Максимальное количество файлов в поисковом индексе | 10 000 |
| Максимальное количество поисковых индексов | 1 000 |
| Максимальное количество запущенных операций индексации | 10 |
| Максимальная длина пользовательских чанков | 8 000 символов |
| **MCP-серверы** | |
| Количество активных соединений в облаке на одну [зону доступности](https://yandex.cloud/ru/docs/overview/concepts/geo-scope) | 500 |

## См. также

* [Сгенерировать изображение с помощью YandexART](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/yandexart-request.html)
* [Правила тарификации для Yandex AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html)

---
**Навигация:**
* Предыдущая: [Translate](https://aistudio.yandex.ru/docs/ru/translate/at-ref.html)
* Следующая: [SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/concepts/limits.html)

---


# 11. Тарификация

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html

Все цены в рублях и тенге указаны с НДС, все цены в долларах — без НДС.

## Model Gallery

Стоимость использования моделей зависит от [режима работы](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/index.html#working-mode) и количества [токенов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html) разных типов потребления:
* входящие токены запроса;
* исходящие токены ответа модели;
* кешированные токены, если часть информации используется повторно без дополнительных вычислений, например инструкция для модели;
* токены инструментов, переданные в модель в результате вызова какого-либо [инструмента](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/agents/index.html#tools).

Кеширование включается автоматически в тех случаях, когда это возможно и применимо. Кеширование не гарантируется и не применяется к исходящим токенам.

К токенам инструментов относятся все некешированные токены, хранящиеся в истории сообщений на момент передачи результатов работы инструмента. Токены инструментов вычисляются только для встроенных инструментов AI Studio и не распространяются на результаты работы пользовательских функций. [Обращение к инструментам](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html#rules-tools) оплачивается отдельно.

### Синхронный режим работы моделей

Цены в рублях:

| Модель | Цена за 1000 входящих токенов, вкл. НДС | Цена за 1000 кешированных токенов, вкл. НДС | Цена за 1000 токенов инструментов, вкл. НДС | Цена за 1000 исходящих токенов, вкл. НДС |
| --- | --- | --- | --- | --- |
| Alice AI LLM | 0,50 ₽ | 0,50 ₽ | 0,13 ₽ | 1,20 ₽ |
| YandexGPT Pro 5.1 | 0,80 ₽ | 0,80 ₽ | 0,20 ₽ | 0,80 ₽ |
| YandexGPT Pro | 1,20 ₽ | 1,20 ₽ | 0,30 ₽ | 1,20 ₽ |
| YandexGPT Lite | 0,20 ₽ | 0,20 ₽ | 0,05 ₽ | 0,20 ₽ |
| DeepSeek V3.2 | 0,50 ₽ | 0,13 ₽ | 0,13 ₽ | 0,80 ₽ |
| Qwen3 235B | 0,50 ₽ | 0,50 ₽ | 0,50 ₽ | 0,50 ₽ |
| gpt-oss-120b | 0,30 ₽ | 0,30 ₽ | 0,30 ₽ | 0,30 ₽ |
| gpt-oss-20b | 0,10 ₽ | 0,10 ₽ | 0,10 ₽ | 0,10 ₽ |
| Gemma3 27B | 0,40 ₽ | 0,40 ₽ | 0,40 ₽ | 0,40 ₽ |
| speech-realtime-250923 | 0,80 ₽ | 0,20 ₽ | 0,20 ₽ | 0,80 ₽ |

### Асинхронный режим работы моделей

Цены в рублях:

| Модель | Цена за 1000 входящих токенов, вкл. НДС | Цена за 1000 исходящих токенов, вкл. НДС |
| --- | --- | --- |
| Alice AI LLM | 0,25 ₽ | 1,02 ₽ |
| YandexGPT Pro 5.1 | 0,41 ₽ | 0,41 ₽ |
| YandexGPT Pro | 0,61 ₽ | 0,61 ₽ |
| YandexGPT Lite | 0,10 ₽ | 0,10 ₽ |

### Пакетный режим работы моделей

При использовании моделей в пакетном режиме минимальная стоимость запуска — 200 000 токенов.

Цены в рублях:

| Модель | Цена за 1000 входящих токенов, вкл. НДС | Цена за 1000 исходящих токенов, вкл. НДС |
| --- | --- | --- |
| Qwen2.5 7B Instruct | 0,10 ₽ | 0,10 ₽ |
| Qwen2.5 72B Instruct | 0,61 ₽ | 0,61 ₽ |
| QwQ 32B Instruct | 0,41 ₽ | 0,41 ₽ |
| Llama-3.3-70B-Instruct | 0,61 ₽ | 0,61 ₽ |
| Llama-3.1-70B-Instruct | 0,61 ₽ | 0,61 ₽ |
| DeepSeek-R1-Distill-Llama-70B | 0,61 ₽ | 0,61 ₽ |
| Qwen2.5 32B Instruct | 0,41 ₽ | 0,41 ₽ |
| DeepSeek-R1-Distill-Qwen-32B | 0,41 ₽ | 0,41 ₽ |
| phi-4 | 0,20 ₽ | 0,20 ₽ |
| Qwen2 VL 7B | 0,10 ₽ | 0,10 ₽ |
| Qwen2.5 VL 7B | 0,10 ₽ | 0,10 ₽ |
| DeepSeek 2 VL | 0,41 ₽ | 0,41 ₽ |
| DeepSeek 2 VL Tiny | 0,10 ₽ | 0,10 ₽ |
| Gemma3 1B it | 0,10 ₽ | 0,10 ₽ |
| Gemma3 4B it | 0,10 ₽ | 0,10 ₽ |
| Gemma3 12B it | 0,20 ₽ | 0,20 ₽ |
| Gemma3 27B it | 0,41 ₽ | 0,41 ₽ |
| Qwen 2.5 VL 32B Instruct | 0,41 ₽ | 0,41 ₽ |
| Qwen3-1.7B | 0,10 ₽ | 0,10 ₽ |
| Qwen3-4B | 0,10 ₽ | 0,10 ₽ |
| Qwen3-8B | 0,10 ₽ | 0,10 ₽ |
| Qwen3-14B | 0,20 ₽ | 0,20 ₽ |
| Qwen3-32B | 0,41 ₽ | 0,41 ₽ |
| Qwen3-30B-A3B | 0,41 ₽ | 0,41 ₽ |
| Qwen3-235B-A22B | 6,10 ₽ | 6,10 ₽ |

## Работа выделенных инстансов

Стоимость работы выделенного инстанса зависит от модели и выбранной конфигурации. Работа выделенного инстанса тарифицируется посекундно с округлением до юнита в большую сторону. При этом время обслуживания оборудования и развертывания модели не тарифицируется.

Цена указывается за 1 час использования. Тарификация посекундная.
Стоимость 1 юнита для выделенных инстансов равна 1,02 ₽ (вкл. НДС).

Цены в рублях:

| Модель | Цена за 1 час конфигурация S, вкл. НДС | Цена за 1 час конфигурация M, вкл. НДС | Цена за 1 час конфигурация L, вкл. НДС |
| --- | --- | --- | --- |
| Qwen 2.5 VL 32B Instruct | 817,40 ₽ | 1 634,80 ₽ | 2 452,20 ₽ |
| Qwen 2.5 72B Instruct | 817,40 ₽ | 1 634,80 ₽ | 2 452,20 ₽ |
| Gemma 3 4B it | 408,70 ₽ | 817,40 ₽ | 1 226,10 ₽ |
| Gemma 3 12B it | 408,70 ₽ | 817,40 ₽ | 1 226,10 ₽ |
| T-pro-it-2.0-FP8 | 756,40 ₽ | 1 512,80 ₽ | 2 269,20 ₽ |

## Дообучение модели

На стадии [Preview](https://yandex.cloud/ru/docs/overview/concepts/launch-stages) процесс дообучения моделей не тарифицируется. Дообученная модель YandexGPT Lite тарифицируется как базовая модель YandexGPT Lite.

## Токенизация текста

Использование токенизатора (вызовы [TokenizerService](https://aistudio.yandex.ru/docs/ru/ai-studio/text-generation/api-ref/grpc/Tokenizer/index.html) и методы [Tokenizer](https://aistudio.yandex.ru/docs/ru/ai-studio/text-generation/api-ref/Tokenizer/index.html)) не тарифицируются.

## Векторизация текста

Стоимость представления текста в виде [векторов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html) (получения эмбеддингов по тексту) зависит от объема текста, поданного на векторизацию. Создание эмбеддингов [детализируется в Yandex Cloud Billing](https://yandex.cloud/ru/docs/billing/operations/check-charges) в юнитах векторизации. 1 юнит равен 1 токену.

| Услуга | Цена за 1000 токенов, вкл. НДС |
| --- | --- |
| [Получение эмбеддингов текста](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/embeddings.html) | 0,0102 ₽ |

## Классификации текста

Стоимость классификации текста зависит от используемой модели классификации и количества переданных [токенов](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/generation/tokens.html).

* При классификации с помощью YandexGPT Lite единицей тарификации является 1 запрос до 1 000 токенов.
* При классификациях с помощью YandexGPT Pro и дообученных классификаторов единицей тарификации является 1 запрос до 250 токенов.

Запросы, содержащие тексты меньше единицы тарификации, округляются в большую сторону до ближайшего целого. Тексты большего объема тарифицируются как несколько запросов с округлением в большую сторону.

| Услуга | Цена, вкл. НДС |
| --- | --- |
| 1 запрос (1 000 токенов) на [классификацию с помощью YandexGPT Lite](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/readymade.html) | 0,1525 ₽ |
| 1 запрос (250 токенов) на [классификацию с помощью YandexGPT Pro](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/readymade.html) | 0,1525 ₽ |
| 1 запрос (250 токенов) к [дообученному классификатору](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/classifier/additionally-trained.html) | 0,1525 ₽ |

## Генерация изображений

Использование YandexART тарифицируется за каждый запрос на генерацию. При этом запросы не идемпотентны, поэтому два запроса с идентичными параметрами и промптом генерации считаются двумя самостоятельными запросами.

| Услуга | Цена, вкл. НДС |
| --- | --- |
| 1 запрос на [генерацию изображения](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/generation/yandexart-request.html) с помощью YandexART | 2,24 ₽ |

## Agent Atelier

### Голосовые агенты

Стоимость использования голосовых агентов складывается из:
* стоимости распознавания речи (входящее аудио);
* стоимости синтеза речи (исходящее аудио);
* стоимости генерации текста с помощью [модели speech-realtime-250923](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html#common-instance-sync);
* стоимости [вызова инструментов](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html#rules-tools).

| Услуга | Цена, вкл. НДС |
| --- | --- |
| Входящее аудио, за 1 секунду | 0,0122 ₽ |
| Исходящее аудио, за 1 секунду | 0,0203 ₽ |

### Текстовые агенты

Стоимость использования текстовых агентов складывается из:
* потребления токенов по правилам и тарифам [моделей Model Gallery](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html#rules-model-gallery);
* стоимости [вызова инструментов](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing.html#rules-tools).

### Вызов инструментов в агентах

| Услуга | Цена за 1000 запросов, вкл. НДС |
| --- | --- |
| Инструмент веб-поиска | 915,00 ₽ |
| Инструмент поиска по файлам | 300,00 ₽ |
| Инструмент исполнения кода | Не тарифицируется |
| Инструмент MCP | Не тарифицируется |

## AI Search

Размер поискового индекса округляется до целого числа ГБ в большую сторону.
Во всех расчетах 1 ГБ = 2^30 байт, 1 МБ = 2^20 байт.

| Услуга | Цена в день за 1 ГБ, вкл. НДС |
| --- | --- |
| Хранение индекса поиска | 10,60 ₽ |
| Хранение файлов в AI Studio | Не тарифицируется |

## MCP Hub

Примечание: Функциональность находится на стадии [Preview](https://yandex.cloud/ru/docs/overview/concepts/launch-stages).

На стадии Preview [MCP-серверы](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/index.html#servers) не тарифицируются. При этом может оплачиваться использование инструментов, создаваемых в MCP-серверах. Например, [вызовы функций](https://yandex.cloud/ru/docs/functions/pricing#invoke) Yandex Cloud Functions.

При работе с внешними API, такими как [Контур.Фокус](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/templates.html#kontur) или [amoCRM](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/mcp-hub/templates.html#amocrm), оплата использования производится партнеру напрямую.

## Внутренние ошибки сервера

Если в процессе выполнения запроса произошла внутренняя ошибка сервера, запрос не тарифицируется.

---


# 12. История изменений

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/release-notes/index.html

*Страница «История изменений» содержит хронологию релизов Yandex AI Studio с 02.08.2023 по 03.03.2026. Полный текст доступен по ссылке выше.*

---


# 13. Глоссарий

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html

## Зерно генерации

*Зерно генерации (seed)* — начальная точка для генерации изображения из шума, которая позволяет повторять результат. Так, при одном и том же промпте и зерне результат генерации будет одинаковым. Чтобы изменить сгенерированное изображение, измените значение зерна или описание.

В модели YandexART зерно генерации может принимать значения от 0 до 2<sup>63</sup>-1.

## Промпт

Управление генеративными моделями осуществляется с помощью *промптов*. Эффективный промпт должен содержать контекст запроса (инструкцию) для модели и непосредственно задание, которое модель должна выполнить, учитывая переданный контекст. Чем конкретнее составлен промпт, тем более точными будут результаты работы модели.

Кроме промпта на результаты генерации моделей будут влиять и другие параметры запроса. Используйте AI Playground, доступный в [интерфейсе AI Studio](https://aistudio.yandex.cloud/platform/), чтобы протестировать ваши запросы.

## Температура

*Температура* — это параметр больших текстовых моделей, который определяет вариативность ответа: чем выше значение температуры, тем более непредсказуемым будет результат выполнения запроса. Обычно изменяется в диапазоне от 0 до 1.

---

### Ссылки на другие страницы документации:
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
* [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
* [Публичные материалы](https://aistudio.yandex.ru/docs/ru/ai-studio/public-talks.html)
* [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)
* [Обзор технологий SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/overview.html)
* [Поддерживаемые форматы аудио](https://aistudio.yandex.ru/docs/ru/speechkit/formats.html)
* [Интеграция телефонии](https://aistudio.yandex.ru/docs/ru/speechkit/concepts/ivr-integration.html)
* [О сервисе Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/concepts/index.html)
* [Начало работы (Search API)](https://aistudio.yandex.ru/docs/ru/search-api/quickstart/index.html)
* [О сервисе Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/concepts/ocr/index.html)
* [Начало работы (Vision OCR)](https://aistudio.yandex.ru/docs/ru/vision/quickstart.html)
* [Вопросы и ответы (Vision OCR)](https://aistudio.yandex.ru/docs/ru/vision/qa/index.html)
* [О сервисе Translate](https://aistudio.yandex.ru/docs/ru/translate/concepts/index.html)
* [Начало работы (Translate)](https://aistudio.yandex.ru/docs/ru/translate/quickstart.html)
* [Получить API-ключ](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/get-api-key.html)
* [Отключить логирование запросов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/disable-logging.html)

---


# 14. FAQ

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html

## Я могу получить логи моей работы в сервисах?

Да, вы можете запросить информацию о работе с вашими ресурсами из логов сервисов Yandex Cloud. Для этого обратитесь в [техническую поддержку](https://center.yandex.cloud/support).

Получить историю запросов к моделям из логов нельзя. Данные запросов [хранятся](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/disable-logging.html) в обезличенном формате и без привязки к вашему аккаунту.

## Я могу посмотреть историю чатов?

Вы можете посмотреть историю только тех чатов, которые вели в [AI Playground](https://console.yandex.cloud/link/ai-studio/). Для этого:

1. В [консоли управления](https://console.yandex.cloud/) выберите каталог, в котором вы вели чат.
2. Выберите сервис **AI Studio**.
3. В блоке **AI Playground** выберите **Генерация текста**.

В левой части экрана вы увидите все доступные вам эксперименты.

## Можно ли обращаться к моделям из frontend-приложений?

Нет, организовать прямую работу с API сервисов Yandex AI Studio из frontend-приложений нельзя. Для решения проблемы вы можете отправлять запросы через сервис [Yandex Cloud Functions](https://aistudio.yandex.ru/docs/ru/functions/).

---
### Ссылки на другие страницы документации
- [Документация AI Studio](https://aistudio.yandex.ru/docs/ru/index.html)
- [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
- [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
- [Публичные материалы](https://aistudio.yandex.ru/docs/ru/ai-studio/public-talks.html)
- [Термины и определения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html)
- [Обзор технологий SpeechKit](https://aistudio.yandex.ru/docs/ru/speechkit/overview.html)
- [Поддерживаемые форматы аудио](https://aistudio.yandex.ru/docs/ru/speechkit/formats.html)
- [Интеграция телефонии](https://aistudio.yandex.ru/docs/ru/speechkit/concepts/ivr-integration.html)
- [О сервисе Yandex Search API](https://aistudio.yandex.ru/docs/ru/search-api/concepts/index.html)
- [О сервисе Vision OCR](https://aistudio.yandex.ru/docs/ru/vision/concepts/ocr/index.html)
- [О сервисе Translate](https://aistudio.yandex.ru/docs/ru/translate/concepts/index.html)
- [Получить API-ключ](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/get-api-key.html)
- [Отключить логирование запросов](https://aistudio.yandex.ru/docs/ru/ai-studio/operations/disable-logging.html)
- [Коды ошибок](https://aistudio.yandex.ru/docs/ru/ai-studio/troubleshooting/error-codes.html)

---


# 15. Устранение неполадок


## 15.1 Коды ошибок

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/troubleshooting/error-codes.html

В ответ на любой запрос модели AI Studio возвращают сообщение, содержащее код и статус обработки запроса. Если при обработке запроса произошла ошибка, сообщение также будет содержать возможную причину ее возникновения.

При обработке ответов моделей в своем приложении ориентируйтесь на код и статус запроса. Сообщения об ошибках содержат полезную информацию, но могут меняться при обновлении моделей.

| gRPC | REST | Статус | Причина | Решение |
| --- | --- | --- | --- | --- |
| 0 | 200 | `OK` | Операция выполнена | — |
| 3 | 400 | `INVALID_ARGUMENT` | Некорректный запрос | Проверьте формат запроса. Возможно, указан неправильный URI модели, превышена длина промпта, задано недопустимое значение параметра или нарушены этические ограничения YandexART. Например, для решения ошибок `invalid model_uri`, `Failed to parse model URI` проверьте, правильно ли введен URI модели и указан ли идентификатор каталога. Ошибка вида `Specified folder ID does not match with service account` означает, что неправильно указан идентификатор каталога или у сервисного аккаунта, от которого вы отправляете запрос, нет доступа к указанному каталогу — проверьте, от имени какого аккаунта вы отправляете запрос. |
| 4 | 504 | `DEADLINE_EXCEEDED` | Превышен срок выполнения запроса | Проблемы в сети между клиентом и сервером либо превышен таймаут ожидания ответа. Попробуйте отправить запрос повторно. При использовании AI SDK увеличьте таймаут с помощью [метода](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk-ref/sync/chat/completions.html#yandex_ai_studio_sdk._chat.completions.model.ChatModel) `config.run(timeout)`. Если проблема сохраняется, обратитесь в [техническую поддержку](https://yandex.cloud/ru/docs/support/overview). |
| 7 | 403 | `PERMISSION_DENIED` | Недостаточно прав | Проверьте:<ul><li>наличие необходимых [ролей](https://aistudio.yandex.ru/docs/ru/ai-studio/security/index.html) у [сервисного аккаунта](https://yandex.cloud/ru/docs/iam/concepts/users/service-accounts), от имени которого вы делаете запрос;</li><li>предоставлен ли доступ к модели, если он предоставляется по запросу;</li><li>привязан ли платежный аккаунт к облаку и не находится ли оно в статусе `CREATING`.</li></ul> |
| 8 | 429 | `RESOURCE_EXHAUSTED` | Превышена [квота](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/limits.html) | В зависимости от квоты, подождите или обратитесь в техническую поддержку, чтобы увеличить квоту. При запросе увеличить квоту укажите модель, режим работы и название квоты, которую необходимо увеличить. Специалисты технической поддержки могут попросить дополнительную информацию. |
| 12 | 501 | `UNIMPLEMENTED` | Проблема на стороне сервиса | Обратитесь в техническую поддержку. |
| 13 | 500 | `INTERNAL` | Внутренняя ошибка сервиса | Обратитесь в техническую поддержку. |
| 14 | 503 | `UNAVAILABLE` | Сервис недоступен | Попробуйте отправить запрос повторно или обратитесь в техническую поддержку. |
| 16 | 401 | `UNAUTHENTICATED` | Ошибка авторизации | Проверьте, от имени какого аккаунта вы отправляете запрос, правильно ли указан [API-ключ](https://yandex.cloud/ru/docs/iam/concepts/authorization/api-key) или [IAM-токен](https://yandex.cloud/ru/docs/iam/concepts/authorization/iam-token), и не истек ли срок действия токена. Сообщения ошибок могут содержать информацию об ошибке, например: `Unknown api key` — неправильно указан API-ключ или его область действия, `The apikey has expired` — истек срок действия API-ключа. |

## Была ли статья полезна?

### Ссылки на другие страницы документации:
* [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)
* [Заголовки для диагностики ошибок](https://aistudio.yandex.ru/docs/ru/ai-studio/api-ref/support-headers.html)
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
* [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
* [Тарифы](https://aistudio.yandex.ru/docs/ru/ai-studio/pricing/)

---


# Приложение: Публичные материалы

> Источник: https://aistudio.yandex.ru/docs/ru/ai-studio/public-talks.html

## Видео

### 2025 год
* От AI-ассистента к многоагентным системам. [Видео](https://www.youtube.com/watch?v=yYMoc6RTxls).
* Как оценивать и улучшать ответы генеративных моделей. [Видео](https://www.youtube.com/watch?v=sNWmI28FKTw).
* Создание Telegram-бота на базе LLM с RAG и Function Calling. [Видео](https://www.youtube.com/live/gQEpthYWN38).
* Как дообучить LLM с помощью LoRA Fine-tuning. [Видео](https://www.youtube.com/watch?v=PVeuQu1j6Y4).
* Deep-dive для разработчиков: создание AI-ассистентов. [Видео](https://www.youtube.com/watch?v=Xjutc_T0p8s).
* Искусство YandexART для бизнеса. Видео на [YouTube](https://www.youtube.com/watch?v=I9Fpsxv8Hlc) и [Яндекс](https://runtime.strm.yandex.ru/player/episode/vplefdetiqv7tasxrbyk).
* Как применять AI-агентов для конкретных бизнес-задач. [Видео](https://www.youtube.com/watch?v=VJKQjFYR2b4).
* Воркшоп «Как создать мультиагентную систему в Yandex AI Studio». [Видео](https://www.youtube.com/watch?v=Iyf17k0Hf2M).
* **How to Yandex AI Studio:**
    * Обзор платформы. [Видео](https://www.youtube.com/watch?v=tkGHcxDWbSA).
    * Как создать простого текстового агента. [Видео](https://www.youtube.com/watch?v=KY4fd3HaUNM).
    * Как создать простого голосового агента. [Видео](https://www.youtube.com/watch?v=bCwuFFHTKME).
* **AI Studio Series:**
    * Введение в агентов и мультиагентные системы. [Видео](https://www.youtube.com/watch?v=lq8dSaF5CaQ).
    * Как собрать агента на Workflows для обработки документов с OCR и VLM. [Видео](https://www.youtube.com/watch?v=f0jBqF7_Ev0).
    * Как создать и развернуть AI-агента: с нуля до продакшена. [Видео](https://www.youtube.com/watch?v=_MU5wK_FgZg).
    * Как создать голосового агента. [Видео](https://www.youtube.com/watch?v=JAcaGNmgG2U).

### 2024 год
* Создание AI-ассистентов. [Видео](https://www.youtube.com/watch?v=kKbMaWSi20I).
* Как мы делаем Yandex Cloud — ML-проекты. [Видео](https://www.youtube.com/watch?v=PM1CT4j5pd8).
* Ответы на вопросы про нейросети. [Видео](https://www.youtube.com/watch?v=sZr5vltW5Hw).
* YandexGPT для образовательных и научных проектов. [Видео](https://www.youtube.com/watch?v=YEm2wzSW2b4).
* Дообучение модели YandexGPT в Yandex DataSphere. [Видео](https://www.youtube.com/watch?v=hGrH0Shovtk).

### 2023 год
* Тренды машинного обучения. [Видео](https://www.youtube.com/watch?v=1fRV83AIq1s).

## Статьи

### 2025 год
* Что произошло с ИИ в 2025 году: восемь главных трендов. [Статья](https://yandex.cloud/ru/blog/ai-review-2025).
* ИИ‑агенты в промышленности: как перейти от хаоса пилотов к индустриальному стандарту. [Статья](https://yandex.cloud/ru/blog/ai-agents-industry).
* Автоматизировали треть рутинных задач ИБ‑специалистов с помощью ИИ‑агентов. [Статья](https://yandex.cloud/ru/blog/ai-soc).
* Представляем AI Search — технологию поиска в интернете и по документам для ИИ‑агентов. [Статья](https://yandex.cloud/ru/blog/ai-search).
* Открываем доступ к Alice AI — самому мощному семейству нейросетей Яндекса. [Статья](https://yandex.cloud/ru/blog/alice-ai-november-2025).
* Цифровое востоковедение: как ИВ РАН с Yandex Cloud открывает доступ к первоисточникам. [Статья](https://yandex.cloud/ru/blog/digital-oriental-studies).
* AI‑агенты: переход от инструментов к автономным исполнителям в бизнесе. [Статья](https://yandex.cloud/ru/blog/ai-agents).
* Клиенты Yandex AI Studio увеличили потребление генеративных нейросетей в облаке в пять раз. [Статья](https://yandex.cloud/ru/blog/yandex-ai-studio-results-october-2025).
* Yandex Cloud Stackland: новое инфраструктурное решение для разработки AI‑сервисов. [Статья](https://yandex.cloud/ru/blog/yandex-cloud-stackland).
* YandexGPT 5.1 Pro: открыли доступ к флагманской модели для бизнеса. [Статья](https://yandex.cloud/ru/blog/yandexgpt-5-1-pro).
* От карточек товаров до обучения сотрудников: как ИИ трансформирует современный ритейл. [Статья](https://yandex.cloud/ru/blog/ai-in-retail).
* Yandex AI Studio использовали в детских умных часах. [Статья](https://yandex.cloud/ru/blog/yandexgpt-speechkit-smart-watch).
* Визуально‑лингвистические модели: архитектура, применение и перспективы. [Статья](https://yandex.cloud/ru/blog/vlm-visual-language-models).
* ОТП Банк ускорил анализ обращений клиентов в 30 раз с помощью нейросетей Yandex Cloud. [Статья](https://yandex.cloud/ru/blog/otp-yandexgpt).
* Как писать промпты для нейросетей: инструкция, примеры и советы. [Статья](https://yandex.cloud/ru/blog/gpt-prompting-guide).
* Нейросети Яндекса помогли врачам ускорить разработку новых методов лечения. [Статья](https://yandex.cloud/ru/blog/local-ethics-committee).
* RAG: учим искусственный интеллект работать с новыми данными. [Статья](https://yandex.cloud/ru/blog/posts/2025/05/retrieval-augmented-generation-basics).
* HR‑Tech: как нейросети и облачные технологии помогают справляться с наймом и удержанием сотрудников… [Статья](https://yandex.cloud/ru/blog/posts/2025/05/hr-tech).
* Как технологии трансформируют строительную сферу. [Статья](https://yandex.cloud/ru/blog/posts/2025/04/technologies-in-construction).
* Как ИИ помогает в поддержке клиентов: кейсы банков, ритейла и IT‑компаний. [Статья](https://yandex.cloud/ru/blog/posts/2025/04/ai-and-support).
* Нейросети для текста: применение в бизнесе. [Статья](https://yandex.cloud/ru/blog/posts/2025/03/ai-for-texts).
* Fine‑tuning языковых моделей: как адаптировать ИИ для решения специализированных задач. [Статья](https://yandex.cloud/ru/blog/posts/2025/03/fine-tuning).
* Встречаем YandexGPT 5 — в Алисе, облаке и опенсорсе. [Статья](https://habr.com/ru/companies/yandex/articles/885218/).
* От небольшой мастерской к ML-фабрике: как мы Yandex AI Studio пересобирали. [Статья](https://habr.com/ru/companies/yandex/articles/949884/).

### 2024 год
* Как составлять промпты для нейросети: пример сервиса для создания сертификатов «Золотого Яблока». [Статья](https://vc.ru/ai/1699310-kak-sostavlyat-promty-dlya-neiroseti-primer-servisa-dlya-sozdaniya-sertifikatov-zolotogo-yabloka).
* Как с помощью YandexGPT автоматически отвечать на 60% вопросов и отзывов: опыт Ralf Ringer. [Статья](https://vc.ru/services/1659960-kak-s-pomoshyu-yandexgpt-avtomaticheski-otvechat-na-60-voprosov-i-otzyvov-opyt-ralf-ringer).
* Более мощное семейство моделей YandexGPT 4: рост качества ответов, длинный контекст, пошаговые рассуждения. [Статья](https://habr.com/ru/companies/yandex/articles/852968/).
* Создание креативов, подготовка субтитров и озвучивание текстов: какие задачи медиакомпании передают ИИ. [Статья](https://vc.ru/future/1162468-sozdanie-kreativov-podgotovka-subtitrov-i-ozvuchivanie-tekstov-kakie-zadachi-mediakompanii-peredayut-ii).
* Как мы учили YandexART создавать картинки, которые понравятся людям. [Статья](https://habr.com/ru/companies/yandex/articles/805745/).
* Персонализировать обучение и автоматически проверять работы студентов: как EdTech-проекты используют ИИ. [Статья](https://vc.ru/education/1084748-personalizirovat-obuchenie-i-avtomaticheski-proveryat-raboty-studentov-kak-edtech-proekty-ispolzuyut-ii).

### 2023 год
* Анализ отзывов, помощь в чате и креативы: что умеет YandexGPT API. [Статья](https://vc.ru/services/945084-analiz-otzyvov-pomosh-v-chate-i-kreativy-chto-umeet-yandexgpt-api).
* Как обойтись без серверов, настроить бизнес-аналитику и протестировать YandexGPT. [Статья](https://vc.ru/offline/845622-oboitis-bez-serverov-nastroit-biznes-analitiku-i-protestirovat-yandexgpt).

## Конференции и вебинары

### 2024: Yandex Scale
* От набора Ml‑сервисов к единой платформе для создания AI‑решений. [Запись трансляции](https://www.youtube.com/watch?v=70kXmv9GL8s).

### 2023: Yandex Scale
* ML в Yandex Cloud: было, есть и будет. [Запись трансляции](https://www.youtube.com/watch?v=90jIHP2F-zA).

### 2023: Webinar
* Генеративная текстовая модель YandexGPT. [Запись трансляции](https://www.youtube.com/watch?v=sdzcjygd_EQ).

---
**Ссылки на другие страницы документации:**
* [Начало работы](https://aistudio.yandex.ru/docs/ru/ai-studio/quickstart/index.html)
* [О сервисе AI Studio](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/index.html)
* [Термины и определения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html)
* [Вопросы и ответы](https://aistudio.yandex.ru/docs/ru/ai-studio/qa/index.html)
* [Request retries](https://aistudio.yandex.ru/docs/ru/ai-studio/sdk-ref/retry.html) (Предыдущая)
* [Термины и определения](https://aistudio.yandex.ru/docs/ru/ai-studio/concepts/glossary.html) (Следующая)

---

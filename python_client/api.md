# 🎵 API Документация AllTalk TTS
[AllTalk ENG] DeepSpeed version : 0.14.2+cu121torch2.2
[AllTalk ENG] Python Version    : 3.11.9
[AllTalk ENG] PyTorch Version   : 2.2.1
[AllTalk ENG] CUDA Version      : 12.1
[AllTalk ENG]
[AllTalk ENG] Loading XTTS model xttsv2_2.0.3 on cuda
[AllTalk ENG] Model License : https://coqui.ai/cpml.txt
[AllTalk ENG] Model Loadtime: 28.73 seconds
[AllTalk TTS]
[AllTalk TTS] API Address : 80.251.139.116:7851
[AllTalk TTS] Gradio Light: http://80.251.139.116:7852
[AllTalk TTS] Gradio Dark : http://80.251.139.116:7852?__theme=dark
[AllTalk TTS]
[AllTalk TTS] AllTalk WIKI: https://github.com/erew123/alltalk_tts/wiki
[AllTalk TTS] Errors Help : https://github.com/erew123/alltalk_tts/wiki/Error-Messages-List
## 🔌 Потоковая генерация TTS

### Обзор
Этот эндпоинт позволяет генерировать и стримить TTS аудио напрямую для воспроизведения в реальном времени. Не поддерживает нарратор и генерирует аудиопоток, а не файл. Также не поддерживает RVC пайплайн.

> **Примечание:** Только TTS движки, поддерживающие стриминг, могут стримить аудио (например, Coqui XTTS поддерживает стриминг).

### Детали эндпоинта
- **URL:** `http://{ipaddress}:{port}/api/tts-generate-streaming`
- **Метод:** `POST`
- **Content-Type:** `application/x-www-form-urlencoded`

### Параметры запроса

| Параметр | Тип | Описание |
|----------|-----|----------|
| `text` | string | Текст для преобразования в речь |
| `voice` | string | Тип голоса для использования |
| `language` | string | Язык для TTS |
| `output_file` | string | Имя выходного файла |

### Пример запроса

```bash
curl -X POST "http://80.251.139.116:7851/api/tts-generate-streaming" \
     -d "text=Вот какой-то текст" \
     -d "voice=female_01.wav" \
     -d "language=en" \
     -d "output_file=stream_output.wav"
```

### Ответ
Эндпоинт возвращает `StreamingResponse` для аудиопотока.

API также возвращает JSON объект со следующим свойством:

| Свойство | Описание |
|----------|----------|
| `output_file_path` | Имя выходного файла |

#### Пример ответа:
```json
{
    "output_file_path": "stream_output.wav"
}
```

### JavaScript пример для потокового воспроизведения

```javascript
const text = "Вот какой-то текст";
const voice = "female_01.wav";
const language = "en";
const outputFile = "stream_output.wav";
const encodedText = encodeURIComponent(text);
const streamingUrl = `http://localhost:7851/api/tts-generate-streaming?text=${encodedText}&voice=${voice}&language=${language}&output_file=${outputFile}`;
const audioElement = new Audio(streamingUrl);
audioElement.play();
```

### 📝 Дополнительные заметки

- **Без поддержки нарратора:** Этот эндпоинт не поддерживает функцию нарратора, доступную в стандартном эндпоинте генерации TTS
- **Без RVC пайплайна:** Потоковый эндпоинт не поддерживает RVC (Real-time Voice Conversion) пайплайн
- **Воспроизведение в реальном времени:** Предназначен для сценариев, где нужен немедленный аудиовывод
- **Совместимость с браузерами:** Работает с современными браузерами, поддерживающими аудиопотоки. Firefox может НЕ работать
- **Обработка ошибок:** Реализуйте правильную обработку ошибок в клиентском коде
- **Пропускная способность:** Требует стабильного сетевого соединения
- **Файловый вывод:** Хотя API возвращает `output_file_path`, основная цель - стриминг
- **Выбор голоса:** Убедитесь, что указанный голос доступен в конфигурации AllTalk
- **Поддержка языков:** Такая же, как в стандартной генерации TTS

---

## 🔌 Эндпоинты управления сервером

### 1. 🛑 Остановка генерации

Прерывает текущий процесс генерации TTS, если загруженный TTS движок поддерживает это.

- **URL:** `http://{ipaddress}:{port}/api/stop-generation`
- **Метод:** `PUT`

#### Ответ:
```json
{
    "message": "Отмена текущей генерации TTS"
}
```

#### Пример запроса:
```bash
curl -X PUT "http://80.251.139.116:7851/api/stop-generation"
```

### 2. 🔄 Перезагрузка конфигурации

Перезагружает конфигурацию TTS движка и сканирует новые голоса и модели.

- **URL:** `http://{ipaddress}:{port}/api/reload_config`
- **Метод:** `GET`

#### Ответ:
```
Файл конфигурации успешно перезагружен
```

### 3. 🔀 Перезагрузка/смена модели

Загружает или переключается на одну из моделей из списка `models_available`.

- **URL:** `http://{ipaddress}:{port}/api/reload`
- **Метод:** `POST`

| Параметр | Тип | Описание |
|----------|-----|----------|
| `tts_method` | string | Имя модели для загрузки |

#### Ответ:
```json
{"status": "model-success"}
```
или
```json
{"status": "model-failure"}
```

### 4. ⚡ Переключение DeepSpeed

Включает или отключает режим DeepSpeed.

- **URL:** `http://{ipaddress}:{port}/api/deepspeed`
- **Метод:** `POST`

| Параметр | Тип | Описание |
|----------|-----|----------|
| `new_deepspeed_value` | boolean | True для включения, False для отключения |

### 5. 💾 Переключение Low VRAM

Включает или отключает режим Low VRAM.

- **URL:** `http://{ipaddress}:{port}/api/lowvramsetting`
- **Метод:** `POST`

| Параметр | Тип | Описание |
|----------|-----|----------|
| `new_low_vram_value` | boolean | True для включения, False для отключения |

---

## 🔌 Эндпоинты статуса сервера

### 1. ✅ Статус готовности сервера

Проверяет, запущен ли TTS движок и готов ли принимать запросы.

- **URL:** `http://{ipaddress}:{port}/api/ready`
- **Метод:** `GET`

| Статус | Описание |
|--------|----------|
| `Ready` | TTS движок готов обрабатывать запросы |
| `Unloaded` | TTS движок перезапускается или не готов |

### 2. 🎤 Список стандартных голосов

Получает список доступных голосов для текущего TTS движка и модели.

- **URL:** `http://{ipaddress}:{port}/api/voices`
- **Метод:** `GET`

#### Ответ:
```json
{
    "status": "success",
    "voices": ["voice1", "voice2", "voice3"]
}
```

### 3. 🎭 Список RVC голосов

Получает список доступных RVC голосов для дополнительной обработки.

- **URL:** `http://{ipaddress}:{port}/api/rvcvoices`
- **Метод:** `GET`

#### Ответ:
```json
{
    "status": "success",
    "voices": ["Disabled", "folder1\\voice1.pth", "folder2\\voice2.pth"]
}
```

### 4. ⚙️ Текущие настройки

Получает текущие настройки загруженного TTS движка.

- **URL:** `http://{ipaddress}:{port}/api/currentsettings`
- **Метод:** `GET`

#### Ключевые поля ответа:

| Поле | Описание |
|------|----------|
| `engines_available` | Список доступных TTS движков |
| `current_engine_loaded` | Текущий загруженный TTS движок |
| `models_available` | Список доступных моделей |
| `current_model_loaded` | Текущая загруженная модель |
| `manufacturer_name` | Производитель TTS движка |
| `audio_format` | Основной формат аудиовывода |
| `deepspeed_capable` | Поддержка DeepSpeed |
| `streaming_capable` | Поддержка стриминга |
| `temperature_capable` | Поддержка настройки температуры |
| `languages_capable` | Поддержка множественных языков |

#### Пример ответа:
```json
{
    "engines_available": ["parler", "piper", "vits", "xtts"],
    "current_engine_loaded": "xtts",
    "models_available": [
        {"name": "xtts - xttsv2_2.0.2"},
        {"name": "xtts - xttsv2_2.0.3"}
    ],
    "current_model_loaded": "xtts - xttsv2_2.0.3",
    "manufacturer_name": "Coqui",
    "audio_format": "wav",
    "deepspeed_capable": true,
    "streaming_capable": true,
    "temperature_capable": true,
    "languages_capable": true
}
```

---

## 💡 Советы по использованию

- ✅ Проверяйте готовность сервера перед другими API вызовами
- 🎤 Используйте эндпоинты голосов для заполнения меню выбора
- ⚙️ Используйте эндпоинт текущих настроек для адаптации UI
- 🔄 Регулярно опрашивайте эндпоинты для поддержания актуального статуса
- 🛑 Используйте остановку генерации при необходимости отмены процесса
- 📊 Всегда проверяйте статус ответа для подтверждения успешности изменений
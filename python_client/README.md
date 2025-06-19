# 🎵 AllTalk TTS Python Клиент

Профессиональный Python клиент для AllTalk TTS API с поддержкой потокового аудио, умного чанкования текста и интеграции с языковыми моделями типа Ollama.

**Обновлен согласно официальным рекомендациям по интеграции AllTalk API**

## ✨ Новые возможности v2.0

### 🔧 Управление конфигурацией
- **Автоматическое создание** конфигурационного файла
- **Горячее обновление** настроек без перезапуска
- **Валидация параметров** с fallback значениями
- **Персистентное хранение** успешных настроек

### 💾 Система кэширования
- **TTL кэш** для API ответов (голоса, настройки, возможности)
- **Автоматическая инвалидация** устаревших данных
- **Ускорение повторных запросов** до 10x
- **Умная очистка** при перезагрузке конфигурации

### 🔄 Устойчивость к ошибкам
- **Автоматические повторы** с экспоненциальной задержкой
- **Graceful degradation** при недоступности сервера
- **Детальное логирование** для диагностики
- **Fallback режимы** для критических функций

### ⚙️ Проверка возможностей сервера
- **Автоматическое определение** capabilities сервера
- **Адаптивное поведение** в зависимости от возможностей
- **Валидация голосов** перед использованием
- **Предупреждения** о неподдерживаемых функциях

## 🚀 Быстрый старт

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Базовое использование с автоконфигурацией
```python
import asyncio
from client import TTSStreamingClient

async def main():
    async with TTSStreamingClient() as client:
        # Автоматическая инициализация с проверкой сервера
        if await client.initialize():
            print("✅ Клиент готов к работе")
            
            # Генерация TTS из текста
            async for audio_chunk in client.generate_tts_from_text(
                "Привет! Это демонстрация нового TTS клиента."
            ):
                print(f"🎵 Получен аудио чанк: {len(audio_chunk)} байт")
        else:
            print("❌ Сервер недоступен")

asyncio.run(main())
```

## 📋 Конфигурация

### Автоматическое создание конфигурации
При первом запуске создается файл `tts_config.json`:

```json
{
    "api_alltalk_protocol": "http://",
    "api_alltalk_ip_port": "80.251.139.116:7851",
    "api_connection_timeout": 5,
    "max_retries": 3,
    "retry_delay": 1.0,
    "cache_ttl": 300,
    "default_voice": "female_01.wav",
    "default_language": "en",
    "default_chunk_size": 200,
    "default_chunk_timeout": 2.0
}
```

### Обновление конфигурации в runtime
```python
from client import TTSConfig

config = TTSConfig()
config.update_config(
    default_voice="male_01.wav",
    max_retries=5,
    cache_ttl=600
)
```

## 🎯 Основные возможности

### 1. 🧠 Умное чанкование текста

Алгоритм разбиения текста с приоритетами:
1. **По предложениям** (`.!?`)
2. **По клаузам** (`,;`) для длинных предложений  
3. **По словам** для очень длинных клауз

```python
client = TTSStreamingClient()

# Автоматическое чанкование
chunks = client.chunk_text(
    "Длинный текст. С несколькими предложениями, содержащими запятые!",
    max_chunk_size=30
)
print(f"Создано {len(chunks)} чанков")
```

### 2. 🌊 Потоковая обработка с Ollama

```python
async def stream_from_ollama():
    async with TTSStreamingClient() as tts_client:
        if await tts_client.initialize():
            # Симуляция потока от Ollama
            async def text_generator():
                texts = ["Привет! ", "Как дела? ", "Это потоковый текст."]
                for text in texts:
                    yield text
                    await asyncio.sleep(0.1)
            
            # Потоковая генерация TTS
            async for audio_data in tts_client.stream_tts_from_iterator(
                text_generator(),
                max_chunk_size=100,
                chunk_timeout=1.0
            ):
                print(f"🎵 Аудио чанк: {len(audio_data)} байт")
```

### 3. 🔍 Проверка возможностей сервера

```python
async with TTSStreamingClient() as client:
    if await client.initialize():
        capabilities = await client.get_server_capabilities()
        
        print("🔧 Возможности сервера:")
        for capability, supported in capabilities.items():
            status = "✅" if supported else "❌"
            print(f"  {status} {capability}")
        
        # Адаптивное поведение
        if capabilities.get('streaming_capable'):
            print("🌊 Используем потоковую генерацию")
        else:
            print("📦 Используем обычную генерацию")
```

### 4. 💾 Кэширование для производительности

```python
async with TTSStreamingClient() as client:
    # Первый запрос - обращение к серверу
    voices1 = await client.get_available_voices(use_cache=False)
    
    # Второй запрос - из кэша (быстрее в ~10 раз)
    voices2 = await client.get_available_voices(use_cache=True)
    
    # Принудительное обновление кэша
    await client.reload_config()  # Очищает кэш
```

### 5. 🎤 Автоматическая валидация голосов

```python
async with TTSStreamingClient() as client:
    if await client.initialize():
        # Клиент автоматически проверит доступность голоса
        audio = await client.stream_tts_chunk(
            "Тест голоса",
            voice="nonexistent_voice.wav"  # Несуществующий голос
        )
        # Автоматически выберется первый доступный голос
```

## 🔄 Синхронная версия

Для совместимости с синхронным кодом:

```python
from client import SyncTTSClient

sync_client = SyncTTSClient()

# Проверка сервера с повторными попытками
if sync_client.check_server_ready():
    print("✅ Сервер готов")
    
    # Получение голосов с retry логикой
    voices = sync_client.get_available_voices()
    print(f"🎤 Доступно голосов: {len(voices)}")
    
    # Чанкование текста
    chunks = sync_client.chunk_text("Тестовый текст для разбиения.")
    print(f"✂️ Создано чанков: {len(chunks)}")
```

## 🧪 Тестирование

Запуск полного набора тестов:

```bash
cd python_client
python test_tts_client.py
```

### Тестовые сценарии:
- ✅ **Управление конфигурацией** - создание, загрузка, обновление
- ✅ **Возможности сервера** - определение capabilities, fallback режимы  
- ✅ **Система кэширования** - TTL, инвалидация, производительность
- ✅ **Механизм повторов** - retry логика, экспоненциальные задержки
- ✅ **Улучшенное чанкование** - разные размеры, знаки препинания
- ✅ **Валидация голосов** - проверка доступности, автозамена
- ✅ **Потоковая обработка** - симуляция Ollama, буферизация
- ✅ **Синхронный клиент** - совместимость, retry механизмы

## 📊 Мониторинг и логирование

### Настройка логирования
```python
import logging

# Детальное логирование для отладки
logging.basicConfig(level=logging.DEBUG)

# Только важные сообщения
logging.basicConfig(level=logging.WARNING)
```

### Метрики производительности
```python
async with TTSStreamingClient() as client:
    if await client.initialize():
        # Статистика сохраняется в конфигурации
        print(f"Последняя успешная генерация: {client.config.config.get('last_successful_generation')}")
        print(f"Используемый голос: {client.config.config.get('last_successful_voice')}")
```

## 🔒 Лучшие практики безопасности

### 1. Валидация входных данных
```python
def safe_text_input(text: str) -> str:
    """Очистка и валидация текста перед отправкой в TTS"""
    # Ограничение длины
    if len(text) > 10000:
        text = text[:10000]
    
    # Удаление потенциально опасных символов
    import re
    text = re.sub(r'[<>"\']', '', text)
    
    return text.strip()
```

### 2. Ограничение скорости запросов
```python
import asyncio
from asyncio import Semaphore

class RateLimitedTTSClient:
    def __init__(self, max_concurrent=5):
        self.semaphore = Semaphore(max_concurrent)
        self.client = TTSStreamingClient()
    
    async def generate_with_limit(self, text: str):
        async with self.semaphore:
            async with self.client as client:
                if await client.initialize():
                    async for chunk in client.generate_tts_from_text(text):
                        yield chunk
```

### 3. Обработка чувствительных данных
```python
# НЕ логируем полный текст в продакшене
logger.info(f"Обработка текста длиной {len(text)} символов")

# Вместо:
# logger.info(f"Обработка текста: {text}")  # Может содержать личные данные
```

## 🚀 Интеграция с производственными системами

### Docker развертывание
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Конфигурация через переменные окружения
ENV TTS_SERVER_URL="http://alltalk-server:7851"
ENV TTS_MAX_RETRIES="5"
ENV TTS_CACHE_TTL="600"

CMD ["python", "your_app.py"]
```

### Переменные окружения
```python
import os
from client import TTSConfig

config = TTSConfig()
config.update_config(
    api_alltalk_ip_port=os.getenv('TTS_SERVER_URL', '80.251.139.116:7851'),
    max_retries=int(os.getenv('TTS_MAX_RETRIES', '3')),
    cache_ttl=int(os.getenv('TTS_CACHE_TTL', '300'))
)
```

## 📈 Оптимизация производительности

### 1. Пул соединений
```python
# Клиент автоматически использует пул соединений
async with TTSStreamingClient() as client:
    # Настройки пула в конструкторе aiohttp.TCPConnector
    # limit=100, limit_per_host=30
    pass
```

### 2. Параллельная обработка
```python
async def process_multiple_texts(texts: list):
    async with TTSStreamingClient() as client:
        if await client.initialize():
            tasks = [
                client.generate_tts_from_text(text) 
                for text in texts
            ]
            
            # Параллельная обработка
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
```

### 3. Умное кэширование
```python
# Настройка TTL кэша в зависимости от нагрузки
config = TTSConfig()

# Высокая нагрузка - долгий кэш
config.update_config(cache_ttl=3600)  # 1 час

# Разработка - короткий кэш  
config.update_config(cache_ttl=60)    # 1 минута
```

## 🔧 Расширенная конфигурация

### Полный список параметров конфигурации
```json
{
    "api_alltalk_protocol": "http://",
    "api_alltalk_ip_port": "80.251.139.116:7851",
    "api_connection_timeout": 5,
    "max_retries": 3,
    "retry_delay": 1.0,
    "cache_ttl": 300,
    "default_voice": "female_01.wav",
    "default_language": "en", 
    "default_chunk_size": 200,
    "default_chunk_timeout": 2.0,
    
    // Автоматически сохраняемые метрики
    "last_successful_voice": "female_01.wav",
    "last_successful_language": "en",
    "last_successful_generation": 1703123456.789,
    "last_test_chunks": 5,
    "last_test_size": 48576,
    "last_test_time": 1703123456.789
}
```

## 🆘 Устранение неполадок

### Частые проблемы и решения

#### 1. Сервер не отвечает
```python
# Проверка доступности
async with TTSStreamingClient() as client:
    if not await client.check_server_ready():
        print("❌ Сервер недоступен")
        print(f"🔍 Проверьте URL: {client.config.base_url}")
        print("🔧 Проверьте настройки в tts_config.json")
```

#### 2. Ошибки аутентификации  
```python
# Для HTTPS с аутентификацией
config = TTSConfig()
config.update_config(
    api_alltalk_protocol="https://",
    api_alltalk_ip_port="secure-server.com:443"
)
```

#### 3. Проблемы с голосами
```python
async with TTSStreamingClient() as client:
    if await client.initialize():
        voices = await client.get_available_voices()
        if not voices:
            print("⚠️ Голоса недоступны")
            await client.reload_config()  # Попытка обновления
```

#### 4. Медленная работа
```python
# Увеличение таймаутов для медленных серверов
config = TTSConfig()
config.update_config(
    api_connection_timeout=30,
    cache_ttl=1800,  # Увеличиваем кэш
    max_retries=1    # Уменьшаем повторы
)
```

## 📚 Дополнительные ресурсы

- 📖 [Официальная документация AllTalk](https://github.com/erew123/alltalk_tts/wiki)
- 🔧 [Рекомендации по интеграции](api_recomendations.md)
- 🌐 [API документация на русском](api.md)
- 🧪 [Примеры интеграции](quick_start.py)

## 🤝 Поддержка и обратная связь

Если у вас возникли вопросы или предложения по улучшению клиента:

1. 🐛 **Сообщения об ошибках**: Включите детальные логи и конфигурацию
2. 💡 **Предложения**: Опишите желаемую функциональность
3. 📊 **Производительность**: Поделитесь метриками и сценариями использования

---

**Версия**: 2.0  
**Совместимость**: AllTalk TTS API v1.0+  
**Python**: 3.8+  
**Лицензия**: MIT 
"""
Упрощенный клиент для AllTalk TTS API с поддержкой потокового аудио
Фокус на стриминге и чанковании текста
"""

import asyncio
import re
import time
import json
import os
from typing import Iterator, Optional, AsyncIterator, List, Dict, Any
import aiohttp
import requests
from urllib.parse import urlencode, quote
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TTSConfig:
    """Простая конфигурация TTS клиента"""
    
    def __init__(self, config_file: str = "tts_config.json"):
        self.config_file = config_file
        self.default_config = {
            "api_alltalk_protocol": "http://",
            "api_alltalk_ip_port": "80.251.139.116:7851",
            "api_connection_timeout": 10,
            "default_voice": "Arnold.wav",
            "default_language": "ru",
            "default_chunk_size": 100,
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Загружает конфигурацию из файла или создает с настройками по умолчанию"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Дополняем недостающие ключи значениями по умолчанию
                for key, value in self.default_config.items():
                    config.setdefault(key, value)
                return config
            else:
                logger.info(f"Создается новый файл конфигурации {self.config_file}")
                self.save_config(self.default_config)
                return self.default_config.copy()
        except Exception as e:
            logger.error(f"Ошибка загрузки конфигурации: {e}")
            return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any] = None) -> None:
        """Сохраняет конфигурацию в файл"""
        try:
            config_to_save = config or self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Ошибка сохранения конфигурации: {e}")
    
    @property
    def base_url(self) -> str:
        """Возвращает базовый URL для API"""
        return f"{self.config['api_alltalk_protocol']}{self.config['api_alltalk_ip_port']}"


class TTSStreamingClient:
    """Упрощенный клиент для потокового TTS API AllTalk"""
    
    def __init__(self, config_file: str = "tts_config.json"):
        self.config = TTSConfig(config_file)
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        """Асинхронный контекстный менеджер - вход"""
        timeout = aiohttp.ClientTimeout(total=self.config.config['api_connection_timeout'])
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный контекстный менеджер - выход"""
        if self.session:
            await self.session.close()
    
    def chunk_text(self, text: str, max_chunk_size: int = None) -> List[str]:
        """
        Разбивает текст на чанки по знакам препинания
        
        Args:
            text: Исходный текст
            max_chunk_size: Максимальный размер чанка
            
        Returns:
            Список чанков текста
        """
        if max_chunk_size is None:
            max_chunk_size = self.config.config['default_chunk_size']
            
        if not text.strip():
            return []
            
        # Знаки препинания для разбиения (в порядке приоритета)
        sentence_endings = r'[.!?]+\s+'
        clause_endings = r'[;,]\s+'
        
        chunks = []
        current_chunk = ""
        
        # Сначала разбиваем по предложениям
        sentences = re.split(sentence_endings, text)
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Если предложение слишком длинное, разбиваем по запятым/точкам с запятой
            if len(sentence) > max_chunk_size:
                clauses = re.split(clause_endings, sentence)
                for j, clause in enumerate(clauses):
                    clause = clause.strip()
                    if not clause:
                        continue
                        
                    # Если клауза все еще слишком длинная, разбиваем по словам
                    if len(clause) > max_chunk_size:
                        words = clause.split()
                        temp_chunk = ""
                        for word in words:
                            if len(temp_chunk + " " + word) > max_chunk_size and temp_chunk:
                                chunks.append(temp_chunk.strip())
                                temp_chunk = word
                            else:
                                temp_chunk = temp_chunk + " " + word if temp_chunk else word
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                    else:
                        chunks.append(clause)
            else:
                # Проверяем, поместится ли предложение в текущий чанк
                if len(current_chunk + " " + sentence) > max_chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk = current_chunk + " " + sentence if current_chunk else sentence
        
        # Добавляем последний чанк
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
            
        return chunks
    
    async def stream_tts_chunk(
        self, 
        text: str, 
        voice: str = None, 
        language: str = None,
        output_file: str = None
    ) -> bytes:
        """
        Генерирует TTS для одного чанка текста через GET запрос как в документации
        
        Args:
            text: Текст для преобразования
            voice: Голос для использования
            language: Язык
            output_file: Имя выходного файла
            
        Returns:
            Аудиоданные в байтах
        """
        if not text.strip():
            return b""
        
        if not self.session:
            raise RuntimeError("Клиент не инициализирован. Используйте async with.")
        
        # Используем значения по умолчанию если не указаны
        voice = voice or self.config.config['default_voice']
        language = language or self.config.config['default_language']
        
        # Генерируем уникальное имя файла если не указано
        if not output_file:
            timestamp = int(time.time() * 1000)
            output_file = f"tts_chunk_{timestamp}.wav"
        
        # Создаем URL с параметрами как в документации
        params = {
            "text": text.strip(),
            "voice": voice,
            "language": language,
            "output_file": output_file
        }
        
        # Кодируем параметры для URL
        encoded_params = urlencode(params, quote_via=quote)
        streaming_url = f"{self.config.base_url}/api/tts-generate-streaming?{encoded_params}"
        
        logger.info(f"🌊 Запрос TTS: '{text[:50]}...' через GET")
        
        try:
            # Используем GET запрос как в JavaScript примере
            async with self.session.get(streaming_url) as response:
                if response.status == 200:
                    audio_data = await response.read()
                    logger.info(f"✅ Получено {len(audio_data)} байт аудио")
                    return audio_data
                else:
                    logger.error(f"❌ Ошибка TTS API: {response.status}")
                    error_text = await response.text()
                    logger.error(f"❌ Ответ сервера: {error_text}")
                    return b""
                    
        except Exception as e:
            logger.error(f"❌ Ошибка при генерации TTS: {e}")
            return b""
    
    async def generate_tts_from_text(
        self,
        text: str,
        voice: str = None,
        language: str = None,
        max_chunk_size: int = None
    ) -> AsyncIterator[bytes]:
        """
        Генерирует TTS из статического текста, разбитого на чанки
        """
        voice = voice or self.config.config['default_voice']
        language = language or self.config.config['default_language']
        max_chunk_size = max_chunk_size or self.config.config['default_chunk_size']
        
        chunks = self.chunk_text(text, max_chunk_size)
        logger.info(f"📝 Разбито на {len(chunks)} чанков")
        
        for i, chunk in enumerate(chunks, 1):
            if chunk.strip():
                logger.info(f"🎵 Обрабатываем чанк {i}/{len(chunks)}: '{chunk[:30]}...'")
                audio_data = await self.stream_tts_chunk(chunk, voice, language)
                if audio_data:
                    yield audio_data
                    # Небольшая задержка между чанками
                    await asyncio.sleep(0.1)
    
    async def stream_tts_from_iterator(
        self,
        text_iterator: AsyncIterator[str],
        voice: str = None,
        language: str = None,
        max_chunk_size: int = None,
        chunk_timeout: float = 2.0
    ) -> AsyncIterator[bytes]:
        """
        Генерирует TTS из итератора текста (например, от Ollama)
        """
        voice = voice or self.config.config['default_voice']
        language = language or self.config.config['default_language']
        max_chunk_size = max_chunk_size or self.config.config['default_chunk_size']
        
        buffer = ""
        last_update_time = time.time()
        
        async for text_part in text_iterator:
            buffer += text_part
            current_time = time.time()
            
            # Проверяем, нужно ли отправить чанк
            should_send = False
            
            # Если буфер содержит завершенное предложение
            if re.search(r'[.!?]+\s+', buffer):
                should_send = True
            # Если буфер слишком большой
            elif len(buffer) > max_chunk_size:
                should_send = True
            # Если прошло слишком много времени с последнего обновления
            elif current_time - last_update_time > chunk_timeout and buffer.strip():
                should_send = True
            
            if should_send:
                chunks = self.chunk_text(buffer, max_chunk_size)
                
                # Обрабатываем все чанки кроме последнего (который может быть неполным)
                for chunk in chunks[:-1]:
                    if chunk.strip():
                        audio_data = await self.stream_tts_chunk(chunk, voice, language)
                        if audio_data:
                            yield audio_data
                
                # Оставляем последний чанк в буфере
                buffer = chunks[-1] if chunks else ""
                last_update_time = current_time
        
        # Обрабатываем оставшийся текст в буфере
        if buffer.strip():
            final_chunks = self.chunk_text(buffer, max_chunk_size)
            for chunk in final_chunks:
                if chunk.strip():
                    audio_data = await self.stream_tts_chunk(chunk, voice, language)
                    if audio_data:
                        yield audio_data


# Синхронная версия для быстрого использования
class SyncTTSClient:
    """Синхронная обертка для TTSStreamingClient"""
    
    def __init__(self, config_file: str = "tts_config.json"):
        self.config = TTSConfig(config_file)
    
    def chunk_text(self, text: str, max_chunk_size: int = None) -> List[str]:
        """Синхронная версия разбиения текста на чанки"""
        max_chunk_size = max_chunk_size or self.config.config['default_chunk_size']
        client = TTSStreamingClient(self.config.config_file)
        return client.chunk_text(text, max_chunk_size)


# Функция для простого тестирования
async def simple_test():
    """Простой тест клиента"""
    async with TTSStreamingClient() as client:
        # Тестируем чанкование
        test_text = "Привет! Как дела? Это тестовый текст для проверки работы TTS."
        chunks = client.chunk_text(test_text, max_chunk_size=30)
        logger.info(f"📝 Разбито на чанки: {chunks}")
        
        # Тестируем TTS
        if chunks:
            audio_data = await client.stream_tts_chunk(chunks[0])
            if audio_data:
                logger.info(f"🎵 Получено аудио: {len(audio_data)} байт")
                return True
        
        return False


if __name__ == "__main__":
    asyncio.run(simple_test())

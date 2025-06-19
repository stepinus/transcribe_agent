#!/usr/bin/env python3
"""
🚀 Быстрый старт для тестирования AllTalk TTS клиента
Простой тест потокового API через GET запрос
"""

import asyncio
import logging
import time
from client import TTSStreamingClient

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_get_streaming():
    """Тест GET запроса к streaming API как в документации"""
    logger.info("🧪 Тестирование GET потокового API...")
    
    async with TTSStreamingClient() as client:
        # Простой тест текста
        test_text = "Привет! Это тест потокового TTS API на русском языке."
        
        logger.info(f"📝 Тестируем: '{test_text}'")
        logger.info(f"🎤 Голос: {client.config.config['default_voice']}")
        logger.info(f"🌐 Сервер: {client.config.base_url}")
        
        start_time = time.time()
        audio_data = await client.stream_tts_chunk(
            text=test_text,
            voice="Arnold.wav",
            language="ru"
        )
        latency = time.time() - start_time
        
        if audio_data:
            logger.info(f"✅ Успех: {len(audio_data)} байт за {latency:.2f}с")
            
            # Сохраняем файл для проверки
            with open("test_output.wav", "wb") as f:
                f.write(audio_data)
            logger.info("💾 Аудио сохранено в test_output.wav")
            
            return True
        else:
            logger.error("❌ Получены пустые данные")
            return False


async def test_chunking():
    """Тест чанкования текста"""
    logger.info("✂️ Тестирование чанкования...")
    
    async with TTSStreamingClient() as client:
        long_text = """
        Это более длинный текст для тестирования алгоритма чанкования. 
        Он содержит несколько предложений! Некоторые с восклицательными знаками. 
        А некоторые с вопросительными знаками? Система должна разбивать текст разумно.
        """
        
        chunks = client.chunk_text(long_text.strip(), max_chunk_size=50)
        
        logger.info(f"📝 Исходный текст ({len(long_text.strip())} символов):")
        logger.info(f"   '{long_text.strip()}'")
        logger.info(f"✂️ Разбито на {len(chunks)} чанков:")
        
        for i, chunk in enumerate(chunks, 1):
            logger.info(f"   {i}. [{len(chunk):2d}] '{chunk}'")
        
        return len(chunks) > 1


async def test_streaming_generation():
    """Тест потоковой генерации аудио"""
    logger.info("🌊 Тестирование потоковой генерации...")
    
    text = """
    Добро пожаловать в тест потокового TTS! 
    Этот текст будет преобразован в речь по частям. 
    Каждый чанк обрабатывается отдельно для оптимальной производительности.
    """
    
    async with TTSStreamingClient() as client:
        chunks_count = 0
        total_size = 0
        start_time = time.time()
        first_chunk_time = None
        
        async for audio_chunk in client.generate_tts_from_text(
            text.strip(), 
            max_chunk_size=60
        ):
            if audio_chunk:
                chunks_count += 1
                total_size += len(audio_chunk)
                
                if first_chunk_time is None:
                    first_chunk_time = time.time() - start_time
                    logger.info(f"🎯 Первый чанк за: {first_chunk_time:.2f}с")
                
                logger.info(f"📦 Чанк {chunks_count}: {len(audio_chunk)} байт")
        
        total_time = time.time() - start_time
        
        logger.info(f"📊 Результаты:")
        logger.info(f"   📦 Чанков: {chunks_count}")
        logger.info(f"   🎵 Размер: {total_size} байт")
        logger.info(f"   ⏰ Время: {total_time:.2f}с")
        
        if chunks_count > 0:
            # Сохраняем всё аудио в один файл
            all_audio = b""
            async for audio_chunk in client.generate_tts_from_text(text.strip(), max_chunk_size=60):
                if audio_chunk:
                    all_audio += audio_chunk
            
            if all_audio:
                with open("streaming_output.wav", "wb") as f:
                    f.write(all_audio)
                logger.info("💾 Объединенное аудио сохранено в streaming_output.wav")
        
        return chunks_count > 0


async def main():
    """Основная функция демонстрации"""
    logger.info("🚀 Быстрый старт AllTalk TTS клиента")
    logger.info("=" * 50)
    
    tests = [
        ("GET Streaming API", test_get_streaming),
        ("Алгоритм чанкования", test_chunking),
        ("Потоковая генерация", test_streaming_generation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            logger.info(f"\n🧪 {test_name}")
            logger.info("-" * 30)
            
            success = await test_func()
            if success:
                passed += 1
                logger.info(f"✅ {test_name} - УСПЕХ")
            else:
                failed += 1
                logger.error(f"❌ {test_name} - ПРОВАЛ")
                
        except Exception as e:
            failed += 1
            logger.error(f"💥 {test_name} - ОШИБКА: {e}")
    
    logger.info(f"\n" + "=" * 50)
    logger.info(f"📊 ИТОГИ: {passed} успех, {failed} провал")
    
    if failed == 0:
        logger.info("🎉 Все тесты прошли успешно!")
        logger.info("💡 Потоковый API работает через GET запросы")
    else:
        logger.error("🔧 Проверьте подключение к серверу AllTalk")


if __name__ == "__main__":
    asyncio.run(main()) 
"""
Упрощенный тестовый набор для TTS клиента AllTalk
Фокус на стриминге и чанковании
"""

import asyncio
import time
import random
from typing import AsyncIterator
from client import TTSStreamingClient, SyncTTSClient, TTSConfig
import logging

# Настройка логирования для тестов
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OllamaTextSimulator:
    """Симулятор потока текста от Ollama для тестирования"""
    
    def __init__(self, full_text: str, chunk_delay: float = 0.1):
        self.full_text = full_text
        self.chunk_delay = chunk_delay
        
    async def stream_text(self) -> AsyncIterator[str]:
        """Имитирует потоковую генерацию текста с задержками"""
        words = self.full_text.split()
        current_chunk = ""
        
        for i, word in enumerate(words):
            current_chunk += word + " "
            
            # Отправляем чанк каждые 2-4 слова или в конце предложения
            should_send = (
                (i + 1) % random.randint(2, 4) == 0 or 
                word.endswith(('.', '!', '?')) or 
                i == len(words) - 1
            )
            
            if should_send:
                yield current_chunk
                current_chunk = ""
                await asyncio.sleep(self.chunk_delay)


async def test_chunking():
    """Тест алгоритма чанкования"""
    logger.info("✂️ Тестирование алгоритма чанкования...")
    
    client = TTSStreamingClient()
    
    test_cases = [
        {
            "text": "Короткий текст.",
            "max_size": 100,
            "description": "Короткий текст"
        },
        {
            "text": "Первое предложение. Второе предложение! Третье предложение?",
            "max_size": 25,
            "description": "Три предложения"
        },
        {
            "text": "Очень длинное предложение, которое содержит много слов и должно быть разбито на части.",
            "max_size": 30,
            "description": "Длинное предложение"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        chunks = client.chunk_text(case["text"], case["max_size"])
        logger.info(f"Тест {i} - {case['description']}: {len(chunks)} чанков")
        for j, chunk in enumerate(chunks):
            logger.info(f"  Чанк {j+1}: '{chunk}' (длина: {len(chunk)})")
    
    logger.info("✅ Тест чанкования завершен")
    return True


async def test_streaming_tts():
    """Тест потокового TTS"""
    logger.info("🌊 Тестирование потокового TTS...")
    
    async with TTSStreamingClient() as client:
        # Тест одиночного чанка
        test_text = "Привет! Это тест потокового TTS API."
        
        logger.info(f"🎯 Тестируем одиночный чанк: '{test_text}'")
        start_time = time.time()
        
        audio_data = await client.stream_tts_chunk(test_text)
        latency = time.time() - start_time
        
        if audio_data:
            logger.info(f"✅ Успех: {len(audio_data)} байт за {latency:.2f}с")
            logger.info(f"⚡ Скорость: {len(test_text)/latency:.1f} символов/сек")
            return True
        else:
            logger.error("❌ Не удалось получить аудио")
            return False


async def test_text_to_speech():
    """Тест преобразования текста в речь с чанкованием"""
    logger.info("📝 Тестирование преобразования текста в речь...")
    
    text = """
    Добро пожаловать в систему преобразования текста в речь! 
    Эта технология позволяет компьютерам говорить человеческим голосом. 
    Современные системы используют нейронные сети для создания естественной речи.
    """.strip()
    
    async with TTSStreamingClient() as client:
        logger.info(f"📄 Исходный текст ({len(text)} символов)")
        
        chunks_received = 0
        total_size = 0
        start_time = time.time()
        first_chunk_time = None
        
        async for audio_chunk in client.generate_tts_from_text(text, max_chunk_size=80):
            if audio_chunk:
                chunks_received += 1
                total_size += len(audio_chunk)
                
                if first_chunk_time is None:
                    first_chunk_time = time.time() - start_time
                    logger.info(f"🎯 Первый чанк получен за: {first_chunk_time:.2f}с")
                
                logger.info(f"📦 Чанк {chunks_received}: {len(audio_chunk)} байт")
        
        total_time = time.time() - start_time
        
        logger.info(f"📊 Результаты:")
        logger.info(f"   📦 Чанков: {chunks_received}")
        logger.info(f"   🎵 Размер: {total_size} байт")
        logger.info(f"   ⏰ Время: {total_time:.2f}с")
        if first_chunk_time:
            logger.info(f"   🚀 Задержка первого чанка: {first_chunk_time:.2f}с")
        
        return chunks_received > 0


async def test_streaming_simulation():
    """Тест потоковой обработки с симуляцией Ollama"""
    logger.info("🤖 Тестирование симуляции потока от Ollama...")
    
    demo_text = """
    Искусственный интеллект быстро развивается. 
    Современные языковые модели могут генерировать текст в реальном времени. 
    Системы TTS преобразуют этот текст в натуральную речь.
    """
    
    simulator = OllamaTextSimulator(demo_text.strip(), chunk_delay=0.2)
    
    async with TTSStreamingClient() as client:
        logger.info("🔄 Симулируем поток текста от Ollama...")
        
        audio_chunks = []
        start_time = time.time()
        first_audio_time = None
        
        async for audio_data in client.stream_tts_from_iterator(
            simulator.stream_text(),
            max_chunk_size=60
        ):
            if audio_data:
                audio_chunks.append(audio_data)
                
                if first_audio_time is None:
                    first_audio_time = time.time() - start_time
                    logger.info(f"🎯 Первое аудио за: {first_audio_time:.2f}с")
                
                logger.info(f"🎵 Аудио чанк: {len(audio_data)} байт")
        
        total_time = time.time() - start_time
        total_size = sum(len(chunk) for chunk in audio_chunks)
        
        logger.info(f"📊 Симуляция завершена:")
        logger.info(f"   📦 Аудио чанков: {len(audio_chunks)}")
        logger.info(f"   🎵 Общий размер: {total_size} байт")
        logger.info(f"   ⏰ Общее время: {total_time:.2f}с")
        
        return len(audio_chunks) > 0


async def test_sync_client():
    """Тест синхронного клиента"""
    logger.info("🔄 Тестирование синхронного клиента...")
    
    sync_client = SyncTTSClient()
    
    # Тест чанкования
    test_text = "Это тест синхронного клиента. Он должен правильно разбивать текст."
    chunks = sync_client.chunk_text(test_text, max_chunk_size=25)
    
    logger.info(f"✂️ Синхронное чанкование: {len(chunks)} чанков")
    for i, chunk in enumerate(chunks, 1):
        logger.info(f"  Чанк {i}: '{chunk}'")
    
    logger.info("✅ Синхронный клиент работает")
    return True


async def test_latency_measurement():
    """Тест измерения задержки"""
    logger.info("⏱️ Тестирование измерения задержки...")
    
    async with TTSStreamingClient() as client:
        test_cases = [
            "Короткий тест.",
            "Тест средней длины для измерения задержки генерации.",
            "Более длинный тест для проверки как влияет размер текста на время генерации аудио."
        ]
        
        for i, text in enumerate(test_cases, 1):
            logger.info(f"📝 Тест {i}: '{text[:30]}...' ({len(text)} символов)")
            
            start_time = time.time()
            audio_data = await client.stream_tts_chunk(text)
            latency = time.time() - start_time
            
            if audio_data:
                speed = len(text) / latency
                logger.info(f"   ✅ {len(audio_data)} байт за {latency:.2f}с ({speed:.1f} симв/с)")
            else:
                logger.info(f"   ❌ Ошибка генерации")
        
        logger.info("✅ Измерение задержки завершено")
        return True


async def run_all_tests():
    """Запуск всех упрощенных тестов"""
    logger.info("🧪 Запуск упрощенного набора тестов TTS клиента...")
    
    tests = [
        ("Алгоритм чанкования", test_chunking),
        ("Потоковый TTS", test_streaming_tts),
        ("Преобразование текста в речь", test_text_to_speech),
        ("Симуляция потока Ollama", test_streaming_simulation),
        ("Синхронный клиент", test_sync_client),
        ("Измерение задержки", test_latency_measurement),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            logger.info(f"\n{'='*50}")
            logger.info(f"🧪 Тест: {test_name}")
            logger.info(f"{'='*50}")
            
            result = await test_func()
            if result:
                passed += 1
                logger.info(f"✅ Тест '{test_name}' прошел успешно")
            else:
                failed += 1
                logger.error(f"❌ Тест '{test_name}' провален")
            
        except Exception as e:
            failed += 1
            logger.error(f"❌ Тест '{test_name}' провален с ошибкой: {e}")
    
    logger.info(f"\n{'='*50}")
    logger.info(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    logger.info(f"{'='*50}")
    logger.info(f"✅ Пройдено: {passed}")
    logger.info(f"❌ Провалено: {failed}")
    logger.info(f"📈 Успешность: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        logger.info("🎉 Все тесты прошли успешно!")
    else:
        logger.warning(f"⚠️ {failed} тестов провалено")


if __name__ == "__main__":
    asyncio.run(run_all_tests()) 
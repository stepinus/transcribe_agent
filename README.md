# УМКА ИИ - Агент Транскрибатора

Веб-приложение для транскрипции встреч в реальном времени с возможностью анализа и Q&A с использованием ИИ.

## Возможности

- 🎤 **Живая транскрипция** - запись и транскрипция встреч в реальном времени
- 📝 **Анализ встреч** - автоматическое создание саммари и основных тезисов
- ❓ **Q&A с ИИ** - возможность задавать вопросы о содержании встречи
- 👥 **Определение спикеров** - четкое разделение реплик по участникам
- 📱 **Адаптивный дизайн** - работает на всех устройствах

## Технологии

- **Frontend**: Next.js 15, React, TypeScript
- **UI/UX**: Tailwind CSS, shadcn/ui
- **Иконки**: Lucide React

## Структура интерфейса

### Шапка
- Логотип "УМКА ИИ онлайн"
- Меню-бургер с опциями (настройки, история, экспорт, помощь)

### Основной контент (2 колонки)

#### Левая колонка (1/3 ширины)
- **Транскрипт встречи** - живой список реплик с указанием спикера
- Автоматическое обновление при записи

#### Правая колонка (2/3 ширины)
- **Верхняя часть**: Основные тезисы и саммари встречи
- **Нижняя часть**: Интерактивные вопросы и ответы от ИИ

### Элементы управления
- Плавающая кнопка записи (начать/остановить)
- Поле ввода вопросов с кнопкой отправки

## Запуск проекта

1. Установите зависимости:
```bash
npm install
```

2. Запустите сервер разработки:
```bash
npm run dev
```

3. Откройте [http://localhost:3000](http://localhost:3000) в браузере

## Mock данные

В текущей версии используются тестовые данные для демонстрации интерфейса:
- Пример транскрипта встречи с тремя участниками
- Основные тезисы обсуждения
- Примеры вопросов и ответов

## Будущие возможности

- Интеграция с API транскрипции (например, OpenAI Whisper)
- Подключение LLM для анализа и ответов на вопросы
- Экспорт транскриптов в различные форматы
- Сохранение истории встреч
- Настройки качества записи и языка
- Интеграция с календарем для автоматического планирования

## Команды разработки

```bash
# Запуск в режиме разработки
npm run dev

# Сборка проекта
npm run build

# Запуск production версии
npm start

# Проверка типов TypeScript
npm run type-check
```

## Структура проекта

```
src/
├── app/                    # App Router страницы
│   ├── page.tsx           # Главная страница
│   ├── layout.tsx         # Основной layout
│   └── globals.css        # Глобальные стили
├── components/            # React компоненты
│   └── ui/               # shadcn/ui компоненты
└── lib/                  # Утилиты и конфигурация
    └── utils.ts          # Общие функции
```

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

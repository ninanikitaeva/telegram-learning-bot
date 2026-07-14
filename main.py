import os
from dotenv import load_dotenv

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters
)

from states import (
    CHOOSING_LANG,
    CHOOSING_LESSON,
    DOING_TASK
)

from handlers import (
    start,
    choose_lang,
    choose_lesson,
    check_task,
    cancel
)


# Загружаем .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


if not TOKEN:
    print("❌ BOT_TOKEN не найден в .env")
    exit()


# Создаём приложение
app = Application.builder().token(TOKEN).build()


# Создаём диалог
conversation = ConversationHandler(

    entry_points=[
        CommandHandler("start", start)
    ],


    states={

        # Выбор языка
        CHOOSING_LANG: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                choose_lang
            )
        ],


        # Выбор урока
        CHOOSING_LESSON: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                choose_lesson
            )
        ],


        # Практическое задание
        DOING_TASK: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                check_task
            )
        ],
    },


    fallbacks=[
        CommandHandler("cancel", cancel)
    ]

)


# Добавляем только ConversationHandler
app.add_handler(conversation)


print("✅ Бот запущен")


# Запуск
app.run_polling()
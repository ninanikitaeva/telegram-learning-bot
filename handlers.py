from states import CHOOSING_LANG, CHOOSING_LESSON, DOING_TASK
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler


from keyboards import (
    lang_keyboard,
    back_keyboard,
    lesson_nav_keyboard,
    after_task_keyboard
)

from lessons.list import lessons

from lessons.python import (
    python_lessons_content,
    python_practice_tasks
)

from lessons.cpp import (
    cpp_lessons_content,
    cpp_practice_tasks
)

from lessons.java import (
    java_lessons_content,
    java_practice_tasks
)

from lessons.javascript import (
    javascript_lessons_content,
    javascript_practice_tasks
)

from lessons.csharp import (
    csharp_lessons_content,
    csharp_practice_tasks
)

from lessons.answers import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "👋 Привет!\n\n"
        "Я бот для изучения языков программирования.\n\n"
        "Выбери язык:",
        reply_markup=ReplyKeyboardMarkup(
            lang_keyboard,
            resize_keyboard=True
        ),
    )

    return CHOOSING_LANG


async def choose_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text



    # 👤 Профиль
    if user_choice == "👤 Профиль":

        score = context.user_data.get("score", 0)

        await update.message.reply_text(
            f"👤 Ваш профиль\n\n"
            f"🏆 Баллы: {score}"
        )

        return CHOOSING_LANG


    # Выбор языка
    if user_choice in lessons:

        context.user_data["lang"] = user_choice

        lesson_buttons = [[lesson] for lesson in lessons[user_choice]]

        full_keyboard = lesson_buttons + back_keyboard

        await update.message.reply_text(
            f"📚 Ты выбрал: {user_choice}\n\n"
            "Выбери урок:",
            reply_markup=ReplyKeyboardMarkup(
                full_keyboard,
                resize_keyboard=True
            ),
        )

        return CHOOSING_LESSON

    await update.message.reply_text(
        "❌ Используй кнопки ниже."
    )

    return CHOOSING_LANG


async def check_task(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_code = update.message.text


    # Назад к выбору языка
    if user_code == "Назад к выбору языка":

        await update.message.reply_text(
            "🔙 Выбери язык:",
            reply_markup=ReplyKeyboardMarkup(
                lang_keyboard,
                resize_keyboard=True
            )
        )

        return CHOOSING_LANG

    if user_code == "⬅️ Назад к уроку":

        current_lang = context.user_data.get("lang")
        lesson_index = context.user_data.get("lesson_index", 0)

        lesson_name = lessons[current_lang][lesson_index]

        if current_lang == "Python":
            lesson_text = python_lessons_content.get(lesson_name)

        elif current_lang == "C++":
            lesson_text = cpp_lessons_content.get(lesson_name)

        elif current_lang == "Java":
            lesson_text = java_lessons_content.get(lesson_name)

        elif current_lang == "JavaScript":
            lesson_text = javascript_lessons_content.get(lesson_name)

        elif current_lang == "C#":
            lesson_text = csharp_lessons_content.get(lesson_name)

        else:
            lesson_text = "Урок не найден."

        await update.message.reply_text(
            lesson_text,
            reply_markup=ReplyKeyboardMarkup(
                lesson_nav_keyboard,
                resize_keyboard=True
            )
        )

        return CHOOSING_LESSON

    # Кнопка следующий урок
    if user_code == "➡️ Следующий урок":

        current_lang = context.user_data.get("lang")
        current_index = context.user_data.get("lesson_index", 0)

        current_index += 1

        if current_index >= len(lessons[current_lang]):
            await update.message.reply_text(
                "🎉 Ты прошёл все уроки этого языка!",
                reply_markup=ReplyKeyboardMarkup(
                    lang_keyboard,
                    resize_keyboard=True
                )
            )
            return CHOOSING_LANG


        context.user_data["lesson_index"] = current_index

        lesson_name = lessons[current_lang][current_index]


        if current_lang == "Python":
            lesson_text = python_lessons_content.get(lesson_name)

        elif current_lang == "C++":
            lesson_text = cpp_lessons_content.get(lesson_name)

        elif current_lang == "Java":
            lesson_text = java_lessons_content.get(lesson_name)

        elif current_lang == "JavaScript":
            lesson_text = javascript_lessons_content.get(lesson_name)

        elif current_lang == "C#":
            lesson_text = csharp_lessons_content.get(lesson_name)


        await update.message.reply_text(
            lesson_text,
            reply_markup=ReplyKeyboardMarkup(
                lesson_nav_keyboard,
                resize_keyboard=True
            )
        )

        return CHOOSING_LESSON



    # Кнопка предыдущий урок
    if user_code == "⬅️ Предыдущий урок":

        current_lang = context.user_data.get("lang")
        current_index = context.user_data.get("lesson_index", 0)

        current_index -= 1


        if current_index < 0:
            await update.message.reply_text(
                "🔙 Выбор языка:",
                reply_markup=ReplyKeyboardMarkup(
                    lang_keyboard,
                    resize_keyboard=True
                )
            )

            return CHOOSING_LANG


        context.user_data["lesson_index"] = current_index

        lesson_name = lessons[current_lang][current_index]


        if current_lang == "Python":
            lesson_text = python_lessons_content.get(lesson_name)


        await update.message.reply_text(
            lesson_text,
            reply_markup=ReplyKeyboardMarkup(
                lesson_nav_keyboard,
                resize_keyboard=True
            )
        )

        return CHOOSING_LESSON

    current_lang = context.user_data.get("lang")
    lesson_index = context.user_data.get("lesson_index", 0)

    lesson_name = lessons[current_lang][lesson_index]

    # Проверка практического задания Python

    # ---------------- ПРОВЕРКА ЗАДАНИЙ ----------------

    code = user_code.lower()

    current_lang = context.user_data.get("lang")

    correct_answer = answers[current_lang].get(lesson_name)


    # ---------- PYTHON ----------
    if current_lang == "Python":

        # Урок 1: print()
        if lesson_name == "Урок 1: Введение в Python":

            correct = (
                    "print" in code
                    and "добро пожаловать в python" in code
                    and "какой-то текст" not in code
            )


        elif lesson_name == "Урок 2: Переменные и типы данных":

            lines = code.split("\n")

            variables = []

            for line in lines:
                if "=" in line and "==" not in line:
                    variable = line.split("=")[0].strip()
                    variables.append(variable)

            printed = []

            for line in lines:
                if "print(" in line:
                    inside = line[line.find("(") + 1:line.find(")")].strip()
                    printed.append(inside)

            correct = (
                    len(variables) >= 2
                    and len(printed) >= 2
                    and variables[0] in printed
                    and variables[1] in printed
            )

        # Урок 3: условия
        elif lesson_name == "Урок 3: Условные операторы":

            correct = (
                    "if" in code
                    and "else" in code
                    and "temperature" in code
                    and "тепло" in code
            )


        # Урок 4: циклы
        elif lesson_name == "Урок 4: Циклы for и while":

            correct = (
                    "for" in code
                    and "range" in code
                    and "5" in code
                    and "15" in code
            )


        # Урок 5: функции
        elif lesson_name == "Урок 5: Функции":

            correct = (
                    "def" in code
                    and "multiply" in code
                    and "return" in code
                    and "*" in code
            )


        else:
            correct = False


        # ---------- C++ ----------
    elif current_lang == "C++":

        if lesson_name == "Урок 1: Введение в C++":

            correct = (
                    "cout" in code
                    and "привет" in code
                    and "мир" in code
            )


        elif lesson_name == "Урок 2: Переменные и типы данных":

            correct = (
                    "=" in code
                    and (
                            "int" in code
                            or "string" in code
                    )
                    and "name" in code
            )


        elif lesson_name == "Урок 3: Условные операторы":

            correct = (
                    "if" in code
                    and "else" in code
                    and "age" in code
            )


        elif lesson_name == "Урок 4: Циклы for, while и do while":

            correct = (
                    "for" in code
                    and "10" in code
            )


        elif lesson_name == "Урок 5: Функции":

            correct = (
                    "int" in code
                    and "square" in code
                    and "return" in code
            )


        else:
            correct = False
    # ---------- JAVA ----------
    elif current_lang == "Java":

        if lesson_name == "Урок 1: Введение в Java":

            correct = (
                    "system.out.println" in code
                    and "привет" in code
            )


        elif lesson_name == "Урок 2: Переменные и типы данных":

            correct = (
                    "=" in code
                    and (
                            "int" in code
                            or "string" in code
                    )
                    and "name" in code
            )


        elif lesson_name == "Урок 3: Условные операторы":

            correct = (
                    "if" in code
                    and "else" in code
            )


        elif lesson_name == "Урок 4: Циклы for и while":

            correct = (
                    "for" in code
                    and "10" in code
            )


        elif lesson_name == "Урок 5: Классы и объекты":

            correct = (
                    "class" in code
                    and "person" in code
                    and "new" in code
            )


        else:
            correct = False

    # ---------- JAVASCRIPT ----------
    elif current_lang == "JavaScript":

        if lesson_name == "Урок 1: Введение в JavaScript":

            correct = (
                    "console.log" in code
                    and "привет" in code
            )


        elif lesson_name == "Урок 2: Переменные и типы данных":

            correct = (
                    ("let" in code or "const" in code)
                    and "name" in code
            )


        elif lesson_name == "Урок 3: Условные операторы":

            correct = (
                    "if" in code
                    and "else" in code
            )


        elif lesson_name == "Урок 4: Циклы for и while":

            correct = (
                    "for" in code
                    and "10" in code
            )


        elif lesson_name == "Урок 5: Классы и объекты":

            correct = (
                    "class" in code
                    and "new" in code
            )


        else:
            correct = False

    # ---------- C# ----------
    elif current_lang == "C#":

        if lesson_name == "Урок 1: Введение в C#":

            correct = (
                    "console.writeline" in code
                    and "привет" in code
            )


        elif lesson_name == "Урок 2: Переменные и типы данных":

            correct = (
                    "=" in code
                    and (
                            "int" in code
                            or "string" in code
                    )
            )


        elif lesson_name == "Урок 3: Условные операторы":

            correct = (
                    "if" in code
                    and "else" in code
            )


        elif lesson_name == "Урок 4: Циклы for и while":

            correct = (
                    "for" in code
                    and "10" in code
            )


        elif lesson_name == "Урок 5: Классы и объекты":

            correct = (
                    "class" in code
                    and "person" in code
                    and "new" in code
            )


        else:
            correct = False

    if correct:
        # здесь твой код начисления баллов

        completed_tasks = context.user_data.get("completed_tasks", [])

        # Если задание уже выполнено
        if lesson_name in completed_tasks:
            await update.message.reply_text(
                "✅ Это задание уже выполнено!\n"
                "Баллы повторно не начисляются.",
                reply_markup=ReplyKeyboardMarkup(
                    after_task_keyboard,
                    resize_keyboard=True
                )
            )

            return DOING_TASK

        # Первое выполнение задания
        completed_tasks.append(lesson_name)
        context.user_data["completed_tasks"] = completed_tasks

        score = context.user_data.get("score", 0)
        score += 10
        context.user_data["score"] = score

        await update.message.reply_text(
            "🎉 Правильно!\n"
            "⭐ +10 баллов\n"
            f"🏆 Всего баллов: {score}",
            reply_markup=ReplyKeyboardMarkup(
                after_task_keyboard,
                resize_keyboard=True
            )
        )

    else:

        await update.message.reply_text(
            "❌ Ответ неверный.\n"
            "Попробуй ещё раз."
        )

    return DOING_TASK

# ---------------- ВЫБОР УРОКА ----------------
async def choose_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_choice = update.message.text

    # Практическое задание
    if user_choice == "📝 Практическое задание":

        current_lang = context.user_data.get("lang")
        lesson_index = context.user_data.get("lesson_index", 0)

        lesson_name = lessons[current_lang][lesson_index]

        if current_lang == "Python":
            task = python_practice_tasks.get(lesson_name)

        elif current_lang == "C++":
            task = cpp_practice_tasks.get(lesson_name)

        elif current_lang == "Java":
            task = java_practice_tasks.get(lesson_name)

        elif current_lang == "JavaScript":
            task = javascript_practice_tasks.get(lesson_name)

        elif current_lang == "C#":
            task = csharp_practice_tasks.get(lesson_name)

        else:
            task = "❌ Задание не найдено"

        await update.message.reply_text(
            task,
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["⬅️ Назад к уроку"]
                ],
                resize_keyboard=True
            )
        )

        context.user_data["waiting_for_code"] = True

        return DOING_TASK




    # Выполнение задания
    if user_choice == "✅ Выполнил задание":
        if user_choice == "✅ Выполнил задание":

            user_code = context.user_data.get("user_code")

            current_lang = context.user_data.get("lang")
            lesson_index = context.user_data.get("lesson_index", 0)

            lesson_name = lessons[current_lang][lesson_index]

            correct_answer = answers[current_lang].get(lesson_name)

            if user_code and user_code.strip() == correct_answer.strip():

                score = context.user_data.get("score", 0)
                score += 10
                context.user_data["score"] = score

                await update.message.reply_text(
                    "🎉 Правильно!\n"
                    "🏆 +10 баллов",

                    reply_markup=ReplyKeyboardMarkup(
                        lesson_nav_keyboard,
                        resize_keyboard=True
                    )
                )

            else:

                await update.message.reply_text(
                    "❌ Ошибка в коде.\n"
                    "Попробуй ещё раз."
                )

            context.user_data["waiting_for_code"] = False
            context.user_data["user_code"] = None
            context.user_data["task_done"] = True

            return CHOOSING_LESSON
    # Назад
    if user_choice == "Назад к выбору языка":
        await update.message.reply_text(
            "🔙 Выбери язык:",
            reply_markup=ReplyKeyboardMarkup(
                lang_keyboard,
                resize_keyboard=True
            ),
        )

        return CHOOSING_LANG

    current_lang = context.user_data.get("lang")

    current_lang = context.user_data.get("lang")

    # Переключение между уроками
    if user_choice in ["⬅️ Предыдущий урок", "➡️ Следующий урок"]:

        current_index = context.user_data.get("lesson_index", 0)

        if user_choice == "⬅️ Предыдущий урок":
            current_index -= 1
        else:
            current_index += 1

        lessons_list = lessons[current_lang]

        if current_index < 0:
            await update.message.reply_text(
                "🔙 Ты дошёл до начала курса. Выбери язык:",
                reply_markup=ReplyKeyboardMarkup(
                    lang_keyboard,
                    resize_keyboard=True
                ),
            )

            return CHOOSING_LANG

        if current_index >= len(lessons_list):
            await update.message.reply_text(
                "🎉 Ты просмотрел все уроки этого раздела. Выбери другой язык:",
                reply_markup=ReplyKeyboardMarkup(
                    lang_keyboard,
                    resize_keyboard=True
                ),
            )

            return CHOOSING_LANG

        context.user_data["lesson_index"] = current_index

        user_choice = lessons_list[current_index]

    if current_lang and user_choice in lessons[current_lang]:
        context.user_data["lesson_index"] = lessons[current_lang].index(user_choice)

        lesson_text = "Материал пока недоступен."

        # PYTHON
        if current_lang == "Python":
            lesson_text = python_lessons_content.get(user_choice)

        # C++
        elif current_lang == "C++":
            lesson_text = cpp_lessons_content.get(user_choice)

        # JAVA
        elif current_lang == "Java":
            lesson_text = java_lessons_content.get(user_choice)

        # JAVASCRIPT
        elif current_lang == "JavaScript":
            lesson_text = javascript_lessons_content.get(user_choice)

        # C#
        elif current_lang == "C#":
            lesson_text = csharp_lessons_content.get(user_choice)

        await update.message.reply_text(
            lesson_text,
            reply_markup=ReplyKeyboardMarkup(
                lesson_nav_keyboard,
                resize_keyboard=True
            ),
        )

    else:

        await update.message.reply_text(
            "❌ Выбери урок кнопками."
        )

    return CHOOSING_LESSON

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 До встречи!",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END
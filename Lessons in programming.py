from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv
import os
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)


load_dotenv(".env")


# ---------------- СОСТОЯНИЯ ----------------
CHOOSING_LANG, CHOOSING_LESSON = range(2)

# ---------------- СПИСОК УРОКОВ ----------------
lessons = {
    "Python": [
        "Урок 1: Введение в Python",
        "Урок 2: Переменные и типы данных",
        "Урок 3: Условные операторы",
        "Урок 4: Циклы for и while",
        "Урок 5: Функции",
    ],

    "C++": [
        "Урок 1: Введение в C++",
        "Урок 2: Переменные и типы данных",
        "Урок 3: Условные операторы",
        "Урок 4: Циклы for, while и do while",
        "Урок 5: Функции",
    ],

    "Java": [
        "Урок 1: Введение в Java",
        "Урок 2: Переменные и типы данных",
        "Урок 3: Условные операторы",
        "Урок 4: Циклы for и while",
        "Урок 5: Классы и объекты",
    ],

    "JavaScript": [
        "Урок 1: Введение в JavaScript",
        "Урок 2: Переменные и типы данных",
        "Урок 3: Условные операторы",
        "Урок 4: Циклы for и while",
        "Урок 5: Классы и объекты",
    ],

    "C#": [
        "Урок 1: Введение в C#",
        "Урок 2: Переменные и типы данных",
        "Урок 3: Условные операторы",
        "Урок 4: Циклы for и while",
        "Урок 5: Классы и объекты",
    ],
}

# ---------------- СОДЕРЖАНИЕ УРОКОВ PYTHON ----------------
python_lessons_content = {
    "Урок 1: Введение в Python": """
📘 Урок 1: Введение в Python

Python — популярный язык программирования.

✅ Используется для:
• создания сайтов
• анализа данных
• искусственного интеллекта
• автоматизации задач

Первая программа:

print("Привет, мир!")

Функция print() выводит текст на экран.
""",

    "Урок 2: Переменные и типы данных": """
📘 Урок 2: Переменные и типы данных

Переменная хранит данные.

Основные типы данных:
• str — строка
• int — целое число
• float — дробное число
• bool — True/False

Пример:

name = "Алексей"
age = 20
""",

    "Урок 3: Условные операторы": """
📘 Урок 3: Условные операторы

Условные операторы в Python (if, elif, else) управляют ходом выполнения программы, направляя её по разным веткам в зависимости от истинности условий. Они необходимы для создания гибких алгоритмов, способных реагировать на изменяющиеся данные.

Операторы сравнения:
== равно
!= не равно
> больше
< меньше
>= больше или равно
<= меньше или равно

Пример:

age = 18

if age >= 18:
    print("Доступ разрешён")
else:
    print("Доступ запрещён")
    
Логические операторы
-Условия можно объединять с помощью логических операторов and, or, и not:
and (логическое И) — возвращает True, если оба условия истинны.
or (логическое ИЛИ) — возвращает True, если хотя бы одно из условий истинно.
not (логическое НЕ) — инвертирует значение (например, not True превращается в False).

Пример:

temperature = 25
is_sunny = True

if temperature > 20 and is_sunny:
    print("Идем гулять!")

""",

    "Урок 4: Циклы for и while": """
📘 Урок 4: Циклы for и while

Цикл for в Python используется для итерации по последовательностям, таким как списки, строки, кортежи или диапазоны. Он позволяет выполнять код для каждого элемента последовательности.

Пример:

for i in range(5):
    print(i)

Цикл while используется, когда точное количество шагов неизвестно. Он повторяет код «пока» выполняется определенное логическое условие.

Пример:

count = 0

while count < 5:
    print(count)
    count += 1
    
    
Использование break и continue:

break завершает выполнение цикла.

continue пропускает текущую итерацию и переходит к следующей.

Пример:
# Прерывание цикла при достижении числа 3
for num in range(1, 6):
if num == 3:
break
print(num)

# Пропуск числа 3
for num in range(1, 6):
if num == 3:
continue
print(num)
""",

    "Урок 5: Функции": """
📘 Урок 5: Функции

Функция — это блок кода для выполнения задачи.

Создание функции:

def hello():
    print("Привет!")

Функция с параметрами:

def greet(name):
    print("Привет,", name)

Возврат значения:

def add(a, b):
    return a + b
"""
}

# ---------------- УРОКИ C++ ----------------
cpp_lessons_content = {

    "Урок 1: Введение в C++": """
📘 Урок 1: Введение в C++

C++ — мощный язык программирования.

✅ Используется для:
• создания игр
• разработки программ
• операционных систем
• высокопроизводительных приложений

Первая программа:

#include <iostream>

using namespace std;

int main() {
    cout << "Привет, мир!";
    return 0;
}
""",

    "Урок 2: Переменные и типы данных": """
📘 Урок 2: Переменные и типы данных

Переменная хранит данные.

Пример:

int age = 20;
string name = "Алексей";

Основные типы данных:
• int — целое число
• float — дробное число
• double — точное дробное число
• char — символ
• bool — true/false
• string — строка
""",

    "Урок 3: Условные операторы": """
📘 Урок 3: Условные операторы

Условные операторы в C++ используются для создания ветвлений в коде, позволяя программе принимать решения на основе выполнения заданных логических условий. Основные конструкции — это оператор if-else, тернарный оператор ?: и переключатель switch-case.

Пример:

if (age >= 18) {
    cout << "Доступ разрешён";
}
else {
    cout << "Доступ запрещён";
}
""",

    "Урок 4: Циклы for, while и do while": """
📘 Урок 4: Циклы for, while и do while

Цикл for:

Цикл for имеет следующее формальное определение:


for (инициализатор; условие; итерация)
{
    // тело цикла
}


инициализатор выполняется один раз при начале выполнения цикла и представляет установку начальных условий, как правило, это инициализация счетчиков - специальных переменных, которые используются для контроля за циклом.

условие представляет условие, при соблюдении которого выполняется цикл. Как правило, в качестве условия используется операция сравнения, и если она возвращает ненулевое значение (то есть условие истинно), то выполняется тело цикла, а затем выполняется итерация.

итерация выполняется после каждого завершения блока цикла и задает изменение параметров цикла. Обычно здесь происходит увеличение счетчиков цикла.


Например, перепишем программу по выводу квадратов чисел с помощью цикла for:


#include <iostream>
 
int main()
{   
    for(int i {1}; i < 10; i++)
    {
        std::cout << i << " * " << i << " = " << i * i << std::endl;
    }
}



Цикл while выполняет некоторый код, пока его условие истинно, то есть возвращает true. Он имеет следующее формальное определение:

int count = 0;

while (count < 5) {
    cout << count << endl;
    count++;
}


Цикл do-while в C++ — это разновидность цикла с постусловием. Его главное отличие от while заключается в том, что условие проверяется после выполнения тела цикла. Это гарантирует, что код внутри выполнится хотя бы один раз, даже если условие изначально ложно

Синтаксис выглядит следующим образом:

cppdo {
    // тело цикла (инструкции)
} while (условие);
""",

    "Урок 5: Функции": """
📘 Урок 5: Функции

Функция в C++ — это блок кода с заданным именем и списком параметров. Она выполняет конкретную задачу, позволяет избежать дублирования и делает программу модульной.
Любая программа на C++ начинается с вызова главной функции — main()

Создание функции:

void hello() {
    cout << "Привет!";
}

Функция с параметрами:

void greet(string name) {
    cout << "Привет, " << name;
}

Возврат значения:

int add(int a, int b) {
    return a + b;
}
"""
}

java_lessons_content = {

    "Урок 1: Введение в Java": """
📘 Урок 1: Введение в Java

Java — объектно-ориентированный язык программирования.

Используется для:
• Android-приложений
• веб-приложений
• серверов
• настольных программ

Главный принцип Java:
Write Once, Run Anywhere (Написал один раз — запускай где угодно). :contentReference[oaicite:0]{index=0}

Первая программа:

public class Main {
    public static void main(String[] args) {
        System.out.println("Привет, мир!");
    }
}
""",

    "Урок 2: Переменные и типы данных": """
📘 Урок 2: Переменные и типы данных

Переменная хранит данные.

Пример:

String name = "Алексей";
int age = 20;
double height = 1.75;
boolean student = true;

Основные типы данных:

• int — целые числа
• double — дробные числа
• boolean — true или false
• char — символ
• String — текст :contentReference[oaicite:1]{index=1}
""",

    "Урок 3: Условные операторы": """
📘 Урок 3: Условные операторы

Условные операторы позволяют программе принимать решения.

Пример:

int age = 18;

if (age >= 18) {
    System.out.println("Доступ разрешён");
}
else {
    System.out.println("Доступ запрещён");
}

Также можно использовать else if для нескольких условий.
""",

    "Урок 4: Циклы for и while": """
📘 Урок 4: Циклы for и while

Цикл for:

for (int i = 0; i < 5; i++) {
    System.out.println(i);
}

Цикл while:

int count = 0;

while (count < 5) {
    System.out.println(count);
    count++;
}

Циклы позволяют выполнять код несколько раз. :contentReference[oaicite:2]{index=2}
""",

    "Урок 5: Классы и объекты": """
📘 Урок 5: Классы и объекты

Java основана на объектно-ориентированном программировании (ООП). :contentReference[oaicite:3]{index=3}

Создание класса:

class Person {

    String name = "Алексей";

    void sayHello() {
        System.out.println("Привет!");
    }
}

Создание объекта:

Person person = new Person();

person.sayHello();

Класс — это шаблон.
Объект — экземпляр класса.
"""
}

javascript_lessons_content = {

    "Урок 1: Введение в JavaScript": """
📘 Урок 1: Введение в JavaScript

JavaScript — язык программирования для создания интерактивных сайтов.

Используется для:
• веб-сайтов
• веб-приложений
• игр в браузере
• серверной разработки

Первая программа:

console.log("Привет, мир!");

Функция console.log() выводит текст в консоль.
""",

    "Урок 2: Переменные и типы данных": """
📘 Урок 2: Переменные и типы данных

Переменные используются для хранения данных.

Пример:

let name = "Алексей";
let age = 20;
let height = 1.75;
let student = true;

Основные типы данных:

• String — текст
• Number — числа
• Boolean — true или false
• Null — пустое значение
• Undefined — значение не определено
""",

    "Урок 3: Условные операторы": """
📘 Урок 3: Условные операторы

Условные операторы позволяют выполнять разные действия в зависимости от условия.

Пример:

let age = 18;

if (age >= 18) {
    console.log("Доступ разрешён");
}
else {
    console.log("Доступ запрещён");
}

Также можно использовать else if для нескольких условий.
""",

    "Урок 4: Циклы for и while": """
📘 Урок 4: Циклы for и while

Цикл for:

for (let i = 0; i < 5; i++) {
    console.log(i);
}

Цикл while:

let count = 0;

while (count < 5) {
    console.log(count);
    count++;
}

Циклы позволяют многократно выполнять код.
""",

    "Урок 5: Классы и объекты": """
📘 Урок 5: Классы и объекты

Классы используются для создания объектов.

Пример класса:

class Person {

    constructor(name) {
        this.name = name;
    }

    sayHello() {
        console.log("Привет!");
    }
}

Создание объекта:

const person = new Person("Алексей");

person.sayHello();

Класс — это шаблон.
Объект — экземпляр класса.
"""
}

csharp_lessons_content = {

    "Урок 1: Введение в C#": """
📘 Урок 1: Введение в C#

C# — язык программирования от Microsoft.

Используется для:
• создания Windows-программ
• разработки игр на Unity
• веб-приложений
• мобильных приложений

Первая программа:

using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Привет, мир!");
    }
}
""",

    "Урок 2: Переменные и типы данных": """
📘 Урок 2: Переменные и типы данных

Переменные используются для хранения данных.

Пример:

string name = "Алексей";
int age = 20;
double height = 1.75;
bool student = true;

Основные типы данных:

• int — целые числа
• double — дробные числа
• bool — true или false
• char — символ
• string — текст
""",

    "Урок 3: Условные операторы": """
📘 Урок 3: Условные операторы

Условные операторы позволяют программе принимать решения.

Пример:

int age = 18;

if (age >= 18)
{
    Console.WriteLine("Доступ разрешён");
}
else
{
    Console.WriteLine("Доступ запрещён");
}
""",

    "Урок 4: Циклы for и while": """
📘 Урок 4: Циклы for и while

Цикл for:

for (int i = 0; i < 5; i++)
{
    Console.WriteLine(i);
}

Цикл while:

int count = 0;

while (count < 5)
{
    Console.WriteLine(count);
    count++;
}

Циклы позволяют выполнять код несколько раз.
""",

    "Урок 5: Классы и объекты": """
📘 Урок 5: Классы и объекты

Класс — это шаблон для создания объектов.

Пример класса:

class Person
{
    public string Name;

    public void SayHello()
    {
        Console.WriteLine("Привет!");
    }
}

Создание объекта:

Person person = new Person();

person.Name = "Алексей";

person.SayHello();

Класс — описание объекта.
Объект — экземпляр класса.
"""
}

# ---------------- КЛАВИАТУРЫ ----------------
lang_keyboard = [
    ["Python", "C++"],
    ["Java", "JavaScript"],
    ["C#"]
]

back_keyboard = [
    ["Назад к выбору языка"]
]

lesson_nav_keyboard = [
    ["⬅️ Предыдущий урок", "➡️ Следующий урок"],
    ["Назад к выбору языка"]
]

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

# ---------------- ВЫБОР ЯЗЫКА ----------------
async def choose_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_choice = update.message.text

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
        "❌ Пожалуйста, выбери язык кнопками."
    )

    return CHOOSING_LANG

# ---------------- ВЫБОР УРОКА ----------------
async def choose_lesson(update: Update, context: ContextTypes.DEFAULT_TYPE):


    user_choice = update.message.text

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

# ---------------- CANCEL ----------------
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 До встречи!",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def main():
    load_dotenv(".env")

    print("TOKEN:", os.getenv("TOKEN"))

    TOKEN = os.getenv("TOKEN")

    if not TOKEN:
        print("❌ TOKEN не найден! Проверь .env файл")
        return

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_LANG: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    choose_lang
                )
            ],

            CHOOSING_LESSON: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    choose_lesson
                )
            ],
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    app.add_handler(conv_handler)

    print("✅ Бот запущен!")

    app.run_polling()

# ---------------- ЗАПУСК ----------------
if __name__ == "__main__":
    main()

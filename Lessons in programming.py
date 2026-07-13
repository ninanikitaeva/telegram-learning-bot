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
CHOOSING_LANG, CHOOSING_LESSON, DOING_TASK = range(3)

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

# ---------------- ПРАКТИЧЕСКИЕ ЗАДАНИЯ PYTHON ----------------

python_practice_tasks = {

    "Урок 1: Введение в Python": """
📝 Практическое задание

Создай программу, которая выводит на экран:

Добро пожаловать в Python!


💡 Подсказка:
Используй функцию print()


✍️ Как отправить ответ:
Напиши только код.

Пример:

print("Какой-то текст")

Пример показывает только использование команды.
Текст в программе должен быть другим.
""",


    "Урок 2: Переменные и типы данных": """
📝 Практическое задание

Создай две переменные:

1) Переменная city должна хранить название города.
2) Переменная year должна хранить число.


Выведи обе переменные на экран.


💡 Подсказка:
Используй print()


Пример:

animal = "Кот"
number = 5

print(animal)
print(number)


Пример отличается от задания.
Создай свои переменные.
""",


    "Урок 3: Условные операторы": """
📝 Практическое задание

Создай переменную temperature.


Если температура больше или равна 20:
выведи:

На улице тепло


Иначе:

На улице холодно



💡 Подсказка:
Используй if и else.


Пример:

score = 50

if score > 60:
    print("Хороший результат")
else:
    print("Нужно потренироваться")


Пример показывает структуру условия.
Используй свои данные.
""",


    "Урок 4: Циклы for и while": """
📝 Практическое задание

Используя цикл for:

Выведи числа от 5 до 15.


Дополнительное задание:

Выведи только нечётные числа.


💡 Подсказка:
Используй range()


Пример:

for number in range(1, 4):
    print(number)


Пример показывает только принцип работы цикла.
Диапазон чисел должен быть другим.
""",


    "Урок 5: Функции": """
📝 Практическое задание

Создай функцию multiply(a, b).


Функция должна умножать два числа и возвращать результат.


Проверь работу функции.


💡 Подсказка:
Используй return.


Пример:

def add(a, b):
    return a + b


print(add(2, 3))


Пример использует сложение.
Тебе нужно сделать умножение.
"""
}


python_answers = {

    "Урок 1: Введение в Python":
        'print("Привет, мир!")',

    "Урок 2: Переменные и типы данных":
        'name = "Твое имя"\nage = 20',

    "Урок 3: Условные операторы":
        'if age >= 18:\n    print("Доступ разрешён")',

    "Урок 4: Циклы for и while":
        'for i in range(1, 11):\n    print(i)',

    "Урок 5: Функции":
        'def square(x):\n    return x*x'
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

# ---------------- ПРАКТИЧЕСКИЕ ЗАДАНИЯ C++ ----------------

cpp_practice_tasks = {

    "Урок 1: Введение в C++": """
📝 Практическое задание

Создай программу, которая выводит:

Привет, мир!

✍️ Как отправить ответ:
Напиши только код.

Пример использования cout:

cout << "Привет";
""",

    "Урок 2: Переменные и типы данных": """
📝 Практическое задание

Создай две переменные:

string name = "Твое имя";
int age = твой возраст;

Выведи их на экран.

✍️ Как отправить ответ:
Напиши только код.

Пример создания переменной:

string city = "Москва";

cout << city;
""",

    "Урок 3: Условные операторы": """
📝 Практическое задание

Создай переменную age.

Если возраст больше или равен 18,
выведи:

Доступ разрешён

иначе:

Доступ запрещён

✍️ Как отправить ответ:
Напиши только код.

Пример условия:

int number = 5;

if(number > 0)
{
    cout << "Положительное число";
}
""",

    "Урок 4: Циклы for, while и do while": """
📝 Практическое задание

С помощью цикла for выведи числа от 1 до 10.

✍️ Как отправить ответ:
Напиши только код.

Пример цикла:

for(int i = 1; i <= 3; i++)
{
    cout << i;
}
""",

    "Урок 5: Функции": """
📝 Практическое задание

Создай функцию:

int square(int x)

которая возвращает квадрат числа.

✍️ Как отправить ответ:
Напиши только код.

Пример функции:

int add(int a, int b)
{
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

# ---------------- ПРАКТИЧЕСКИЕ ЗАДАНИЯ JAVA ----------------

java_practice_tasks = {

    "Урок 1: Введение в Java": """
📝 Практическое задание

Создай программу, которая выводит:

Привет, мир!

✍️ Как отправить ответ:
Напиши только код.

Пример вывода текста:

System.out.println("Привет");
""",

    "Урок 2: Переменные и типы данных": """
📝 Практическое задание

Создай две переменные:

String name = "Твое имя";
int age = твой возраст;

Выведи их на экран.

✍️ Как отправить ответ:
Напиши только код.

Пример создания переменной:

String city = "Москва";

System.out.println(city);
""",

    "Урок 3: Условные операторы": """
📝 Практическое задание

Создай переменную age.

Если возраст больше или равен 18,
выведи:

Доступ разрешён

иначе:

Доступ запрещён

✍️ Как отправить ответ:
Напиши только код.

Пример условия:

int number = 5;

if (number > 0) {
    System.out.println("Положительное число");
}
""",

    "Урок 4: Циклы for и while": """
📝 Практическое задание

С помощью цикла for выведи числа от 1 до 10.

✍️ Как отправить ответ:
Напиши только код.

Пример цикла:

for (int i = 1; i <= 3; i++) {
    System.out.println(i);
}
""",

    "Урок 5: Классы и объекты": """
📝 Практическое задание

Создай класс Person.

Добавь поле name.

Создай объект этого класса.

✍️ Как отправить ответ:
Напиши только код.

Пример класса:

class Car {
    String brand;
}

Car car = new Car();

car.brand = "BMW";
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


# ---------------- ПРАКТИЧЕСКИЕ ЗАДАНИЯ JAVASCRIPT ----------------

javascript_practice_tasks = {

    "Урок 1: Введение в JavaScript": """
📝 Практическое задание

Создай программу, которая выводит:

Привет, мир!

✍️ Как отправить ответ:
Напиши только код.

Пример вывода текста:

console.log("Привет");
""",

    "Урок 2: Переменные и типы данных": """
📝 Практическое задание

Создай две переменные:

let name = "Твое имя";
let age = твой возраст;

Выведи их на экран.

✍️ Как отправить ответ:
Напиши только код.

Пример создания переменной:

let city = "Москва";

console.log(city);
""",

    "Урок 3: Условные операторы": """
📝 Практическое задание

Создай переменную age.

Если возраст больше или равен 18,
выведи:

Доступ разрешён

иначе:

Доступ запрещён

✍️ Как отправить ответ:
Напиши только код.

Пример условия:

let number = 5;

if (number > 0) {
    console.log("Положительное число");
}
""",

    "Урок 4: Циклы for и while": """
📝 Практическое задание

С помощью цикла for выведи числа от 1 до 10.

✍️ Как отправить ответ:
Напиши только код.

Пример цикла:

for (let i = 1; i <= 3; i++) {
    console.log(i);
}
""",

    "Урок 5: Классы и объекты": """
📝 Практическое задание

Создай класс Person.

Добавь свойство name.

Создай объект этого класса.

✍️ Как отправить ответ:
Напиши только код.

Пример класса:

class Car {
    constructor() {
        this.brand = "";
    }
}

const car = new Car();

car.brand = "BMW";
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

# ---------------- ПРАКТИЧЕСКИЕ ЗАДАНИЯ C# ----------------

csharp_practice_tasks = {

    "Урок 1: Введение в C#": """
📝 Практическое задание

Создай программу, которая выводит:

Привет, мир!

✍️ Как отправить ответ:
Напиши только код.

Пример вывода текста:

Console.WriteLine("Привет");
""",

    "Урок 2: Переменные и типы данных": """
📝 Практическое задание

Создай две переменные:

string name = "Твое имя";
int age = твой возраст;

Выведи их на экран.

✍️ Как отправить ответ:
Напиши только код.

Пример создания переменной:

string city = "Москва";

Console.WriteLine(city);
""",

    "Урок 3: Условные операторы": """
📝 Практическое задание

Создай переменную age.

Если возраст больше или равен 18,
выведи:

Доступ разрешён

иначе:

Доступ запрещён

✍️ Как отправить ответ:
Напиши только код.

Пример условия:

int number = 5;

if (number > 0)
{
    Console.WriteLine("Положительное число");
}
""",

    "Урок 4: Циклы for и while": """
📝 Практическое задание

С помощью цикла for выведи числа от 1 до 10.

✍️ Как отправить ответ:
Напиши только код.

Пример цикла:

for (int i = 1; i <= 3; i++)
{
    Console.WriteLine(i);
}
""",

    "Урок 5: Классы и объекты": """
📝 Практическое задание

Создай класс Person.

Добавь поле Name.

Создай объект этого класса.

✍️ Как отправить ответ:
Напиши только код.

Пример класса:

class Car
{
    public string Brand;
}

Car car = new Car();

car.Brand = "BMW";
"""
}



# ---------------- КЛАВИАТУРЫ ----------------
lang_keyboard = [
    ["Python", "C++"],
    ["Java", "JavaScript"],
    ["C#"],
    ["👤 Профиль"]
]

back_keyboard = [
    ["Назад к выбору языка"]
]
lesson_nav_keyboard = [
    ["📝 Практическое задание"],
    ["⬅️ Предыдущий урок", "➡️ Следующий урок"],
    ["Назад к выбору языка"]
]

# Клавиатура после выполнения задания
after_task_keyboard = [
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


async def choose_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text

    # Если пользователь отправил код
    if context.user_data.get("waiting_for_code"):

        if user_choice != "✅ Выполнил задание":
            context.user_data["user_code"] = user_choice

            await update.message.reply_text(
                "Код сохранён ✅\n"
                "Теперь нажми кнопку '✅ Выполнил задание'"
            )

            return CHOOSING_LESSON

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
        "❌ Пожалуйста, выбери язык кнопками."
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

    # Назад к уроку
    if user_code == "⬅️ Назад к уроку":

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
            task = "Задание пока недоступно."

        return CHOOSING_LESSON
        print("ОТКРЫТО ЗАДАНИЕ:", lesson_name)

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

    # ---------- PYTHON ----------
    if current_lang == "Python":

        if lesson_name == "Урок 1: Введение в Python":

            correct = "print" in code


        elif lesson_name == "Урок 2: Переменные и типы данных":

            correct = (
                    "=" in code
                    and "print" in code
            )


        elif lesson_name == "Урок 3: Условные операторы":

            correct = (
                    "if" in code
                    and "else" in code
            )


        elif lesson_name == "Урок 4: Циклы for и while":

            correct = (
                    "for" in code
                    and "range" in code
            )


        elif lesson_name == "Урок 5: Функции":

            correct = (
                    "def" in code
                    and "return" in code
            )


    # ---------- C++ ----------
    elif current_lang == "C++":

        if lesson_name == "Урок 1: Введение в C++":

            correct = (
                    "cout" in code
                    or "iostream" in code
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


        elif lesson_name == "Урок 4: Циклы for, while и do while":

            correct = (
                    "for" in code
                    or "while" in code
            )


        elif lesson_name == "Урок 5: Функции":

            correct = (
                    "return" in code
                    and "(" in code
            )


    # ---------- JAVA ----------
    elif current_lang == "Java":

        if lesson_name == "Урок 1: Введение в Java":

            correct = (
                    "system.out.println" in code
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
                    or "while" in code
            )


        elif lesson_name == "Урок 5: Классы и объекты":

            correct = (
                    "class" in code
                    and "new" in code
            )


    # ---------- JAVASCRIPT ----------
    elif current_lang == "JavaScript":

        if lesson_name == "Урок 1: Введение в JavaScript":

            correct = (
                    "console.log" in code
            )


        elif lesson_name == "Урок 2: Переменные и типы данных":

            correct = (
                    "let" in code
                    or "const" in code
            )


        elif lesson_name == "Урок 3: Условные операторы":

            correct = (
                    "if" in code
                    and "else" in code
            )


        elif lesson_name == "Урок 4: Циклы for и while":

            correct = (
                    "for" in code
                    or "while" in code
            )


        elif lesson_name == "Урок 5: Классы и объекты":

            correct = (
                    "class" in code
                    and "new" in code
            )


    # ---------- C# ----------
    elif current_lang == "C#":

        if lesson_name == "Урок 1: Введение в C#":

            correct = (
                    "console.writeline" in code
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
                    or "while" in code
            )


        elif lesson_name == "Урок 5: Классы и объекты":

            correct = (
                    "class" in code
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

        return DOING_TASK

        return CHOOSING_LESSON


    # Выполнение задания
    if user_choice == "✅ Выполнил задание":
        if user_choice == "✅ Выполнил задание":

            user_code = context.user_data.get("user_code")

            current_lang = context.user_data.get("lang")
            lesson_index = context.user_data.get("lesson_index", 0)

            lesson_name = lessons[current_lang][lesson_index]

            correct_answer = python_answers.get(lesson_name)
            correct_answer = cpp_answers.get(lesson_name)
            correct_answer = java_answers.get(lesson_name)
            correct_answer = javascript_answers.get(lesson_name)
            correct_answer = csharp_answers.get(lesson_name)

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

        entry_points=[
            CommandHandler("start", start)
        ],

        allow_reentry=True,

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

            DOING_TASK: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    check_task
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

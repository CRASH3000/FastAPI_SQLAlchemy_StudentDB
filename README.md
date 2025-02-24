# **Модель данных для хранения данных из таблицы со студентами**


Этот проект реализует **модель данных студентов** на **SQLAlchemy** и API на **FastAPI** для работы с базой данных. Данные загружаются из CSV-файла students.csv и хранятся в **SQLite**.



Проект выполняет следующие задачи:

- Создаёт модель данных студентов  с помощью SQLAlchemy
- Реализует операции INSERT и SELECT через специальный класс CRUD
- Автоматически заполняет базу данных из файла students.csv
- Реализует API-методы для работы с данными

## 🚀 Как запустить

#### 1. Установить зависимости
Сначала установите Python и библиотеки:
```bash
pip install -r requirements.txt
```
#### 2. Запустить сервер
```bash
uvicorn api:app --reload
```
#### **3. Открыть в браузере**
Перейдите в [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) и отправьте тестовый запрос.


## **📌 Как это работает?**



1) При запуске проекта данные из students.csv загружаются в базу данных SQLite.

2) FastAPI предоставляет API для работы со студентами:
* /students — получить список всех студентов
* /students/{faculty} — получить студентов по факультету
* /courses — список уникальных курсов
* /average-grade/{faculty} — средний балл по факультету

3) Запросы к API возвращают данные в формате JSON.

4) Для тестирования API используются простые автотесты на pytest и FastAPI TestClient.
Для запуска тестов используйте одну из команд (в зависимости от вашей версии Python):

```sh
pytest tests/ -v
```

```sh
python -m pytest tests/ -v
```
**📂 Структура проекта**
```
StudentDB/
├── api.py             # Основной API FastAPI
├── database.py        # Настройки базы данных
├── models.py          # SQLAlchemy-модель студента
├── crud.py            # CRUD-операции с БД
├── tests/             # Папка с тестами
│   ├── test_api.py    # Автотесты API
├── students.db        # SQLite база данных
├── data/              # CSV-файл с данными
│   ├── students.csv
└── README.md
```

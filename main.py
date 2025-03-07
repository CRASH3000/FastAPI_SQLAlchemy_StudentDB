from fastapi import FastAPI
from database import engine, Base
from api import router as api_router
from auth import router as auth_router

# Создаем таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StudentDB",
    description="Проект загружает данные из CSV-файла в базу данных и предоставляет API для работы с этими данными.",
)
app.include_router(auth_router) # Подключаем маршрутизатор
app.include_router(api_router)
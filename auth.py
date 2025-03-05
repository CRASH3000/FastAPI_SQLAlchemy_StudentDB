from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
import uuid

router = APIRouter(prefix="/auth", tags=["Аутентификация"])

db_users = {}  # Простая имитация базы пользователей (ключ - user_id, значение - dict с данными)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authenticate_user(user_id: str):
    if user_id not in db_users:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Доступ запрещён. Войдите в систему.")
    return user_id

@router.post("/register")
def register(first_name: str, last_name: str):
    user_id = str(uuid.uuid4())  # Генерация уникального идентификатора
    db_users[user_id] = {"first_name": first_name, "last_name": last_name}
    return {"message": "Пользователь зарегистрирован", "user_id": user_id}

@router.post("/login")
def login(user_id: str):
    if user_id not in db_users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный user_id")
    return {"message": "Вход выполнен", "user_id": user_id}

@router.post("/logout")
def logout(user_id: str):
    if user_id not in db_users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
    return {"message": "Выход выполнен"}
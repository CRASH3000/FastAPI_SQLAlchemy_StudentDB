from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import StudentCRUD
from models import Student

app = FastAPI(
    title="StudentDB",
    description="Проект загружает данные из CSV-файла в базу данных и предоставляет API для работы с этими данными.",
)

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/students/{faculty}",
         summary="Получение списка студентов по факультету",
         description="Возвращает список студентов по указанному факультету. Например, ФПМИ",
         tags=["Студенты"]
)
def get_students(faculty: str, db: Session = Depends(get_db)):
    crud = StudentCRUD(db)
    students = crud.get_students_by_faculty(faculty)
    return [{"last_name": s.last_name, "first_name": s.first_name, "course": s.course} for s in students]

@app.get("/courses",
         summary="Получение списка уникальных курсов",
         description="Возвращает список уникальных курсов, на которых учатся студенты.",
         tags=["Курсы"]
)
def get_unique_courses(db: Session = Depends(get_db)):
    crud = StudentCRUD(db)
    courses = crud.get_unique_courses()
    return [course[0] for course in courses]

@app.get("/average-grade/{faculty}",
         summary="Получение среднего балла по факультету",
         description="Возвращает список со средним баллом студентов по факультету.",
         tags=["Оценки"]
)
def get_avg_grade(faculty: str, db: Session = Depends(get_db)):
    crud = StudentCRUD(db)
    avg_grade = crud.get_avg_grade_by_faculty(faculty)
    return {"faculty": faculty, "average_grade": avg_grade if avg_grade else "Нет данных"}

@app.get(
    "/students",
    summary="Получение списка всех студентов",
    description="Возвращает список всех студентов из базы данных с их ID, именем, фамилией, факультетом, курсом и оценкой.",
    tags=["Студенты"]
)
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return [
        {
            "id": s.id,
            "last_name": s.last_name,
            "first_name": s.first_name,
            "faculty": s.faculty,
            "course": s.course,
            "grade": s.grade
        }
        for s in students
    ]
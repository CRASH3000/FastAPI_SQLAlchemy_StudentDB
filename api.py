from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import StudentCRUD
from models import Student
from auth import router as auth_router, authenticate_user
app = FastAPI(
    title="StudentDB",
    description="Проект загружает данные из CSV-файла в базу данных и предоставляет API для работы с этими данными.",
)
app.include_router(auth_router) # Подключаем маршрутизатор

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
def get_students(faculty: str, db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):
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
def get_avg_grade(faculty: str, db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):
    crud = StudentCRUD(db)
    avg_grade = crud.get_avg_grade_by_faculty(faculty)
    return {"faculty": faculty, "average_grade": avg_grade if avg_grade else "Нет данных"}

@app.get(
    "/students",
    summary="Получение списка всех студентов",
    description="Возвращает список всех студентов из базы данных с их ID, именем, фамилией, факультетом, курсом и оценкой.",
    tags=["Студенты"]
)
def get_all_students(db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):
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

@app.get("/student/{student_id}",
         summary="Получение информации о студенте по ID",
         description="Возвращает информацию о студенте с указанным ID (id, фамилия, имя, факультет, курс, оценка).",
         tags=["Студенты"]
)
def get_student_by_id(student_id: int, db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):
    crud = StudentCRUD(db)
    student = crud.get_student_by_id(student_id)

    if student is None:
        return {"error": "Студент с таким ID не найден"}

    return {
        "id": student.id,
        "last_name": student.last_name,
        "first_name": student.first_name,
        "faculty": student.faculty,
        "course": student.course,
        "grade": student.grade
    }

@app.post("/students/",
          summary="Добавление нового студента",
          tags=["Студенты"]
          )
def create_new_student(last_name: str, first_name: str, faculty: str, course: str,
                       grade: int, db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):

    crud = StudentCRUD(db)
    student = crud.post_add_student(last_name, first_name, faculty, course, grade)
    return {"message": "Студент успешно добавлен", "id": student.id}

@app.put("/students/{student_id}",
         summary="Обновление информации о студенте",
         tags=["Студенты"]
         )
def update_student_info_by_id(student_id: int, last_name: str = None, first_name: str = None, faculty: str = None,
                   course: str = None, grade: int = None, db: Session = Depends(get_db),
                              user_id: str = Depends(authenticate_user)):
    crud = StudentCRUD(db)
    student = crud.put_update_student_by_id(student_id, last_name, first_name, faculty, course, grade)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return {"message": "Данные студента обновлены", "student": student}

@app.delete("/students/{student_id}",
            summary="Удаление студента из базы по ID",
            tags=["Студенты"]
            )
def delete_student(student_id: int, db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):
    crud = StudentCRUD(db)
    student = crud.delete_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return {"message": "Студент успешно удалён", "id": student.id}



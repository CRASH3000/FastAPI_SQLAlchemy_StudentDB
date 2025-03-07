from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import StudentCRUD
from models import Student
from auth import authenticate_user
from csv_loader import load_students_from_csv, delete_students_by_ids
from cache import get_cache, set_cache

router = APIRouter()

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/load_csv",
             summary="Фоновая загрузка данных из CSV",
             tags=["Фоновые задачи"])
def load_csv_background(file_name: str, background_tasks: BackgroundTasks, user_id: str = Depends(authenticate_user)):
    background_tasks.add_task(load_students_from_csv, file_name)
    return {"message": "Задача по загрузке CSV запущена в фоне."}


@router.get("/students/{faculty}",
         summary="Получение списка студентов по факультету",
         description="Возвращает список студентов по указанному факультету. Например, ФПМИ",
         tags=["Студенты"]
)
def get_students(faculty: str, db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):
    cache_key = f"students_{faculty}"

    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    crud = StudentCRUD(db)
    students = crud.get_students_by_faculty(faculty)
    result = [{"last_name": s.last_name, "first_name": s.first_name, "course": s.course} for s in students]

    set_cache(cache_key, result)
    return result
@router.get("/courses",
         summary="Получение списка уникальных курсов",
         description="Возвращает список уникальных курсов, на которых учатся студенты.",
         tags=["Курсы"]
)
def get_unique_courses(db: Session = Depends(get_db)):
    cache_key = "courses"

    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    crud = StudentCRUD(db)
    courses = crud.get_unique_courses()
    result = [course[0] for course in courses]

    set_cache(cache_key, result)

    return result

@router.get("/average-grade/{faculty}",
         summary="Получение среднего балла по факультету",
         description="Возвращает список со средним баллом студентов по факультету.",
         tags=["Оценки"]
)
def get_avg_grade(faculty: str, db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):
    cache_key = f"avg_grade_{faculty}"

    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    crud = StudentCRUD(db)
    avg_grade = crud.get_avg_grade_by_faculty(faculty)
    result =  {"faculty": faculty, "average_grade": avg_grade if avg_grade else "Нет данных"}

    set_cache(cache_key, result)

    return result

@router.get(
    "/students",
    summary="Получение списка всех студентов",
    description="Возвращает список всех студентов из базы данных с их ID, именем, фамилией, факультетом, курсом и оценкой.",
    tags=["Студенты"]
)
def get_all_students(db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):
    cache_key = "all_students"

    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    students = db.query(Student).all()
    result = [
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

    # Сохраняем в Redis
    set_cache(cache_key, result)

    return result

@router.get("/student/{student_id}",
         summary="Получение информации о студенте по ID",
         description="Возвращает информацию о студенте с указанным ID (id, фамилия, имя, факультет, курс, оценка).",
         tags=["Студенты"]
)
def get_student_by_id(student_id: int, db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):
    cache_key = f"student_by_id_{student_id}"

    # Проверка есть ли уже данные в кеше Redis
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    crud = StudentCRUD(db)
    student = crud.get_student_by_id(student_id)

    if student is None:
        result = {"error": "Студент с таким ID не найден"}
    else:
        result = {
        "id": student.id,
        "last_name": student.last_name,
        "first_name": student.first_name,
        "faculty": student.faculty,
        "course": student.course,
        "grade": student.grade
    }

    set_cache(cache_key, result)

    return result

@router.post("/students/",
          summary="Добавление нового студента",
          tags=["Студенты"]
          )
def create_new_student(last_name: str, first_name: str, faculty: str, course: str,
                       grade: int, db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):

    crud = StudentCRUD(db)
    student = crud.post_add_student(last_name, first_name, faculty, course, grade)
    return {"message": "Студент успешно добавлен", "id": student.id}

@router.put("/students/{student_id}",
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

@router.delete("/students/{student_id}",
            summary="Удаление студента из базы по ID",
            tags=["Студенты"]
            )
def delete_student(student_id: int, db: Session = Depends(get_db), user_id: str = Depends(authenticate_user)):
    crud = StudentCRUD(db)
    student = crud.delete_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return {"message": "Студент успешно удалён", "id": student.id}

@router.post("/delete_students",
             summary="Фоновое удаление студентов по списку ID",
             tags=["Фоновые задачи"])
def delete_students_background(student_ids: list[int], background_tasks: BackgroundTasks,
                               user_id: str = Depends(authenticate_user)):
    background_tasks.add_task(delete_students_by_ids, student_ids)
    return {"message": f"Задача по удалению студентов с ID {student_ids} запущена в фоне."}



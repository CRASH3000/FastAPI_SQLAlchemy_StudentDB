from database import SessionLocal
from crud import StudentCRUD
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def load_students_from_csv(file_name: str):
    file_path = DATA_DIR / file_name
    db = SessionLocal()
    crud = StudentCRUD(db)

    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        crud.post_add_student(
            last_name=row["Фамилия"],
            first_name=row["Имя"],
            faculty=row["Факультет"],
            course=row["Курс"],
            grade=row["Оценка"]
        )
    db.close()

def delete_students_by_ids(student_ids: list[int]):
    db = SessionLocal()
    crud = StudentCRUD(db)
    for sid in student_ids:
        crud.delete_student_by_id(sid)
    db.close()
from pathlib import Path
import pandas as pd
from database import engine, Base, SessionLocal
from crud import StudentCRUD

# Создаем таблицы
Base.metadata.create_all(bind=engine)

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "data" / "students.csv"

# Функция для загрузки данных из CSV
def load_students_from_csv(file_path):
    if not file_path.exists():
        print(f"Ошибка: файл {file_path} не найден!")
        return

    df = pd.read_csv(file_path)
    db = SessionLocal()
    crud = StudentCRUD(db)

    for _, row in df.iterrows():
        crud.add_student(
            last_name=row["Фамилия"],
            first_name=row["Имя"],
            faculty=row["Факультет"],
            course=row["Курс"],
            grade=row["Оценка"]
        )

    db.close()
    print("Данные успешно загружены в базу!")

# Загружаем студентов в базу
load_students_from_csv(file_path)

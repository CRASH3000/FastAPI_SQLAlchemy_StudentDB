from sqlalchemy.orm import Session
from models import Student


class StudentCRUD:
    def __init__(self, db: Session):
        self.db = db

    def add_student(self, last_name, first_name, faculty, course, grade):
        student = Student(
            last_name=last_name,
            first_name=first_name,
            faculty=faculty,
            course=course,
            grade=grade
        )
        self.db.add(student)
        self.db.commit()

    def get_students_by_faculty(self, faculty):
        return self.db.query(Student).filter(Student.faculty == faculty).all()

    def get_unique_courses(self):
        return self.db.query(Student.course).distinct().all()

    def get_avg_grade_by_faculty(self, faculty):
        from sqlalchemy import func
        return self.db.query(func.avg(Student.grade)).filter(Student.faculty == faculty).scalar()
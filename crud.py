from sqlalchemy.orm import Session
from models import Student

class StudentCRUD:
    def __init__(self, db: Session):
        self.db = db

    def post_add_student(self, last_name, first_name, faculty, course, grade):
        student = Student(
            last_name=last_name,
            first_name=first_name,
            faculty=faculty,
            course=course,
            grade=grade
        )
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def get_students_by_faculty(self, faculty):
        return self.db.query(Student).filter(Student.faculty == faculty).all()

    def get_unique_courses(self):
        return self.db.query(Student.course).distinct().all()

    def get_avg_grade_by_faculty(self, faculty):
        from sqlalchemy import func
        return self.db.query(func.avg(Student.grade)).filter(Student.faculty == faculty).scalar()

    def put_update_student_by_id(self, student_id, last_name=None, first_name=None, faculty=None, course=None, grade=None):
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return None

        # Обновляем только переданные параметры
        if last_name:
            student.last_name = last_name
        if first_name:
            student.first_name = first_name
        if faculty:
            student.faculty = faculty
        if course:
            student.course = course
        if grade is not None:
            student.grade = grade

        self.db.commit()
        self.db.refresh(student)
        return student

    def delete_student_by_id(self, student_id):
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return None

        self.db.delete(student)
        self.db.commit()
        return student

    def get_student_by_id(self, student_id: int):
        return self.db.query(Student).filter(Student.id == student_id).first()
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)  # Создаём тестового клиента FastAPI

def test_get_all_students():
    response = client.get("/students")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        student = data[0]
        assert isinstance(student, dict)  # Должен быть словарь (JSON-объект)
        assert "id" in student
        assert "last_name" in student
        assert "first_name" in student
        assert "faculty" in student
        assert "course" in student
        assert "grade" in student

        # Дополнительно проверяем типы данных
        assert isinstance(student["id"], int)
        assert isinstance(student["last_name"], str)
        assert isinstance(student["first_name"], str)
        assert isinstance(student["faculty"], str)
        assert isinstance(student["course"], str)
        assert isinstance(student["grade"], (int, float))  # Оценка может быть целым или дробным числом


def test_get_students_by_faculty():
    faculty = "АВТФ"
    response = client.get(f"/students/{faculty}")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        student = data[0]
        assert isinstance(student, dict)
        assert "last_name" in student
        assert "first_name" in student
        assert "course" in student

def test_get_unique_courses():
    response = client.get("/courses")
    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert all(isinstance(course, str) for course in data)
    assert len(data) == len(set(data)) # Проверяем, что все курсы уникальны

def test_get_avg_grade():
    faculty = "ФПМИ"
    response = client.get(f"/average-grade/{faculty}")
    assert response.status_code == 200
    data = response.json()
    assert "faculty" in data
    assert "average_grade" in data
    assert isinstance(data["average_grade"], (int, float, str))
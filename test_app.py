from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API"}

def test_read_departments():
    response = client.get("/departments/")
    assert response.status_code == 200
    # Dependiendo de los datos, puedes agregar más validaciones aquí

def test_read_jobs():
    response = client.get("/jobs/")
    assert response.status_code == 200
    # Agrega validaciones adicionales según tus necesidades

def test_read_employees():
    response = client.get("/employees/")
    assert response.status_code == 200
    # Agrega validaciones adicionales según tus necesidades

def test_upload_employees():
    with open("files/hired_employees - Does not Exist Department and Job.csv", "rb") as file:
        response = client.post("/employees/upload/", files={"file": file})
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded and data inserted successfully"}

def test_upload_departments():
    with open("files/departments.csv", "rb") as file:
        response = client.post("/departments/upload/", files={"file": file})
    assert response.status_code == 200
    assert response.json() == {"message": "Departments uploaded successfully"}

def test_upload_jobs():
    with open("files/jobs.csv", "rb") as file:
        response = client.post("/jobs/upload/", files={"file": file})
    assert response.status_code == 200
    assert response.json() == {"message": "Jobs uploaded successfully"}

def test_get_quarterly_hires():
    response = client.get("/hires/quarterly/")
    assert response.status_code == 200
    # Agrega validaciones adicionales según los resultados esperados

def test_get_above_average_hires():
    response = client.get("/hires/above-average/")
    assert response.status_code == 200
    # Agrega validaciones adicionales según los resultados esperados

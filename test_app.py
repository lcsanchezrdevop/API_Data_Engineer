from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_upload_file():
    response = client.post("/upload/", files={"file": ("test.csv", "id,name,datetime,department_id,job_id\n1,John Doe,2021-06-01T12:00:00Z,1,1")})
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded and data inserted successfully"}

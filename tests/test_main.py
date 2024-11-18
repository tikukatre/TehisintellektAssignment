from fastapi.testclient import TestClient
from app.main import app

def test_main():
    with TestClient(app) as client:
        response = client.get("/source_info")
        assert response.status_code == 200
        assert "https://tehisintellekt.ee" in response.json()

        response = client.post("/ask/", json={})
        assert response.status_code == 400
        assert "Question field is required and needs to be filled" in response.json()["detail"]
        
        response = client.post("/ask/", json={"question": "Kes on Elon Musk?"})
        assert response.status_code == 200
        assert "Andmed puuduvad" in response.json()["answer"]
        
        response = client.post("/ask/", json={"question": "Kes on Andmeteadus OÜ tegevjuht?"})
        print(response.json())
        assert response.status_code == 200
        assert "Kristjan Eljand" in response.json()["answer"]

       



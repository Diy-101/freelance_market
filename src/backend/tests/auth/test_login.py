from fastapi.testclient import TestClient
from src.settings import Settings

def test_login(client: TestClient, config: Settings):
    response = client.post(
        "/api/auth/login",
        json={"init_data": config.mock_user},
    )
    print(response.json())
    print(response.status_code)
    assert response.status_code == 200, f"Response: {response.status_code}, body: {response.json()}"

from fastapi.testclient import TestClient
from inventory_api.dependencies import generate_random_name
from sqlalchemy.orm import Session


user_id = None
username = generate_random_name()
email = username + "@test.com"


def test_create_user(client: TestClient):
    global user_id
    response = client.post(
        "/users",
        json={"username": username, "password": username, "email": email, "role": "user"}
    )
    assert response.status_code == 200
    data = response.json()

    assert data["username"] == username
    assert data["email"] == email
    assert "id" in data
    user_id = data["id"]


def test_login_for_access_token(client: TestClient):
    response = client.post(
        "/users/token",
        data={"username": username, "password": username}
    )
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"


def test_update_user(client: TestClient, test_db: Session):
    new_username = generate_random_name()
    new_email = new_username + "@test.com"
    login_response = client.post(
        "users/token",
        data={"username": username, "password": username}
    )
    token = login_response.json()["access_token"]
    response = client.put(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": new_username, "email": new_email}
    )
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["username"] == new_username
    assert updated_data["email"] == new_email

import pytest
from starlette.testclient import TestClient
from inventory_api.dependencies import generate_random_name

item_id = None
username = generate_random_name()
email = username + "@test.com"


def test_create_user(client: TestClient):
    response = client.post(
        "/users",
        json={"username": username, "password": username, "email": email, "role": "user"}
    )
    assert response.status_code == 200


@pytest.fixture
def authenticated_client(client):
    login_data = {
        "username": username,
        "password": username
    }
    response = client.post("/users/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


def test_create_item(authenticated_client):
    global item_id
    item_name = generate_random_name()
    response = authenticated_client.post(
        "/items/", json={
            "name": item_name, "description": "A test item", "category": "category", "quantity": 32, "price": 10.99
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == item_name
    assert data["description"] == "A test item"
    assert data["category"] == "category"
    assert data["price"] == 10.99
    assert data["quantity"] == 32
    assert "id" in data
    item_id = data["id"]


def test_read_items(authenticated_client):
    response = authenticated_client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_item(authenticated_client):
    response = authenticated_client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id


def test_update_item(authenticated_client):
    item_name = generate_random_name()
    response = authenticated_client.put(
        f"/items/{item_id}",
        json={"name": item_name, "description": "Updated item", "category": "new category", "quantity": 30, "price": 12}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_name
    assert data["price"] == 12
    assert data["description"] == "Updated item"
    assert data["category"] == "new category"
    assert data["quantity"] == 30
    assert "id" in data


def test_delete_item(authenticated_client):
    response = authenticated_client.delete(f"/items/{item_id}")
    assert response.status_code == 200

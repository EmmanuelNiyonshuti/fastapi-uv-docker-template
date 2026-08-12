from typing import Any

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.anyio

async def register_user(
    client: AsyncClient, email: str, username: str = "tester"
) -> dict[str, Any]:
    response = await client.post(
        "/api/user",
        json={"username": username, "email": email, "password": "supersecret"},
    )
    assert response.status_code == 201
    return response.json()


async def login(client: AsyncClient, email: str, password: str = "supersecret") -> str:
    response = await client.post(
        "/api/token",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


async def test_register_user(client: AsyncClient) -> None:
    payload = await register_user(client, "alice@example.com")
    assert payload["success"] is True
    assert payload["id"] > 0


async def test_register_duplicate_email_rejected(client: AsyncClient) -> None:
    await register_user(client, "bob@example.com")
    response = await client.post(
        "/api/user",
        json={"username": "bob", "email": "bob@example.com", "password": "supersecret"},
    )
    assert response.status_code == 400


async def test_login_returns_token(client: AsyncClient) -> None:
    await register_user(client, "carol@example.com")
    assert await login(client, "carol@example.com")


async def test_login_with_wrong_password_rejected(client: AsyncClient) -> None:
    await register_user(client, "dave@example.com")
    response = await client.post(
        "/api/token",
        data={"username": "dave@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


async def test_me_returns_current_user(client: AsyncClient) -> None:
    await register_user(client, "erin@example.com", username="erin")
    token = await login(client, "erin@example.com")
    response = await client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "erin@example.com"
    assert body["username"] == "erin"


async def test_me_requires_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/users/me")
    assert response.status_code == 401


async def test_delete_me(client: AsyncClient) -> None:
    await register_user(client, "frank@example.com")
    token = await login(client, "frank@example.com")
    response = await client.delete("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert body == {"message": "User deleted successfully"}

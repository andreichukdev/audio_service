import pytest
from httpx import AsyncClient
from fastapi import status
from src.app.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={
            "username": "testuser_unique",
            "email": "testuser_unique@example.com",
            "password": "testpassword"
        })
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.json()}")
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        register_response = await ac.post("/auth/register", json={
            "username": "testuser_unique",
            "email": "testuser_unique@example.com",
            "password": "testpassword"
        })
        assert register_response.status_code == status.HTTP_200_OK

        login_response = await ac.post("/auth/login", json={
            "email": "testuser_unique@example.com",
            "password": "testpassword"
        })
        assert login_response.status_code == status.HTTP_200_OK
        assert "access_token" in login_response.json()
        access_token = login_response.json()["access_token"]

        assert access_token is not None


@pytest.mark.asyncio
async def test_get_user_info():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        register_response = await ac.post("/auth/register", json={
            "username": "testuser_unique",
            "email": "testuser_unique@example.com",
            "password": "testpassword"
        })
        assert register_response.status_code == status.HTTP_200_OK

        login_response = await ac.post("/auth/login", json={
            "email": "testuser_unique@example.com",
            "password": "testpassword"
        })
        access_token = login_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = await ac.get("/user", headers=headers)
        assert user_info_response.status_code == status.HTTP_200_OK

        user_data = user_info_response.json()
        assert user_data["email"] == "testuser_unique@example.com"
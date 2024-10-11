import pytest
from httpx import AsyncClient
from fastapi import status
from src.app.main import app

@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        register_response = await ac.post("/auth/register", json={
            "username": "task_testuser",
            "email": "task_testuser@example.com",
            "password": "testpassword"
        })
        assert register_response.status_code == status.HTTP_200_OK
        access_token = register_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        task_data = {
            "task_name": "New Task",
            "user_id": 1, 
            "prompts": ["First prompt", "Second prompt"],
            "audio_url": "https://example.com/audio.mp3"
        }
        response = await ac.post("/tasks/", headers=headers, json=task_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["task_name"] == task_data["task_name"]


@pytest.mark.asyncio
async def test_read_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        register_response = await ac.post("/auth/register", json={
            "username": "task_read_user",
            "email": "task_read_user@example.com",
            "password": "testpassword"
        })
        assert register_response.status_code == status.HTTP_200_OK
        access_token = register_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        task_data = {
            "task_name": "Read Task",
            "user_id": 1,
            "prompts": ["Read this prompt"],
            "audio_url": "https://example.com/audio.mp3"
        }
        create_response = await ac.post("/tasks/", headers=headers, json=task_data)
        assert create_response.status_code == status.HTTP_200_OK
        task_id = create_response.json()["id"]

        response = await ac.get(f"/tasks/{task_id}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["task_name"] == task_data["task_name"]


@pytest.mark.asyncio
async def test_update_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        register_response = await ac.post("/auth/register", json={
            "username": "task_update_user",
            "email": "task_update_user@example.com",
            "password": "testpassword"
        })
        assert register_response.status_code == status.HTTP_200_OK
        access_token = register_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        task_data = {
            "task_name": "Old Task",
            "user_id": 1,
            "prompts": ["Old prompt"],
            "audio_url": "https://example.com/audio.mp3"
        }
        create_response = await ac.post("/tasks/", headers=headers, json=task_data)
        assert create_response.status_code == status.HTTP_200_OK
        task_id = create_response.json()["id"]

        updated_task_data = {
            "task_name": "Updated Task",
            "prompts": ["Updated prompt"]
        }
        response = await ac.put(f"/tasks/{task_id}", headers=headers, json=updated_task_data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["task_name"] == updated_task_data["task_name"]


@pytest.mark.asyncio
async def test_delete_tasks():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        register_response = await ac.post("/auth/register", json={
            "username": "task_delete_user",
            "email": "task_delete_user@example.com",
            "password": "testpassword"
        })
        assert register_response.status_code == status.HTTP_200_OK
        access_token = register_response.json()["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        task_data = {
            "task_name": "Delete Task",
            "user_id": 1,
            "prompts": ["Delete this prompt"],
            "audio_url": "https://example.com/audio.mp3"
        }
        create_response = await ac.post("/tasks/", headers=headers, json=task_data)
        assert create_response.status_code == status.HTTP_200_OK
        task_id = create_response.json()["id"]

        response = await ac.delete("/tasks/", headers=headers, json={"task_ids": [task_id]})
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Tasks deleted"
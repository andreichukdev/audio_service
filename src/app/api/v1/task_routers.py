from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.db.session import get_db
from src.app.crud.tasks import get_task_by_id, create_task, update_task, delete_tasks
from src.app.schemas.tasks import TaskCreate, TaskUpdate, TaskResponse
from src.app.schemas.users import User
from src.app.utils.common import get_current_user
from src.app.services.audio import process_audio
import aiofiles
import os

router = APIRouter()

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = await get_task_by_id(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized access")
    return task

@router.post("/tasks/", response_model=TaskResponse)
async def create_new_task(task_data: TaskCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = await create_task(db, task_name=task_data.task_name, user_id=current_user.id, prompts=task_data.prompts, audio_url=task_data.audio_url)
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_existing_task(task_id: int, task_data: TaskUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = await get_task_by_id(db, task_id=task_id)
    if task is None or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found or unauthorized access")
    updated_task = await update_task(db, task_id, task_data.task_name, task_data.prompts)
    return updated_task

@router.delete("/tasks/")
async def delete_task_list(task_ids: list[int], db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = [await get_task_by_id(db, task_id) for task_id in task_ids]
    for task in tasks:
        if task is None or task.user_id != current_user.id:
            raise HTTPException(status_code=404, detail="Task not found or unauthorized access")
    await delete_tasks(db, task_ids)
    return {"message": "Tasks deleted"}

@router.post("/tasks/audio", response_model=TaskResponse)
async def create_task_from_audio(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    audio_file_path = f"/tmp/{file.filename}"
    
    async with aiofiles.open(audio_file_path, "wb") as buffer:
        while content := await file.read(1024):
            await buffer.write(content)

    prompts = process_audio(audio_file_path)

    task = await create_task(db, task_name="Task from audio", user_id=current_user.id, prompts=prompts, audio_url=audio_file_path)
    
    os.remove(audio_file_path)
    
    return task
from sqlalchemy.future import select
from src.app.db.models.tasks import Task
from sqlalchemy.ext.asyncio import AsyncSession

async def get_task_by_id(db: AsyncSession, task_id: int):
    stmt = select(Task).filter(Task.id == task_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def create_task(db: AsyncSession, task_name: str, user_id: int, prompts: list[str], audio_url: str = None):
    prompt_text = ';'.join(prompts) 
    db_task = Task(task_name=task_name, user_id=user_id, prompts=prompt_text, audio_url=audio_url)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update_task(db: AsyncSession, task_id: int, task_name: str = None, prompts: list[str] = None):
    stmt = select(Task).filter(Task.id == task_id)
    result = await db.execute(stmt)
    task = result.scalars().first()
    
    if task:
        if task_name:
            task.task_name = task_name
        if prompts:
            task.prompts = ';'.join(prompts)
        await db.commit()
        return task
    return None

async def delete_tasks(db: AsyncSession, task_ids: list[int]):
    stmt = select(Task).filter(Task.id.in_(task_ids))
    result = await db.execute(stmt)
    tasks_to_delete = result.scalars().all()

    if tasks_to_delete:
        for task in tasks_to_delete:
            await db.delete(task)
        await db.commit()
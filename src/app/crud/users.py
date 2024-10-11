from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.db.models.users import User
from src.app.core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).filter(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(User).filter(User.username == username)
    result = await db.execute(stmt)
    return result.scalars().first()

async def create_user(db: AsyncSession, username: str, email: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
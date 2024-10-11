from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from src.app.schemas.users import UserCreate, UserResponse, UserLogin
from src.app.crud.users import create_user, get_user_by_email
from src.app.db.session import get_db
from src.app.core.security import verify_password, create_access_token, create_refresh_token
from src.app.utils.common import get_current_user
from datetime import timedelta
from src.app.core.config import settings

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = await create_user(db, username=user.username, email=user.email, password=user.password)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user.email}, 
        secret_key=settings.SECRET_KEY, 
        expires_delta=access_token_expires
    )

    refresh_token = create_refresh_token(
        data={"sub": new_user.email}, 
        secret_key=settings.SECRET_KEY, 
        expires_delta=timedelta(days=7)
    )
    
    return {
        "username": new_user.username, 
        "email": new_user.email, 
        "id": new_user.id, 
        "access_token": access_token, 
        "refresh_token": refresh_token
    }


@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email=data.email)
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, 
        secret_key=settings.SECRET_KEY, 
        expires_delta=access_token_expires
    )
    
    refresh_token_expires = timedelta(days=30)
    refresh_token = create_access_token(
        data={"sub": user.email}, 
        secret_key=settings.SECRET_KEY, 
        expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }

@router.get("/user", response_model=UserResponse)
async def read_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, 
        secret_key=settings.SECRET_KEY, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token}
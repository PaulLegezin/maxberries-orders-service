import uuid

from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import settings
from app.core.db import engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.AUTH_SERVICE_URL)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    async with SessionLocal() as db:
        yield db


async def get_current_user_id(request: Request) -> uuid.UUID:
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Необходима авторизация"
        )
    return user_id

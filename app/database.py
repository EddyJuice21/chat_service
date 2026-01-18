import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# Получаем адрес БД из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/chat_db")

# Создаем движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Фабрика сессий
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс
class Base(AsyncAttrs, DeclarativeBase):
    pass

async def get_db():
    async with async_session_factory() as session:
        yield session
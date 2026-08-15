from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """*Declarative base class shared by all ORM models.*"""


engine = create_async_engine(
    settings.db.database_url,
    echo=False,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session_db() -> AsyncGenerator[AsyncSession, None]:
    """*Provides an async database session and rolls it back on failure.*

    Yields:
        AsyncSession: session bound to the application engine.

    Raises:
        Exception: re-raises any error occurred inside the session after a rollback.
    """
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

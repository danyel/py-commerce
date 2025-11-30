from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://ecommerce:ecommerce@localhost:5401/ecommerce")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# noinspection PyPackageRequirements
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# noinspection PyPackageRequirements
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from .config import settings

async_engine: AsyncEngine = create_async_engine(settings.ASYNC_DATABASE_URL, pool_pre_ping=True)

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("uid", Integer, primary_key=True),
    Column("username", String, nullable=True),
    Column("email", String, unique=True, nullable=False),
    Column("password_hash", String, nullable=False),
)

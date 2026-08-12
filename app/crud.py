from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncConnection

from app.core.db import user_table


async def find_user_by_email(db: AsyncConnection, email: str) -> Row | None:
    stmt = user_table.select().where(user_table.c.email == email)
    result = await db.execute(stmt)
    return result.fetchone()


async def find_user_by_id(db_conn: AsyncConnection, user_id: int) -> Row | None:
    stmt = user_table.select().where(user_table.c.uid == user_id)
    result = await db_conn.execute(stmt)
    return result.fetchone()

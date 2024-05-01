# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from model import User

async def get_user_by_username(db: AsyncSession, username: str) -> User:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def get_user_by_uid(db: AsyncSession, uid: int) -> User:
    return await db.get(User, uid)

async def create_user(db: AsyncSession, username: str, hashedPass: str) -> int | None:
    user = User(
        username = username,
        hashedPass = hashedPass
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user.uid

async def delete_user_by_id(db: AsyncSession, uid: int) -> None:
    stmt = delete(User).where(User.uid == uid)
    await db.execute(stmt)
    await db.commit()
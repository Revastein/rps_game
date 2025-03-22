from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import select

from backend.models.database import Session, UserOrm
from backend.models.schemas import UserBase, User, UserStatUpdate, UserAuthUpdate
from backend.secure import pwd_context, verify_password


class UserViews:
    @classmethod
    async def register(cls, data: UserBase) -> int:
        async with Session() as session:
            user = await session.execute(
                UserOrm.__table__.select().where(UserOrm.username == data.username)
            )
            if user.scalar_one_or_none():
                raise HTTPException(
                    status_code=409, detail="User with this login already exists"
                )
            user_dict = data.model_dump()
            user = UserOrm(**user_dict)
            user.password = pwd_context.hash(data.password)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.user_id

    @classmethod
    async def get_user_by_username(cls, username: str) -> Optional[UserOrm]:
        async with Session() as session:
            result = await session.execute(
                select(UserOrm).where(UserOrm.username == username)
            )
            return result.scalar_one_or_none()

    @classmethod
    async def login(cls, username: str, password: str) -> int:
        async with Session() as session:
            result = await session.execute(
                select(UserOrm).where(UserOrm.username == username)
            )
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            if not verify_password(password, user.password):
                raise HTTPException(status_code=401, detail="Incorrect password")
            return user.user_id

    @classmethod
    async def get_user(cls, user_id: int) -> User:
        async with Session() as session:
            user = await session.get(UserOrm, user_id)
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            return user

    @classmethod
    async def get_all_users(cls) -> List[User]:
        async with Session() as session:
            result = await session.execute(select(UserOrm))
            return result.scalars().all()

    @classmethod
    async def update_user_status(cls, user_id: int, status: str) -> None:
        async with Session() as session:
            user = await session.get(UserOrm, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            user.status = status
            await session.commit()

    @classmethod
    async def update_user_stat(cls, user_id: int, data: UserStatUpdate) -> None:
        async with Session() as session:
            user = await session.get(UserOrm, user_id)
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            for field, value in data.model_dump(exclude_unset=True).items():
                if value is not None:
                    setattr(user, field, value)
            await session.commit()

    @classmethod
    async def update_user_auth(cls, user_id: int, data: UserAuthUpdate) -> None:
        async with Session() as session:
            user = await session.get(UserOrm, user_id)
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            existing_user = await session.execute(
                select(UserOrm).where(UserOrm.username == data.username)
            )
            existing_user = existing_user.scalar_one_or_none()
            if existing_user and existing_user.user_id != user_id:
                raise HTTPException(status_code=400, detail="Username already exists")
            for field, value in data.model_dump(exclude_unset=True).items():
                if field == "password":
                    if value:
                        value = pwd_context.hash(value)
                if value is not None:
                    setattr(user, field, value)
            await session.commit()

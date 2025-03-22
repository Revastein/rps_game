from fastapi import HTTPException, status

from backend.models.database import Session, UserOrm
from backend.service.user_service import UserViews


class UserManager:
    @staticmethod
    async def update_status(user_id: int, user_status: str) -> None:
        await UserViews.update_user_status(user_id, user_status)

    @staticmethod
    async def get_online_status(user_id: int) -> str:
        async with Session() as session:
            user = await session.get(UserOrm, user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user.status


user_manager = UserManager()

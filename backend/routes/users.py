from typing import List

from fastapi import APIRouter

from backend.models.schemas import (
    User,
)
from backend.service.user_service import UserViews

router = APIRouter(tags=["Users"])


@router.get("/users/", response_model=List[User], status_code=200)
async def get_users():
    return await UserViews.get_all_users()


@router.get("/users/{user_id}", response_model=User, status_code=200)
async def get_user(user_id: int):
    return await UserViews.get_user(user_id)

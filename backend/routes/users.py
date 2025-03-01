from typing import List, Annotated

from fastapi import APIRouter, Depends

from backend.models.schemas import User, UserId, UserBase, UserStatUpdate, UserAuthUpdate
from backend.usecases.users import UserViews

router = APIRouter(
    tags=["Users"]
)


@router.post("/register", response_model=UserId, status_code=201)
async def create_user(user: UserBase):
    user_id = await UserViews.register(user)
    return {"user_id": user_id}


@router.post("/login", response_model=UserId, status_code=200)
async def login_user(user: UserBase):
    user_id = await UserViews.login(user.username, user.password)
    return {"user_id": user_id}


@router.get("/user/{user_id}", response_model=User, status_code=200)
async def get_user(user_id: int):
    user = await UserViews.get_user(user_id)
    return user


@router.get("/users/", response_model=List[User], status_code=200)
async def get_users():
    users = await UserViews.get_all_users()
    return users


@router.patch("/update_stat/", status_code=204)
async def update_user_stat(data: Annotated[UserStatUpdate, Depends()]):
    await UserViews.update_user_stat(data.user_id, data)


@router.patch("/update_auth/", status_code=204)
async def update_user_auth_data(data: Annotated[UserAuthUpdate, Depends()]):
    await UserViews.update_user_auth(data.user_id, data)

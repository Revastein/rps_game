from typing import Annotated

from fastapi import APIRouter, Depends

from backend.models.schemas import (
    UserStatUpdate,
    UserAuthUpdate,
)
from backend.secure.auth import admin_required
from backend.service.user_service import UserViews

router = APIRouter(tags=["Admin"], dependencies=[Depends(admin_required)])


@router.patch("/update_stat/", status_code=204)
async def update_user_stat(data: Annotated[UserStatUpdate, Depends()]):
    await UserViews.update_user_stat(data.user_id, data)


@router.patch("/update_auth/", status_code=204)
async def update_user_auth_data(data: Annotated[UserAuthUpdate, Depends()]):
    await UserViews.update_user_auth(data.user_id, data)

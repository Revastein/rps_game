from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.models.schemas import UserId, UserBase
from backend.secure import verify_password
from backend.secure.auth import SECRET_KEY, ALGORITHM
from backend.service.user_service import UserViews

router = APIRouter(tags=["Authorization"])


@router.post("/register", response_model=UserId, status_code=201)
async def create_user(user: Annotated[UserBase, Depends()]):
    return {"user_id": await UserViews.register(user)}


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserViews.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=60)
    expire = datetime.now(timezone.utc) + access_token_expires
    payload = {
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role,
        "exp": expire
    }
    access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"user_id": user.user_id, "access_token": access_token}

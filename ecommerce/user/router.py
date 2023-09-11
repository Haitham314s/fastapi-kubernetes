import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ecommerce.auth.jwt import get_current_user
from ecommerce.config import SUCCESS_RESPONSE

from .models import User
from .schema import UserGenOut, UserIn, UserOut
from .services import delete_user_service, get_all_users, new_user_register
from .validator import verify_email_exist

router = APIRouter(tags=["Users"], prefix="/user")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user_registration(user_in: UserIn = Depends(UserIn)):
    user = await verify_email_exist(user_in.email)
    if user is not None:
        raise HTTPException(
            status_code=400, detail="User with this email already exist"
        )

    new_user = await new_user_register(user_in)
    return new_user


@router.get("s", response_model=List[UserOut])
async def get_users(user: User = Depends(get_current_user)):
    return await get_all_users()


@router.get("", response_model=UserGenOut)
async def get_user(user: User = Depends(get_current_user)) -> UserGenOut:
    return UserGenOut.model_validate(user)


@router.delete("")
async def delete_user(user: User = Depends(get_current_user)):
    await delete_user_service(user)

    return SUCCESS_RESPONSE

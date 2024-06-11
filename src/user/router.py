from typing import List

from fastapi import APIRouter, Depends, status

from user.depends import get_user_usecase
from user.schemas import *
from user.use_cases import UserUseCase

user_router = APIRouter(tags=["user"], prefix="/user")


@user_router.get("/", response_model=List[User])
async def get_users(user_usecase: UserUseCase = Depends(get_user_usecase)):
    return await user_usecase.get_all_users()


@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: BaseUser, user_usecase: UserUseCase = Depends(get_user_usecase)):
    return await user_usecase.create_user(new_user)


@user_router.delete("/")
async def delete_user(user: DeleteUser, user_usecase: UserUseCase = Depends(get_user_usecase)):
    await user_usecase.delete_user(user.user_id)


@user_router.patch("/", response_model=User)
async def update_user(user: User, user_usecase: UserUseCase = Depends(get_user_usecase)):
    return await user_usecase.update_user(user)

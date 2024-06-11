from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from user.repository import UserRepository
from user.use_cases import UserUseCase
from core.database_depends import get_db


def get_user_repository(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_usecase(repo: UserUseCase = Depends(get_user_repository)) -> UserUseCase:
    return UserUseCase(repo)

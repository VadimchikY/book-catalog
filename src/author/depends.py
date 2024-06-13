from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from author.repository import AuthorRepository
from author.use_cases import AuthorUseCase
from core.database_depends import get_db


def get_author_repository(db: AsyncSession = Depends(get_db)) -> AuthorRepository:
    return AuthorRepository(db)


def get_author_usecase(repo: AuthorRepository = Depends(get_author_repository)) -> AuthorUseCase:
    return AuthorUseCase(repo)

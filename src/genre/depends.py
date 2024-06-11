from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from genre.repository import GenreRepository
from genre.use_cases import GenreUseCase
from core.database_depends import get_db


def get_genre_repository(db: AsyncSession = Depends(get_db)) -> GenreRepository:
    return GenreRepository(db)


def get_genre_usecase(repo: GenreUseCase = Depends(get_genre_repository)) -> GenreUseCase:
    return GenreUseCase(repo)

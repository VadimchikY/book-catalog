from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from book.repository import BookRepository
from book.use_cases import BookUseCase
from core.database_depends import get_db


def get_book_repository(db: AsyncSession = Depends(get_db)) -> BookRepository:
    return BookRepository(db)


def get_book_usecase(repo: BookUseCase = Depends(get_book_repository)) -> BookUseCase:
    return BookUseCase(repo)

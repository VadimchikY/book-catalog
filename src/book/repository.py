from typing import List

from sqlalchemy import delete, select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from book import model
from book.schemas import BookBase, Book, ExtendBook
from core.exceptions import DatabaseException
from genre.model import Genre


class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_book(self, book: BookBase) -> Book:
        try:
            query = insert(model.Book).values(**book.dict()).returning(model.Book)
            result = await self.db.execute(query)
            return Book.from_orm(result.scalar())
        except Exception:
            await self.db.rollback()
            raise DatabaseException

    async def get_all_books(self) -> List[Book]:
        try:
            query = select(model.Book)
            result = await self.db.execute(query)
            books = [Book.from_orm(db_book) for db_book in result.scalars().all()]
            return books
        except Exception:
            raise DatabaseException

    async def get_book(self, book_id: int) -> ExtendBook | None:
        # try:
        result = await self.db.execute(
            select(model.Book)
            .options(joinedload(model.Book.author), joinedload(model.Book.genres), joinedload(model.Book.user))
            .filter(model.Book.book_id == book_id)
        )
        book = result.unique().scalars().first()
        return ExtendBook.from_orm(book)
        # except Exception:
        #     raise DatabaseException

    async def update_book(self, book: Book) -> Book | None:
        try:
            query = (
                update(model.Book)
                .where(model.Book.book_id == book.book_id)
                .values(**book.dict())
                .returning(model.Book)
            )
            result = await self.db.execute(query)
            return Book.from_orm(result.scalar())
        except Exception:
            await self.db.rollback()
            raise DatabaseException

    async def delete_book(self, book_id: int) -> None:
        try:
            query = delete(model.Book).where(model.Book.book_id == book_id)
            await self.db.execute(query)
        except Exception:
            await self.db.rollback()
            raise DatabaseException

    async def update_genres(self, book_id: int, genres: List[Genre]) -> None:
        # try:
        result = await self.db.execute(
            select(model.Book).options(selectinload(model.Book.genres)).filter_by(book_id=book_id))
        db_book = result.scalar_one()
        result = await self.db.execute(select(Genre).where(Genre.genre_id.in_(genres)))
        db_genres = result.scalars().all()
        db_book.genres = []
        db_book.genres.extend(db_genres)
        # except Exception:
        #     await self.db.rollback()
        #     raise DatabaseException

    async def restore_user(self, book_id) -> str:
        try:
            query = select(model.Book).where(model.Book.book_id == book_id)
            result = await self.db.execute(query)
            book = result.scalar()
            book.user_id = None
            return book.task_id
        except Exception:
            raise DatabaseException

    async def reserve_book(self, book_id: int, user_id: int, task_id: str) -> None:
        try:
            query = select(model.Book).where(model.Book.book_id == book_id)
            print("sss5")
            result = await self.db.execute(query)
            book = result.scalar()
            book.user_id = user_id
            book.task_id = task_id
            print("sss6")
        except Exception:
            raise DatabaseException

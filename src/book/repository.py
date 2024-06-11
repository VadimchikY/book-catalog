from typing import List

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from book import model
from book.schemas import BookBase, Book
from core.exceptions import DatabaseException
from genre.model import Genre


class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_book(self, book: BookBase) -> Book:
        try:
            query = (insert(model.Book).values(title=book.title,
                                               price=book.price,
                                               pages=book.pages,
                                               author_id=book.author_id)
                     .returning(model.Book))
            result = await self.db.execute(query)
            db_book = result.scalar_one()

            for genre_id in book.genres:
                query = select(Genre).where(Genre.genre_id == genre_id)
                result = await self.db.execute(query)
                db_genre = result.scalar_one()
                db_book.genres.append(db_genre)
            return Book.from_orm(db_book)
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

    async def get_book(self, book_id: int) -> Book | None:
        try:
            query = select(model.Book).where(model.Book.book_id == book_id)
            result = await self.db.execute(query)
            return Book.from_orm(result.scalar())
        except Exception:
            raise DatabaseException

    async def update_book(self, book: Book) -> Book | None:
        try:
            query = (
                update(model.Book)
                .where(model.Book.book_id == book.book_id)
                .values(**book.dict())
                .returning(model.Book)
            )
            result = await self.db.execute(query)
            db_book = result.scalar()

            db_book.genres = []
            for genre_id in book.genres:
                query = select(Genre).where(Genre.genre_id == genre_id)
                result = await self.db.execute(query)
                db_genre = result.scalar()
                if db_genre:
                    db_book.genres.append(db_genre)
            return Book.from_orm(db_book)
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
            result = await self.db.execute(query)
            book = result.scalar()
            book.user_id = user_id
            book.task_id = task_id
        except Exception:
            raise DatabaseException

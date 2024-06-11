from typing import List

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from author import model
from author.schemas import BaseAuthor, Author
from core.exceptions import DatabaseException


class AuthorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_author(self, author: BaseAuthor) -> Author:
        try:
            query = insert(model.Author).values(**author.dict()).returning(model.Author)
            result = await self.db.execute(query)
            return Author.from_orm(result.scalar())
        except Exception:
            await self.db.rollback()
            raise DatabaseException

    async def get_all_authors(self) -> List[Author]:
        try:
            query = select(model.Author)
            result = await self.db.execute(query)
            authors = [Author.from_orm(db_author) for db_author in result.scalars().all()]
            return authors
        except Exception:
            raise DatabaseException

    async def update_author(self, author: Author) -> Author | None:
        try:
            query = (
                update(model.Author)
                .where(model.Author.author_id == author.author_id)
                .values(**author.dict())
                .returning(model.Author)
            )
            result = await self.db.execute(query)
            return Author.from_orm(result.scalar())
        except Exception:
            await self.db.rollback()
            raise DatabaseException

    async def delete_author(self, author_id: int) -> None:
        try:
            query = delete(model.Author).where(model.Author.author_id == author_id)
            await self.db.execute(query)
        except Exception:
            await self.db.rollback()
            raise DatabaseException

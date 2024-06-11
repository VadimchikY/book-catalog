from typing import List

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import DatabaseException
from genre import model
from genre.schemas import BaseGenre, Genre


class GenreRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_genre(self, genre: BaseGenre) -> Genre:
        try:
            query = insert(model.Genre).values(**genre.dict()).returning(model.Genre)
            result = await self.db.execute(query)
            return Genre.from_orm(result.scalar())
        except Exception:
            await self.db.rollback()
            raise DatabaseException

    async def get_all_genres(self) -> List[Genre]:
        try:
            query = select(model.Genre)
            result = await self.db.execute(query)
            genres = [Genre.from_orm(db_genre) for db_genre in result.scalars().all()]
            return genres
        except Exception:
            raise DatabaseException

    async def update_genre(self, genre: Genre) -> Genre | None:
        try:
            query = (
                update(model.Genre)
                .where(model.Genre.genre_id == genre.genre_id)
                .values(**genre.dict())
                .returning(model.Genre)
            )
            result = await self.db.execute(query)
            return Genre.from_orm(result.scalar())
        except Exception:
            await self.db.rollback()
            raise DatabaseException

    async def delete_genre(self, genre_id: int) -> None:
        try:
            query = delete(model.Genre).where(model.Genre.genre_id == genre_id)
            await self.db.execute(query)
        except Exception:
            await self.db.rollback()
            raise DatabaseException

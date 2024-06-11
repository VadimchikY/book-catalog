from typing import List

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from user import model
from user.schemas import BaseUser, User
from core.exceptions import DatabaseException


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: BaseUser) -> User:
        try:
            query = insert(model.User).values(**user.dict()).returning(model.User)
            result = await self.db.execute(query)
            return User.from_orm(result.scalar())
        except Exception:
            await self.db.rollback()
            raise DatabaseException

    async def get_all_users(self) -> List[User]:
        try:
            query = select(model.User)
            result = await self.db.execute(query)
            users = [User.from_orm(db_user) for db_user in result.scalars().all()]
            return users
        except Exception:
            raise DatabaseException

    async def update_user(self, user: User) -> User | None:
        try:
            query = (
                update(model.User)
                .where(model.User.user_id == user.user_id)
                .values(**user.dict())
                .returning(model.User)
            )
            result = await self.db.execute(query)
            return User.from_orm(result.scalar())
        except Exception:
            await self.db.rollback()
            raise DatabaseException

    async def delete_user(self, user_id: int) -> None:
        try:
            query = delete(model.User).where(model.User.user_id == user_id)
            await self.db.execute(query)
        except Exception:
            await self.db.rollback()
            raise DatabaseException

from fastapi import Depends

from core.orm_engine import SQLAlchemy
from core.settings import settings


class SQLAlchemyDependency:
    def __init__(self):
        self.sqlalchemy = None

    async def __call__(self) -> SQLAlchemy:
        self.sqlalchemy = SQLAlchemy.start(settings.DB_URL) if not self.sqlalchemy else self.sqlalchemy
        return self.sqlalchemy


get_sql_alchemy = SQLAlchemyDependency()


async def get_db(sqlalchemy: SQLAlchemy = Depends(get_sql_alchemy)):
    async with sqlalchemy.session_maker() as session:
        async with session.begin():
            yield session

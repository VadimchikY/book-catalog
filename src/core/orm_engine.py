from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.exceptions import DatabaseConnectionException


class SQLAlchemy:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    @classmethod
    def start(cls, db_url):
        try:
            engine = create_async_engine(db_url, echo=True, future=True)
            async_session = async_sessionmaker(engine, expire_on_commit=False)
            return cls(async_session)
        except Exception:
            raise DatabaseConnectionException

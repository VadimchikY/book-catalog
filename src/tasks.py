import asyncio

from celery import Celery

from book.repository import BookRepository
from core.database_depends import get_sql_alchemy, get_db

celery_app = Celery('tasks', broker='redis://redis:6379/0')


@celery_app.task
def return_book_task(book_id):
    async def _return_book_task(book_id):
        sqlalchemy = await get_sql_alchemy()
        async with sqlalchemy.session_maker() as session:
            repo = BookRepository(session)
            await repo.restore_user(book_id)

    asyncio.run(_return_book_task(book_id))

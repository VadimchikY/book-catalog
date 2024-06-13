import asyncio

from celery import Celery

from book.repository import BookRepository
from core.database_depends import get_db


celery_app = Celery('tasks', broker='redis://redis:6379/0')


async def return_book_async(book_id):
    async with get_db() as session:
        repo = BookRepository(session)
        await repo.restore_user(book_id)


@celery_app.task
def return_book_task(book_id):
    asyncio.run(return_book_async(book_id))

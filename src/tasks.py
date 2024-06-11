from celery import Celery

from book.repository import BookRepository
from core.database_depends import get_db


celery_app = Celery('tasks', broker='redis://redis:6379/0')


@celery_app.task
async def return_book(self, book_id):
    async with get_db() as session:
        repo = BookRepository(session)
        await repo.restore_user(book_id)

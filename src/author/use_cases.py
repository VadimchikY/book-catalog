
from author.repository import AuthorRepository
from author.schemas import BaseAuthor, Author


class AuthorUseCase:
    def __init__(self, repo: AuthorRepository):
        self.repo = repo

    async def create_author(self, author: BaseAuthor):
        return await self.repo.create_author(author)

    async def update_author(self, author: Author):
        return await self.repo.update_author(author)

    async def get_all_authors(self):
        return await self.repo.get_all_authors()

    async def delete_author(self, author_id: int):
        await self.repo.delete_author(author_id)
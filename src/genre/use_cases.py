
from genre.repository import GenreRepository
from genre.schemas import BaseGenre, Genre


class GenreUseCase:
    def __init__(self, repo: GenreRepository):
        self.repo = repo

    async def create_genre(self, genre: BaseGenre):
        return await self.repo.create_genre(genre)

    async def update_genre(self, genre: Genre):
        return await self.repo.update_genre(genre)

    async def get_all_genres(self):
        return await self.repo.get_all_genres()

    async def delete_genre(self, genre_id: int):
        await self.repo.delete_genre(genre_id)

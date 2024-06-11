
from user.repository import UserRepository
from user.schemas import BaseUser, User


class UserUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, user: BaseUser):
        return await self.repo.create_user(user)

    async def update_user(self, user: User):
        return await self.repo.update_user(user)

    async def get_all_users(self):
        return await self.repo.get_all_users()

    async def delete_user(self, user_id: int):
        await self.repo.delete_user(user_id)

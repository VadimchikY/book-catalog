from pydantic import BaseModel


class BaseUser(BaseModel):
    first_name: str
    last_name: str
    avatar: str

    class Config:
        from_attributes=True


class DeleteUser(BaseModel):
    user_id: int


class User(BaseUser, DeleteUser):
    pass

from app.core.domain.entities.user import User
from app.core.domain.repositories.user_repository import UserRepository


class ListUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self) -> list[User]:

        users = self.user_repository.get_all()

        return users

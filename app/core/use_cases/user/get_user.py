from app.core.domain.entities.user import User
from app.core.domain.repositories.user_repository import UserRepository
from app.core.domain.value_objects.uuidv7_vo import UUIDv7


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, id: str) -> User:

        id_vo = UUIDv7(id)

        user_data = self.user_repository.get_by_id(id_vo)

        if not user_data:
            raise ValueError(f"User with id '{id}' does not found.")

        else:
            return user_data

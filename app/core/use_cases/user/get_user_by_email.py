from app.core.domain.entities.user import User
from app.core.domain.repositories.user_repository import UserRepository
from app.core.domain.value_objects.email_vo import Email


class GetUserByEmailUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, email: str) -> User:

        email_vo = Email(email)

        user_data = self.user_repository.get_by_email(email=email_vo)

        if not user_data:
            raise ValueError(f"User with email '{email}' does not found.")

        else:
            return user_data

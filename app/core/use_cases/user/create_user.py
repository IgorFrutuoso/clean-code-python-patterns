import datetime

from app.core.domain.interfaces.password_hasher import PasswordHasher
from app.core.domain.entities.user import User
from app.core.domain.repositories.user_repository import UserRepository
from app.core.domain.value_objects.document_vo import Document
from app.core.domain.value_objects.email_vo import Email
from app.core.domain.value_objects.password_vo import Password
from app.core.domain.value_objects.person_name_vo import PersonName
from app.core.domain.value_objects.phone_number_vo import PhoneNumber
from app.core.domain.value_objects.uuidv7_vo import UUIDv7


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(
        self,
        document_str: str,
        name_str: str,
        email_str: str,
        phone_number_str: str,
        password_str: str,
        password_hasher: PasswordHasher,
        creator_id: str,
        admin: bool = False,
        super_admin: bool = False
    ) -> str | None:

        creator_user = self.user_repository.get_by_id(UUIDv7(creator_id))
        if not creator_user:
            raise ValueError(f"Creator with id '{creator_id}' does not exist.")

        if super_admin == True and creator_user.super_admin == False:
            raise ValueError("Only super admins can create super admins.")

        if creator_user.admin == False:
            raise ValueError("Only admins can create new users.")

        id_vo = UUIDv7(None)
        document_vo = Document(document_str)
        name_vo = PersonName(name_str)
        email_vo = Email(email_str)
        phone_number_vo = PhoneNumber(phone_number_str)
        password_vo = Password(password_str, password_hasher)

        email_user = self.user_repository.get_by_email(email_vo)
        if email_user and email_user.email == email_vo:
            raise ValueError(f"The email '{email_str}' is already in use.")

        phone_user = self.user_repository.get_by_phone_number(phone_number_vo)
        if phone_user and phone_user.phone == phone_number_vo:
            raise ValueError(
                f"The phone number '{phone_number_str}' is already in use.")

        document_user = self.user_repository.get_by_document(document_vo)
        if document_user and document_user.document == document_vo:
            raise ValueError(
                f"The document '{document_str}' is already in use.")

        current_data = str(datetime.datetime.now(
            datetime.timezone.utc).isoformat())

        user = User(
            id=id_vo,
            document=document_vo,
            name=name_vo,
            email=email_vo,
            phone=phone_number_vo,
            password=password_vo,
            created_at_utc=current_data,
            updated_at_utc=current_data,
            last_accessed_at_utc="",
            admin=admin,
            super_admin=super_admin,
        )

        user_uuid = self.user_repository.create(user)

        return user_uuid.value

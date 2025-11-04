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


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(
        self,
        creator_id: str,
        id_str: str,
        password_hasher: PasswordHasher | None = None,
        document_str: str | None = None,
        name_str: str | None = None,
        email_str: str | None = None,
        phone_number_str: str | None = None,
        password_str: str | None = None,
        last_accessed_at_utc_str: str | None = None,
        admin: bool | None = None,
    ) -> None:

        creator_user = self.user_repository.get_by_id(UUIDv7(creator_id))

        if not creator_user:
            raise ValueError(f"Creator with id '{creator_id}' does not exist.")

        if admin == True and creator_user.admin == False and creator_user.super_admin == False:
            raise ValueError(f"Only admin can change admin permissions.")

        id_vo = UUIDv7(id_str)

        existing_user = self.user_repository.get_by_id(id_vo)

        if not existing_user:
            raise ValueError(f"User with id '{id_str}' does not exist.")

        document_vo = Document(
            document_str) if document_str else existing_user.document
        name_vo = PersonName(name_str) if name_str else existing_user.name
        email_vo = Email(email_str) if email_str else existing_user.email
        phone_number_vo = PhoneNumber(
            phone_number_str) if phone_number_str else existing_user.phone
        is_admin = admin if admin is not None else existing_user.admin
        has_last_accessed_at_utc = last_accessed_at_utc_str if last_accessed_at_utc_str else existing_user.last_accessed_at_utc

        if document_str:
            document_user = self.user_repository.get_by_document(document_vo)
            if document_user and document_user.id != id_vo:
                raise ValueError(
                    f"The document '{document_str}' is already in use.")

        if email_str:
            email_user = self.user_repository.get_by_email(email_vo)
            if email_user and email_user.id != id_vo:
                raise ValueError(f"The email '{email_str}' is already in use.")

        if phone_number_str:
            phone_user = self.user_repository.get_by_phone_number(
                phone_number_vo)
            if phone_user and phone_user.id != id_vo:
                raise ValueError(
                    f"The phone number '{phone_number_str}' is already in use.")

        if password_str and not password_hasher:
            raise ValueError(
                "Password hasher must be provided when updating password.")

        password_vo = Password(
            password_str, password_hasher) if password_str and password_hasher else existing_user.password

        current_data = datetime.datetime.now(datetime.timezone.utc).isoformat()

        user = User(
            id=id_vo,
            document=document_vo,
            name=name_vo,
            email=email_vo,
            phone=phone_number_vo,
            password=password_vo,
            created_at_utc=existing_user.created_at_utc,
            updated_at_utc=current_data,
            last_accessed_at_utc=existing_user.last_accessed_at_utc,
            admin=is_admin,
            super_admin=existing_user.super_admin
        )

        self.user_repository.update(user)

        return None

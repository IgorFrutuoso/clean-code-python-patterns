from abc import ABC, abstractmethod

from app.core.domain.entities.user import User
from app.core.domain.value_objects.document_vo import Document
from app.core.domain.value_objects.email_vo import Email
from app.core.domain.value_objects.phone_number_vo import PhoneNumber
from app.core.domain.value_objects.uuidv7_vo import UUIDv7


class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: UUIDv7) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def create(self, user: User) -> UUIDv7:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: Email) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_phone_number(self, telefone: PhoneNumber) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_document(self, document: Document) -> User | None:
        raise NotImplementedError

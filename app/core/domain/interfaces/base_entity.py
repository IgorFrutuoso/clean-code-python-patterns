from abc import ABC, abstractmethod

from app.core.domain.value_objects.document_vo import Document
from app.core.domain.value_objects.person_name_vo import PersonName
from app.core.domain.value_objects.phone_number_vo import PhoneNumber
from app.core.domain.value_objects.email_vo import Email
from app.core.domain.value_objects.uuidv7_vo import UUIDv7


class BaseEntity(ABC):
    @abstractmethod
    def __init__(self,
                 id: UUIDv7,
                 document: Document,
                 name: PersonName,
                 email: Email,
                 phone: PhoneNumber,
                 created_at_utc: str,
                 updated_at_utc: str,
                 ) -> None:
        self.id = id
        self.document = document
        self.name = name
        self.email = email
        self.phone = phone
        self.created_at_utc = created_at_utc
        self.updated_at_utc = updated_at_utc

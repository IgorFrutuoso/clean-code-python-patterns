from app.core.domain.interfaces.base_entity import BaseEntity
from app.core.domain.value_objects.document_vo import Document
from app.core.domain.value_objects.email_vo import Email
from app.core.domain.value_objects.password_vo import Password
from app.core.domain.value_objects.person_name_vo import PersonName
from app.core.domain.value_objects.phone_number_vo import PhoneNumber
from app.core.domain.value_objects.uuidv7_vo import UUIDv7


class User(BaseEntity):

    def __init__(self,
                 id: UUIDv7,
                 document: Document,
                 name: PersonName,
                 email: Email,
                 phone: PhoneNumber,
                 created_at_utc: str,
                 updated_at_utc: str,
                 last_accessed_at_utc: str,
                 password: Password,
                 admin: bool = False,
                 super_admin: bool = False,
                 ) -> None:

        super().__init__(
            id,
            document,
            name,
            email,
            phone,
            created_at_utc,
            updated_at_utc)
        self.last_accessed_at_utc = last_accessed_at_utc
        self.password = password
        self.admin = admin
        self.super_admin = super_admin

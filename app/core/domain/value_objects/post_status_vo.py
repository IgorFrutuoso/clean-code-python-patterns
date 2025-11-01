from dataclasses import dataclass
from enum import Enum


class StatusEnum(Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"


@dataclass(frozen=True)
class PostStatus:

    status: StatusEnum

    def __post_init__(self):
        if not isinstance(self.status, StatusEnum):
            raise ValueError("Status must be an instance of StatusEnum")

        object.__setattr__(self, "status", self.status)

    def __str__(self):
        """ Returns the string representation of the status. """
        return self.status.name

    def __repr__(self):
        """ Returns an unambiguous developer represtentation of the status. """
        return f"PostStatus(status={self.status})"

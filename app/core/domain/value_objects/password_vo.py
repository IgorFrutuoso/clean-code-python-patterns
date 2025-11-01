import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Pattern

if TYPE_CHECKING:
    from app.core.domain.interfaces.password_hasher import PasswordHasher


@dataclass(frozen=True)
class Password:
    value: str

    password_hasher: "PasswordHasher"

    is_hashed: bool = False

    __REGEX_VALID_CHARACTERS: ClassVar[Pattern[str]] = re.compile(
        r'^[a-zA-Z0-9!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]+$')

    __MIN_LENGTH: ClassVar[int] = 8

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError("Password must be a string")

        if self.is_hashed:
            object.__setattr__(self, 'value', self.value)

        else:
            if not self.__REGEX_VALID_CHARACTERS.fullmatch(self.value):
                raise ValueError(
                    "Password contains invalid characters. Only alphanumeric and special characters are allowed."
                )

            if len(self.value) < self.__MIN_LENGTH:
                raise ValueError(
                    "Password must be at least 8 characters long.")

            hashed_value = self.password_hasher.hash(self)

            object.__setattr__(self, 'value', hashed_value)

            object.__setattr__(self, 'is_hashed', True)

    def __str__(self) -> str:
        return "*" * len(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}({'*' * len(self.value)})"

from dataclasses import dataclass
from typing import ClassVar, Pattern
import re


@dataclass(frozen=True)
class PersonName:
    name: str

    __MAX_LENGTH: ClassVar[int] = 100

    __PERSON_NAME_CARACTERS: ClassVar[Pattern[str]] = re.compile(
        r'^[a-zA-Z\s\u00C0-\u00FF]+$')

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError("Person name must be a string")

        cleaned_name = ' '.join(self.name.split()).strip()

        if not cleaned_name:
            raise ValueError(
                "Person name cannot be empty or whitespace only"
            )

        if len(cleaned_name) > self.__MAX_LENGTH:
            raise ValueError(
                f"Person name length ({len(cleaned_name)}) invalid (must be 1-{self.__MAX_LENGTH})"
            )

        if not self.__PERSON_NAME_CARACTERS.fullmatch(cleaned_name):
            raise ValueError(
                f"Invalid person name format: '{self.name}'."
            )

        object.__setattr__(self, 'name', cleaned_name)

    def __str__(self) -> str:
        """Returns the person's name string."""
        return self.name

    def __repr__(self) -> str:
        """Returns the unambiguous developer representation."""
        return f"PersonName(name='{self.name}')"

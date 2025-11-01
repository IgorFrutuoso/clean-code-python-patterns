from dataclasses import dataclass
from typing import ClassVar, Pattern
import re


@dataclass(frozen=True)
class Email:
    address: str

    # _EMAIL_REGEX: ClassVar[Pattern[str]] = re.compile(
    #     r"^[a-zA-Z0-9!#$%&'*+/=?^_\`{|}~.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9-]+$"
    # )

    __LOCAL_REGEX: ClassVar[Pattern[str]] = re.compile(
        r"^[a-zA-Z0-9_.-]+$"
    )

    __DOMAIN_REGEX: ClassVar[Pattern[str]] = re.compile(
        r"^[a-zA-Z0-9.-]+$"
    )

    __LABEL_REGEX: ClassVar[Pattern[str]] = re.compile(
        r"^[a-zA-Z0-9-]+$"
    )

    __MAX_LOCAL_PART_LEN: ClassVar[int] = 60
    __MAX_DOMAIN_PART_LEN: ClassVar[int] = 190
    __MAX_TOTAL_LEN: ClassVar[int] = 250

    def __post_init__(self):
        if not isinstance(self.address, str):
            raise TypeError("Email address must be a string")

        cleaned_address = self.address.strip()

        if not cleaned_address:
            raise ValueError(
                "Email address cannot be empty or whitespace only")

        if not (0 < len(cleaned_address) <= self.__MAX_TOTAL_LEN):
            raise ValueError(
                f"Email total length ({len(cleaned_address)}) invalid (must be 1-{self.__MAX_TOTAL_LEN})")

        try:
            local_part, domain_part = cleaned_address.split('@', 1)
        except ValueError:
            # Deveria ser pego pelo regex, mas é uma garantia extra
            raise ValueError("Email address must contain exactly one '@'")

        if not (0 < len(local_part) <= self.__MAX_LOCAL_PART_LEN):
            raise ValueError(
                f"Email local part length ({len(local_part)}) invalid (must be 1-{self.__MAX_LOCAL_PART_LEN})")

        if local_part.startswith('.') or local_part.endswith('.'):
            raise ValueError("Email local part cannot start or end with a dot")

        if '..' in local_part:
            raise ValueError(
                "Email local part cannot contain consecutive dots")

        if not self.__LOCAL_REGEX.fullmatch(local_part):
            raise ValueError(
                f"Email local part '{local_part}' contains invalid characters")

        if not (0 < len(domain_part) <= self.__MAX_DOMAIN_PART_LEN):
            raise ValueError(
                f"Email domain part length ({len(domain_part)}) invalid (must be 1-{self.__MAX_DOMAIN_PART_LEN})")

        if not self.__DOMAIN_REGEX.fullmatch(domain_part):
            raise ValueError(
                f"Email domain part '{domain_part}' contains invalid characters")

        domain_labels = domain_part.split('.')

        # Precisa de pelo menos dominio.tld
        if not domain_labels or len(domain_labels) < 2:
            raise ValueError(
                "Email domain must include at least one dot and a TLD")

        for label in domain_labels:
            if not label:  # Checa rótulos vazios (ex: domain..com)
                raise ValueError(
                    "Email domain cannot have empty labels (consecutive dots)")
            if label.startswith('-') or label.endswith('-'):
                raise ValueError(
                    f"Email domain label '{label}' cannot start or end with a hyphen")
            # Checa caracteres inválidos (redundante se o regex inicial for bom, mas seguro)
            if not self.__LABEL_REGEX.fullmatch(label):
                raise ValueError(
                    f"Email domain label '{label}' contains invalid characters")

        object.__setattr__(self, 'address', cleaned_address)

    def get_local_part(self) -> str:
        """Returns the local part of the email address (before @)."""
        return self.address.split('@', 1)[0]

    def get_domain(self) -> str:
        """Returns the domain part of the email address (after @)."""
        return self.address.split('@', 1)[1]

    def __str__(self) -> str:
        """Returns the email address string."""
        return self.address

    def __repr__(self) -> str:
        """Returns the unambiguous developer representation."""
        return f"Email(address='{self.address}')"

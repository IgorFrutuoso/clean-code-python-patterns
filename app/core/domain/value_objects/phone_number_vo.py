from dataclasses import dataclass
from typing import ClassVar, Pattern, Set
import re


@dataclass(frozen=True)
class PhoneNumber:
    number: str

    __PHONE_REGEX: ClassVar[Pattern[str]] = re.compile(
        r"^55[1-9][0-9]{1}\d{9}$"
    )

    __VALID_CARACTERS: ClassVar[Pattern[str]] = re.compile(
        r"^[0-9\-()+]+$"
    )

    __MAX_LENGTH: ClassVar[int] = 30

    __DDD_CODES_BRAZIL: ClassVar[Set[str]] = {
        "11", "12", "13", "14", "15", "16", "17", "18", "19",  # São Paulo
        "21", "22", "24",  # Rio de Janeiro
        "27", "28",  # Espírito Santo
        "31", "32", "33", "34", "35", "37", "38",  # Minas Gerais
        "41", "42", "43", "44", "45", "46",  # Paraná
        "47", "48", "49",  # Santa Catarina
        "51", "53", "54", "55",  # Rio Grande do Sul
        "61",  # Distrito Federal
        "62", "64",  # Goiás
        "63",  # Tocantins
        "65", "66",  # Mato Grosso
        "67",  # Mato Grosso do Sul
        "68",  # Acre
        "69",  # Rondônia
        "71", "73", "74", "75", "77",  # Bahia
        "79",  # Sergipe
        "81", "87",  # Pernambuco
        "82",  # Alagoas
        "83",  # Paraíba
        "84",  # Rio Grande do Norte
        "85", "88",  # Ceará
        "86", "89",  # Piauí
        "91", "93", "94",  # Pará
        "92", "97",  # Amazonas
        "95",  # Roraima
        "96",  # Amapá
        "98", "99"  # Maranhão
    }

    def __post_init__(self):
        if not isinstance(self.number, str):
            raise TypeError("Phone number must be a string")

        cleaned_number = self.number.strip()

        if not cleaned_number:
            raise ValueError(
                "Phone number cannot be empty or whitespace only")

        if not self.__VALID_CARACTERS.fullmatch(cleaned_number):
            raise ValueError(
                f"Phone number contains invalid characters ({cleaned_number})")

        if not (0 < len(cleaned_number) <= self.__MAX_LENGTH):
            raise ValueError(
                f"Phone number length ({len(cleaned_number)}) invalid (must be 1-{self.__MAX_LENGTH})")

        number = re.sub(r'\D', '', cleaned_number)

        if not number.startswith("55"):
            number = "55" + number

        ddi = number[:2]

        ddd = number[2:4]
        if ddd not in self.__DDD_CODES_BRAZIL:
            raise ValueError(f"Invalid DDD code: {ddd}")

        remainder = number[4:]

        if len(remainder) < 8 or len(remainder) > 9:
            raise ValueError(
                f"Invalid phone number length without ddi and ddd: {len(remainder)}")

        if len(remainder) < 9:
            remainder = "9" + remainder

        formated_number = f"{ddi}{ddd}{remainder[:5]}{remainder[5:]}"

        if not self.__PHONE_REGEX.fullmatch(formated_number):
            raise ValueError(
                f"Invalid phone number format: '{formated_number}'")

        object.__setattr__(self, 'number', formated_number)

    def __str__(self) -> str:
        return f"+{self.number[:2]} ({self.number[2:4]}) {self.number[4:5]}{self.number[5:9]}-{self.number[9:]}"

    def __repr__(self) -> str:
        return f"PhoneNumber(number='{self.number}')"

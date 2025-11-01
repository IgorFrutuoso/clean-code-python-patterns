import re
from dataclasses import dataclass
from typing import ClassVar, Pattern


@dataclass(frozen=True)
class Document:
    value: str

    __REGEX_VALID_CHARACTERS: ClassVar[Pattern[str]] = re.compile(
        r'^[0-9./-]+$')

    def __post_init__(self):
        if not isinstance(self.value, str):
            raise TypeError(f"Value must be a string")

        if not self.__REGEX_VALID_CHARACTERS.match(self.value):
            raise ValueError(
                f"Value must contain only numbers and optional special characters (./-)")

        only_numbers_value = re.sub(r'\D', '', self.value).strip()

        if len(only_numbers_value) == 11:
            if not Document.__is_valid_cpf(only_numbers_value):
                raise ValueError("Failed validation algorithm for CPF")

        elif len(only_numbers_value) == 14:
            if not Document.__is_valid_cnpj(only_numbers_value):
                raise ValueError("Failed validation algorithm for CNPJ")

        else:
            raise ValueError(
                f"Invalid document length ({len(only_numbers_value)}). Must be 11 (CPF) or 14 (CNPJ) digits")

        object.__setattr__(self, "value", only_numbers_value)

    @staticmethod
    def __is_valid_cnpj(cnpj: str) -> bool:
        if len(cnpj) != 14 or len(set(cnpj)) == 1:
            return False

        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        if digito1 != int(cnpj[12]):
            return False

        pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        if digito2 != int(cnpj[13]):
            return False

        return True

    @staticmethod
    def __is_valid_cpf(cpf: str) -> bool:
        if len(cpf) != 11 or len(set(cpf)) == 1:
            return False

        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = (soma * 10) % 11
        digito1 = resto if resto < 10 else 0
        if digito1 != int(cpf[9]):
            return False

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = (soma * 10) % 11
        digito2 = resto if resto < 10 else 0
        if digito2 != int(cpf[10]):
            return False

        return True

    def is_cpf(self) -> bool:

        return len(self.value) == 11

    def is_cnpj(self) -> bool:

        return len(self.value) == 14

    def formatted(self) -> str:
        if self.is_cpf():
            return f"{self.value[:3]}.{self.value[3:6]}.{self.value[6:9]}-{self.value[9:]}"

        elif self.is_cnpj():
            return f"{self.value[:2]}.{self.value[2:5]}.{self.value[5:8]}/{self.value[8:12]}-{self.value[12:]}"

        else:
            return self.value

    def __str__(self) -> str:
        return self.formatted()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

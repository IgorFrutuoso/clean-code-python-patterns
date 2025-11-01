from abc import ABC, abstractmethod

from app.core.domain.value_objects.password_vo import Password


class PasswordHasher(ABC):

    @abstractmethod
    def hash(self, password: Password) -> str:
        """
        Hashes the provided plain-text password securely.

        Args:
            password: The Password Value Object containing the plain-text password
                      that has already passed complexity validation.

        Returns:
            A string representation of the generated password hash,
            suitable for persistent storage.
        """
        pass

    @abstractmethod
    def verify(self, password: Password, hashed_password: str) -> bool:
        """
        Verifies a plain-text password attempt against a stored hash.

        Args:
            password: The Password Value Object containing the plain-text password attempt.
            hashed_password: The stored hash string retrieved from storage.

        Returns:
            True if the password attempt matches the hash, False otherwise.
        """
        pass

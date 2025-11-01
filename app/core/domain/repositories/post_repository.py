from abc import ABC, abstractmethod

from app.core.domain.entities.post import Post
from app.core.domain.value_objects.uuidv7_vo import UUIDv7


class PostRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: UUIDv7) -> Post | None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, user_id: UUIDv7) -> list[Post]:
        raise NotImplementedError

    @abstractmethod
    def create(self, post: Post) -> UUIDv7:
        raise NotImplementedError

    @abstractmethod
    def update(self, post: Post) -> None:
        raise NotImplementedError

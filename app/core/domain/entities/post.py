from app.core.domain.value_objects.post_status_vo import PostStatus
from app.core.domain.value_objects.uuidv7_vo import UUIDv7


class Post():

    def __init__(self,
                 id: UUIDv7,
                 user_id: UUIDv7,
                 image: str | None,
                 title: str,
                 link: str | None,
                 description: str,
                 body_content: str,
                 status: PostStatus,
                 created_at_utc: str,
                 updated_at_utc: str
                 ) -> None:

        self.id = id
        self.user_id = user_id
        self.image = image
        self.title = title
        self.link = link
        self.description = description
        self.body_content = body_content
        self.status = status
        self.created_at_utc = created_at_utc
        self.updated_at_utc = updated_at_utc
from sqlalchemy import Integer, Enum, String
from sqlalchemy.sql.schema import Column, ForeignKey
from .database import Base
from .content_types import ContentTypes
from .content_schemas import ContentBase


class Content(Base):
    __tablename__ = 'content'

    blog_id = Column(Integer, ForeignKey("blog.id"), primary_key=True, autoincrement=False)
    position = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    value = Column(String, nullable=False)


def from_content_base(blog_id: int, content_base: ContentBase) -> Content:
    return Content(
        blog_id=blog_id,
        position=content_base.position,
        type=ContentTypes(content_base.type).value,
        value=content_base.value
    )

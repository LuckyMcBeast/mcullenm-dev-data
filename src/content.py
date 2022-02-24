from sqlalchemy import Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.sql.schema import Column, ForeignKey
from .database import Base
from pydantic import BaseModel
import enum


class Content(Base):
    __tablename__ = 'content'

    blog_id = Column(Integer, ForeignKey("blog.id"),
                     primary_key=True, autoincrement=False)
    position = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    value = Column(String, nullable=False)


class ContentBase(BaseModel):
    position: int
    type: str
    value: str


class ContentTypes(enum.Enum):
    paragraph = "p"


def from_content_base(blog_id: int, content_base: ContentBase) -> Content:
    return Content(
        blog_id=blog_id,
        position=content_base.position,
        type=ContentTypes(content_base.type).value,
        value=content_base.value
    )


def from_content(content: Content) -> ContentBase:
    return ContentBase(
        position=content.position,
        type=content.type,
        value=content.value
    )


def from_content_list(content_list: list[Content]) -> list[ContentBase]:
    content_base_list = []
    for content in content_list:
        content_base_list.append(from_content(content))
    return content_base_list


def commit_new_content(blog_id: int, content_base_list: list[ContentBase], db: Session) -> list[Content]:
    try:
        new_content = []
        for content_base in content_base_list:
            new_content.append(from_content_base(blog_id, content_base))
        for content in new_content:
            db.add(content)
        db.commit()
        return new_content
    except Exception as e:
        raise e


def commit_updated_content(blog_id: int, updated_content_list: list[ContentBase], db: Session) -> list[Content]:
    try:
        remove_content_by_blog_id(blog_id, db)
        return commit_new_content(blog_id, updated_content_list, db)
    except Exception as e:
        raise e


def retrieve_content_by_blog(blog, db):
    return db.query(Content).filter_by(blog_id=blog.id)


def remove_content_by_blog_id(blog_id, db):
    db.query(Content).filter_by(blog_id=blog_id).delete()

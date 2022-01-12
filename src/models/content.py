from sqlalchemy import Integer, Enum, String
from sqlalchemy.sql.schema import Column, ForeignKey
from ..database import base
from content_types import ContentTypes


class Content(base):
    __tablename__ = 'content'

    blog_id = Column(Integer, ForeignKey("blogs.id"), primary_key=True)
    position = Column(Integer, primary_key=True)
    type = Column(Enum(ContentTypes), nullable=False)
    value = Column(String, nullable=False)

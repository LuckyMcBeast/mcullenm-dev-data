from pydantic import BaseModel
from .content_schemas import ContentBase


class CreateBlogRequest(BaseModel):
    title: str
    content: list[ContentBase] = []

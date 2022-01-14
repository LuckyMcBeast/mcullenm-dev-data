from pydantic import BaseModel
from .content import ContentBase


class CreateBlogRequest(BaseModel):
    title: str
    content: list[ContentBase] = []




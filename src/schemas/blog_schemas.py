from pydantic import BaseModel


class CreateBlogRequest(BaseModel):
    title: str

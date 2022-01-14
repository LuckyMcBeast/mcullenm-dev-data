from pydantic import BaseModel
from .content import ContentBase
from .blog import Blog


class ViewModelResponse(BaseModel):
    blog_id: int
    title: str
    publish_date: str
    content: list[ContentBase]


def map_view_model_response(blog: Blog, blog_content: list[ContentBase]) -> ViewModelResponse:
    return ViewModelResponse(
        blog_id=blog.id,
        title=blog.title,
        publish_date=str(blog.publish_date),
        content=blog_content
    )

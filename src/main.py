from fastapi import FastAPI, Depends
from src.schemas.blog_schemas import CreateBlogRequest
from sqlalchemy.orm import Session
from .database import get_db
from .models.blog import Blog
from _datetime import datetime
from .models.content import Content
from .models.content_types import ContentTypes

app = FastAPI()


@app.post('/db-api/')
def create_blog(request: CreateBlogRequest, db: Session = Depends(get_db())):
    new_blog = Blog(
        title=request.title,
        publish_date=datetime.now()
    )

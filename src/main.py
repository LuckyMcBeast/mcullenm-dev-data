from fastapi import FastAPI, Depends
from .blog_schemas import CreateBlogRequest
from sqlalchemy.orm import Session
from .database import get_db
from .blog import Blog
from _datetime import datetime
from .content import Content, from_content_base
from .content_schemas import ContentBase
import logging

app = FastAPI()
logging.basicConfig(filename='error.log', level=logging.ERROR)


@app.post('/blog')
def create_blog(request: CreateBlogRequest, db: Session = Depends(get_db)):
    try:
        new_blog = commit_new_blog(db, request)
        new_content = commit_new_content(new_blog.id, request.content, db)
        return {
            "success": True,
            "created_id": new_blog.id,
            "content_amount": len(new_content)
        }
    except Exception as e:
        logging.error(e)
        return {
            "error": '{e}'.format(e=e)
        }


@app.get('/blog')
def get_blogs(db: Session = Depends(get_db)):
    try:
        return db.query(Blog).all()
    except Exception as e:
        logging.error(e)
        return {
            "error": '{e}'.format(e=e)
        }

# @app.get('/blog/view')
# def get_blogs_with_content(db: Session = Depends(get_db)):
#     try:
#         blogs : list[Blog] = db.query(Blog).all()
#         content : list[Content] = db.query(Content).all()
#
#         for blog in blogs:
#
#
#     except Exception as e:
#         logging.error(e)
#         return {
#             "error": '{e}'.format(e=e)
#         }

def commit_new_blog(db, request):
    try:
        new_blog = Blog(
            title=request.title,
            publish_date=datetime.now()
        )
        db.add(new_blog)
        db.commit()
        return new_blog
    except Exception as e:
        raise e


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

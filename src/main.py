from fastapi import FastAPI, Depends
from .request_schemas import CreateBlogRequest
from .response_schemas import ViewModelResponse, map_view_model_response
from sqlalchemy.orm import Session
from .database import get_db
from .blog import Blog, commit_new_blog, retrieve_blogs, retrieve_blog
from .content import ContentBase, from_content_list, commit_new_content, retrieve_content_by_blog
import logging


app = FastAPI()
logging.basicConfig(filename='error.log', level=logging.ERROR)
logging.basicConfig(filename='debug.log', level=logging.DEBUG)


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
            "success": False, 
            "error": '{e}'.format(e=e)
        }


@app.get('/blog')
def get_blogs(db: Session = Depends(get_db)):
    try:
        return retrieve_blogs(db)
    except Exception as e:
        logging.error(e)
        return {
            "error": '{e}'.format(e=e)
        }


@app.get('/blog/view', response_model=list[ViewModelResponse])
def get_blogs_with_content(db: Session = Depends(get_db)):
    view_model_response_list = []
    try:
        all_blogs: list[Blog] = retrieve_blogs(db)

        for blog in all_blogs:
            blog_content: list[ContentBase] = from_content_list(retrieve_content_by_blog(blog, db))
            view_model_response_list.append(map_view_model_response(blog, blog_content))
        return view_model_response_list

    except Exception as e:
        logging.error(e)
        return {
            "error": '{e}'.format(e=e)
        }


@app.get('/blog/{blog_id}')
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    try:
        return retrieve_blog(blog_id, db)

    except Exception as e:
        logging.error(e)
        return {
            "error": '{e}'.format(e=e)
        }


@app.get('/blog/{blog_id}/view', response_model=ViewModelResponse)
def get_blog_with_content(blog_id: int, db: Session = Depends(get_db)):
    try:
        blog: Blog = retrieve_blog(blog_id, db)
        blog_content: list[ContentBase] = from_content_list(retrieve_content_by_blog(blog, db))
        return map_view_model_response(blog, blog_content)

    except Exception as e:
        logging.error(e)
        return {
            "error": '{e}'.format(e=e)
        }


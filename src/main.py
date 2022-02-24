from fastapi import FastAPI, Depends, HTTPException
from .request_schemas import CreateBlogRequest
from .response_schemas import ViewModelResponse, map_view_model_response
from sqlalchemy.orm import Session
from .database import get_db
from .blog import Blog, commit_new_blog, retrieve_blogs, retrieve_blog, remove_blog, commit_new_blog_with_id, commit_updated_blog
from .content import ContentBase, Content, from_content_list, commit_new_content, retrieve_content_by_blog, remove_content_by_blog_id, commit_updated_content
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
            blog_content: list[ContentBase] = from_content_list(
                retrieve_content_by_blog(blog, db))
            view_model_response_list.append(
                map_view_model_response(blog, blog_content))
        return view_model_response_list

    except Exception as e:
        logging.error(e)
        return {
            "error": '{e}'.format(e=e)
        }


@app.get('/blog/{blog_id}')
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(blog_id, db)
    if(not isinstance(blog, Blog)):
        raise HTTPException(
            status_code=404, detail="Blog with ID of " + str(blog_id) + " Not Found")
    return retrieve_blog(blog_id, db)


@app.get('/blog/{blog_id}/view', response_model=ViewModelResponse)
def get_blog_with_content(blog_id: int, db: Session = Depends(get_db)):
    try:
        blog: Blog = retrieve_blog(blog_id, db)
        blog_content: list[ContentBase] = from_content_list(
            retrieve_content_by_blog(blog, db))
        return map_view_model_response(blog, blog_content)

    except Exception as e:
        logging.error(e)
        return {
            "error": '{e}'.format(e=e)
        }


@app.put('/blog/{blog_id}')
def update_blog(blog_id: int, request: CreateBlogRequest, db: Session = Depends(get_db)):
    try:
        get_blog = retrieve_blog(blog_id, db)
        if(not isinstance(get_blog, Blog)):
            new_blog = commit_new_blog_with_id(blog_id, db, request)
            new_content = commit_new_content(new_blog.id, request.content, db)
            return {
                "success": True,
                "created_id": new_blog.id,
                "content_amount": len(new_content)
            }

        updated_blog = commit_updated_blog(get_blog, request, db)
        get_content = retrieve_content_by_blog(get_blog, db)
        if(not isinstance(get_content[0], Content) or get_content.count() == 0):
            new_content = commit_new_content(
                updated_blog.id, request.content, db)
            return {
                "success": True,
                "created_id": updated_blog.id,
                "content_amount": len(new_content)
            }

        updated_content = commit_updated_content(
            updated_blog.id, request.content, db)
        return {
            "success": True,
            "created_id": updated_blog.id,
            "content_amount": len(updated_content)
        }

    except Exception as e:
        logging.error(e)
        return {
            "success": False,
            "error": '{e}'.format(e=e)
        }


@app.delete('/blog/{blog_id}')
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    try:
        remove_content_by_blog_id(blog_id, db)
        removed = remove_blog(blog_id, db)
        return {
            "blog_id": removed
        }

    except Exception as e:
        logging.error(e)
        return {
            "error": '{e}'.format(e=e)
        }

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql.schema import Column
from .database import Base
from _datetime import datetime


class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    publish_date = Column(DateTime, nullable=False)


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


def commit_new_blog_with_id(blog_id, db, request):
    try:
        new_blog = Blog(
            id=blog_id,
            title=request.title,
            publish_date=datetime.now()
        )
        db.add(new_blog)
        db.commit()
        return new_blog
    except Exception as e:
        raise e


def commit_updated_blog(blog, request, db):
    try:
        if(request.title == blog.title):
            return blog
        updated_blog = Blog(
            id=blog.id,
            title=request.title,
            publish_date=blog.publish_date
        )
        db.query(Blog).filter(Blog.id == updated_blog.id).update(
            {"title": (updated_blog.title)})
        db.commit()
        return updated_blog
    except Exception as e:
        raise e


def remove_blog(blog_id, db):
    try:
        db.query(Blog).filter(Blog.id == blog_id).delete()
        db.commit()
        return blog_id
    except Exception as e:
        raise e


def retrieve_blogs(db):
    return db.query(Blog).all()


def retrieve_blog(blog_id, db):
    return db.query(Blog).get(blog_id)

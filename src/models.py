from sqlalchemy import Integer, String
from sqlalchemy.sql.schema import Column
from .database import base

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer)
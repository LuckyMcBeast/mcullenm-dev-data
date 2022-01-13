from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql.schema import Column
from .database import Base


class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    publish_date = Column(DateTime, nullable=False)

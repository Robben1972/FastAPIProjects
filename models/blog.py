from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db import Base

class Blog(Base):
    __tablename__ = 'blog'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)
    author = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    comments = relationship('Comment', back_populates='blog')


class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(int, ForeignKey('blogs.id', on_delete='CASCADE'), nullable=False)
    author = Column(String(100), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    blog = relationship('Blog', back_populates='comments')

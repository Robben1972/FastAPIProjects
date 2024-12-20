from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Integer, func
from sqlalchemy.orm import relationship
from app.db import Base

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    comments = relationship('Comment', back_populates='blog', cascade='all, delete-orphan')

# Comment Model
class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(Integer, ForeignKey('blogs.id'), nullable=False)
    author = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    blog = relationship('Blog', back_populates='comments')

from pydantic import BaseModel

class BlogResponse(BaseModel):
    id : int
    title : str
    content : str
    author : str

    class Config:
        from_attributes = True

class BlogCreate(BaseModel):
    title : str
    content : str
    author : str

class CommentCreate(BaseModel):
    author : str
    content : str

class CommentResponse(BaseModel):
    id : int
    blog_id : int
    author : str
    content : str

from fastapi import APIRouter, Depends, HTTPException
from .schemas import BlogResponse, BlogCreate, CommentCreate, CommentResponse
from sqlalchemy.orm import Session
from app.db import get_db
from models.blog import Blog, Comment


router = APIRouter()

@router.get("/blogs/", response_model=list[BlogResponse])
async def blog(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    if not blogs:
        raise HTTPException(status_code=404, detail="No blogs found")
    return blogs

@router.post("/blogs/")
async def create_blog(blog: BlogCreate, db: Session = Depends(get_db)):
    try:
        db_item = Blog(**blog.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        raise HTTPException(status_code=500, message="Something went wrong")

@router.get("/blogs/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/blogs/{blog_id}")
async def update_blog(blog_id: int, blog: BlogCreate, db: Session = Depends(get_db)):
    blog_to_update = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog_to_update:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog_to_update.title = blog.title
    blog_to_update.content = blog.content

@router.delete("/blogs/{blog_id}")
async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog_to_delete = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog_to_delete:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog_to_delete)
    db.commit()
    return {"detail": "Blog deleted"}

@router.post("/blogs/{blog_id}/comments/")
async def create_comment(blog_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    try:
        db_item = Comment(**comment.dict())
        db_item.blog_id = blog_id
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        raise HTTPException(status_code=500, message="Something went wrong")
    
@router.get("/blogs/{blog_id}/comments/", response_model=list[CommentResponse])
async def get_comments(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    comments = db.query(Comment).filter(Comment.blog_id == blog_id).all()
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found")
    return comments
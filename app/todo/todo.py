from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from models.todo import Todo
from .schemas import TodoResponse, TodoCreate

router = APIRouter()

@router.get('/todolist/', response_model=list[TodoResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Todo).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks

@router.post('/todolist/')
def create_task(todo: TodoCreate, db: Session = Depends(get_db)):
    try:
        db_item = Todo(**todo.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail='Something went wrong')

@router.get('/todolist/{task_id}', response_model=TodoResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put('/todolist/{task_id}')
def update_task(task_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = todo.title
    task.description = todo.description
    task.done = todo.done
    db.commit()
    db.refresh(task)
    return task

@router.delete('/todolist/{task_id}')
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Todo).filter(Todo.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}
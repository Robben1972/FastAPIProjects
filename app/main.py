from fastapi import FastAPI
from app.todo import todo
from app.db import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todo.router)

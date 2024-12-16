from fastapi import FastAPI
from app.todo.todo import router
from app.db import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

from pydantic import BaseModel

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    done: bool

    class Config:
        from_attributes = True

class TodoCreate(BaseModel):
    title: str
    description: str
    done: bool = False
# Section 9: API Request Methods that uses Postgres Database and without Routers and without Authentication
from typing import Annotated, Optional

from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, Path, status
from models import Todos, Users
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

router = APIRouter()


# Section 9: API Request Methods - 111 Get all Todos from Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_todos(db: db_dependency):
    return db.query(Todos).all()


@router.get("/users", status_code=status.HTTP_200_OK)
async def read_users(db: db_dependency):
    return db.query(Users).all()


# Section 9: API Request Methods - 112 Get Todo by ID
@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    db: db_dependency, todo_id: int = Path(gt=0)
):  # We are validating the path parameter
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Todo not found")


# Section 9: API Request Methods - 113 Post Request
# Request Body Validation using Pydantic
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)  # Priority between 1 and 5
    complete: bool = Field(default=False)
    owner_id: Optional[int] = Field(
        default=None, gt=0
    )  # Owner ID is optional and must be > 0 if provided


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    db.add(Todos(**todo_request.dict()))
    db.commit()


# Section 9: API Request Methods - 114 Put Request
@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete

        db.add(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Todo ID not found")


# Section 9: API Request Methods - 115 Delete Request
@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model:
        db.delete(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Todo ID not found")

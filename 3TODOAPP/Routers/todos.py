# Section 11: Authenticate Requests
from typing import Annotated

from database import SessionLocal
from fastapi import APIRouter, Depends, HTTPException, Path, status
from models import Todos, Users
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .auth import get_current_user

router = APIRouter()


# Section 9: API Request Methods - 111 Get all Todos from Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[Users, Depends(get_current_user)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_todos(db: db_dependency):
    return db.query(Todos).all()


# Section 11: 131 Get All Todos (User ID)
@router.get("/users", status_code=status.HTTP_200_OK)
async def read_users(user: user_dependency, db: db_dependency):
    # We are trying to save a todo to our database through an API endpoint that requires the get_current user to be successful, which authenticates the user.
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(Users).all()


# Section 11: 132 Get Todo (ID + User ID)
@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):  # We are validating the path parameter
    # We are trying to save a todo to our database through an API endpoint that requires the get_current user to be successful, which authenticates the user.
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
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
    # owner_id: Optional[int] = Field(
    #     default=None, gt=0
    # )  # Owner ID is optional and must be > 0 if provided


# Section 11: 130 Post Todo (User ID)
@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency, db: db_dependency, todo_request: TodoRequest
):
    # We are trying to save a todo to our database through an API endpoint that requires the get_current user to be successful, which authenticates the user.
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    db.add(Todos(**todo_request.dict(), owner_id=user.get("id")))
    db.commit()


# Section 11: 133 Put Todo (User ID)
@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
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
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model:
        db.delete(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Todo ID not found")

from typing import Optional

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_year: int

    def __init__(self, id, title, author, description, rating, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year


# Pydantic Data Model for Data Validation
class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="ID is not needed on create", default=None
    )  # id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_year: int = Field(gt=1999, lt=2031)

    # Setting a default values using Model Config
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithsandeep",
                "description": "A new description of a book",
                "rating": 5,
                "published_year": 2025,
            }
        }
    }


books = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2030),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5, 2030),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5, 2029),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2028),
    Book(5, "HP2", "Author 2", "Book Description", 3, 2027),
    Book(6, "HP3", "Author 3", "Book Description", 1, 2026),
]


# GET Request
@app.get("/")
# async is not needed here, fastapi will automatically add an async before a function
async def home_page():
    return {"message": "Welcome to the Sandeep's Bookstore API"}


# Static Path Parameter
@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books():
    return books


# IMP: Always keep the static path parameter above the dynamic path parameter
# Query Parameter
@app.get("/books/pubyear", status_code=status.HTTP_200_OK)
async def read_by_year(pubyear: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in books:
        print(type(pubyear))
        if book.published_year == pubyear:
            books_to_return.append(book)
    return books_to_return


# Dynamic Path Parameter. Data Validation of Path.
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_by_bookid(book_id: int = Path(gt=0)):
    for book in books:
        if book.id == book_id:
            return book
    # return {"message": f"Book with ID {book_id} not found"}
    raise HTTPException(status_code=404, detail="Book not found")


# IMP: You can't have a same endpoint / address with same request type
# Query Parameter
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_by_rating(rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in books:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


# POST Request
# @app.post("/books/create_book") # When the Request is different, then the endpoint can be same. No need to have a different endpoint
@app.post("/books/", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    book_request.id = generate_book_id()
    new_book = Book(**book_request.model_dump())
    books.append(new_book)
    return {"message": "Book created successfully", "book": new_book}


def generate_book_id():
    book_id = 1 if len(books) == 0 else books[-1].id + 1
    return book_id


# PUT Request
# @app.put("/books/update_book") # When the Request is different, then the endpoint can be same. No need to have a different endpoint
@app.put("/books/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest):
    upd_book = Book(**book_request.model_dump())
    book_changed = False
    for i in range(len(books)):
        if books[i].id == upd_book.id:
            books[i] = upd_book
            book_changed = True
            # raise HTTPException(status_code=204, detail="Book updated successfully")
            return {"message": "Book updated successfully", "book": books[i]}
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


# DELETE Request - Query Parameter
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(books)):
        if books[i].id == book_id:
            books.pop(i)
            return {"message": f"Book with ID {book_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

from fastapi import Body, FastAPI

app = FastAPI()


books = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


# GET Request
@app.get("/")
# async is not needed here, fastapi will automatically add an async before a function
async def home_page():
    return {"message": "Welcome to the Sandeep's Bookstore API"}


# Static Path Parameter
@app.get("/books")
async def get_all_books():
    return books


# Order of Path Parameters is important
@app.get("/books/mybook")
async def my_book():
    return {"message": "Atomic Habits is my favorite book"}


# Query Parameter: Filter the data in the Path Parameter
@app.get("/books/")
async def get_book_by_category(category: str):
    books_to_return = []
    for book in books:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# Dynamic Path Parameter
@app.get("/books/{book_name}")
async def book_details(book_name: str):
    for book in books:
        if book.get("title").casefold() == book_name.casefold():
            return book
    else:
        return {"message": f"{book_name} book details not found"}


# IMPYou can't have two dynamic path parameters / endpoints with the same path (books)


# Dynamic Path and Query Parameter
@app.get("/books/{author}/")
async def get_book_by_author_category(author: str, category: str):
    books_to_return = []
    for book in books:
        if (
            book.get("author").casefold() == author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


# POST Request
# {"title": "Title Seven", "author": "Sandeep", "category": "Python"}
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    books.append(new_book)
    return {"message": "Book created successfully", "book": new_book}

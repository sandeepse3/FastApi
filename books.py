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
@app.get("/bookstore")
async def get_all_books():
    return books


# Order of Path Parameters is important
@app.get("/books/mybook")
async def my_book():
    return {"message": "Atomic Habits is my favorite book"}


# Query Parameter: Filter the data in the Path Parameter
@app.get("/books")
async def get_book_details(
    book_title: str,
):  # book_title is a query parameter for the path /books
    for book in books:
        if book.get("title").casefold() == book_title.casefold():
            return book
    else:
        return {"message": f"{book_title} book details not found"}


# IMP:  **Endpoint Overlap:**  The `/books/{category}` endpoint could potentially catch `/books/authorcat` if not defined above it. So you should be defining here not below '/books/{category}'. Or if you want to define it below `/books/{category}`, you need to add a trailing slash `/` to the `/books/authorcat` endpoint to avoid overlap i.e. `/books/{category}`. Note that this rule is applicable to other CRUD operations as well not just GET requests.
# Using Query Parameters
@app.get("/books/authorcat")
async def get_book_by_author_category(author: str, category: str):
    books_to_return = []
    for book in books:
        if (
            book.get("author").casefold() == author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


# Dynamic Path Parameter
@app.get("/books/{category}")
# IMP: One thing that we need to note is that the API endpoint dynamic param (category) that's in curly brackets above needs to match the naming convention that we have as our parameter in our book_by_category function.
async def book_by_category(category: str):  # category is a dynamic path parameter
    books_to_return = []
    for book in books:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# Using Query Parameters
# It will not work if you are not adding `/` after `/books/byauthor` due to the endpoint overlap with `/books/{category}`, if you want to make it work just with `/books/byauthor` you just need to add it above `/books/{category}` endpoint. Note that this rule is applicable to other CRUD operations as well not just GET requests.
@app.get("/books/byauthor/")
async def books_by_author(author: str):
    books_to_return = []
    for book in books:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return


# IMP: You can't have two dynamic path parameters or endpoints with the same path (/books). Below will not work. Note that this rule is applicable to other CRUD operations as well not just GET requests.
# Dynamic Path Parameter
# @app.get("/books/{author}")
# async def books_by_author(author: str):
#     books_to_return = []
#     for book in books:
#         if book.get("author").casefold() == author.casefold():
#             books_to_return.append(book)
#     return books_to_return


# Using Dynamic Path Parameters
# @app.get("/books/byauthor/{author}")
# async def books_by_author(author: str):
#     books_to_return = []
#     for book in books:
#         if book.get("author").casefold() == author.casefold():
#             books_to_return.append(book)
#     return books_to_return


# POST Request
# {"title": "Title Seven", "author": "Sandeep", "category": "Python"}
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    books.append(new_book)
    return {"message": "Book created successfully", "book": new_book}


# PUT Request
# {"title": "Title Seven", "author": "Sandeep", "category": "Advanced Python"}
@app.put("/books/update_book")
async def update_book(new_book=Body()):
    for index in range(len(books)):
        if books[index].get("title").casefold() == new_book.get("title").casefold():
            books[index] = new_book
            return {"message": "Book updated successfully"}
    else:
        return {"message": "Book not found for update"}


# DELETE Request
# {"title": "Title Seven"}
@app.delete("/books/delete_book")
async def delete_book(new_book=Body()):
    for index, book in enumerate(books):
        if book.get("title").casefold() == new_book.get("title").casefold():
            del books[index]
            return {"message": "Book deleted successfully"}
    else:
        return {"message": "Book not found for deletion"}

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from models import Book, BookResponse
from starlette.responses import JSONResponse

app = FastAPI()
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "Oops! Something went wrong"
        },
    )
@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {
        "book_id": book_id,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald"
    }


#Here, the -> list[BookResponse] function type hint tells FastAPI 
# to use the BookResponse model for responses, ensuring that only 
# the title and author fields are included in the response JSON. 
# Alternatively, you can specify the response type in the endpoint 
# decorator’s arguments as follows:
# @app.get("/allbooks", response_model= list[BookResponse])
# async def read_all_books() -> Any:

@app.get("/allbooks")
async def read_all_books() -> list[BookResponse]:
    return [
        {
            "id": 1,
            "title": "1984",
            "author": "George Orwell"},
        {
            "id": 1,
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
        },
    ]

@app.get("/allbooks2", response_model= list[BookResponse])
async def read_all_books2() -> list[BookResponse]:
    return [
        {
            "id": 1,
            "title": "1984",
            "author": "George Orwell"},
        {
            "id": 1,
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
        },
    ]

@app.get("/books")
async def read_books(year: int = None):
    if year:
        return {
            "year": year,
            "books": ["Book 1", "Book 2"]
        }
    return {"books": ["All Books"]}


@app.post("/book")
async def create_book(book: Book):
    return book

@app.get("/error_endpoint")
async def raise_exception():
    raise HTTPException(status_code=400)
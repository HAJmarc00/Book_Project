from typing import Optional

from fastapi import FastAPI, Path, Query , HTTPException
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


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create! ',default=None)
    title: str = Field(min_length=1 , max_length=15)
    author: str = Field(min_length=1 , max_length=15)
    description: str = Field(min_length=1 , max_length=80)
    rating: int = Field(gt=0 , lt=11)
    published_year : int = Field(gt=999 , lt=3000)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title" : "A new book",
                "author" : "Who read this Book?",
                "description" : "Tell me about Book!",
                "rating" : 5,
                "Date": 1999,
            }
        }
    }


BOOKS = [
    Book(1, "HP1", "Jhon", "None", 5, 2020),
    Book(2, "PHP", "Morde", "None", 6, 2019),
    Book(3, "Django", "Ekko", "None", 10, 1993),
    Book(4, "python", "Miss Fortune", "None", 7, 2016),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Item not found")



@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_book_by_rating(book_rating: int = Query(gt=0, lt=11)):
    book_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            book_to_return.append(book)
            return book_to_return

    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def get_book_by_published_year(published_year: int = Path(gt=400)):
    book_to_return = []
    for book in BOOKS:
        if book.published_year == published_year:
            book_to_return.append(book)
            return book_to_return

    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request : BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book, BOOKS


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book : BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")
    return book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id : int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            deleted_book = BOOKS.pop(i)
            return {
                "SUCCESS, the book got deleted! |",
                deleted_book
            }
    raise HTTPException(status_code=404, detail="Item not found",)


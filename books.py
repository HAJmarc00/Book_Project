from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Django', 'author': 'Sadegh', 'category': 'science'},
    {'title': 'Python', 'author': 'amin', 'category': 'programming'},
    {'title': 'PHP', 'author': 'Abdul', 'category': 'math'},
]

@app.get("/books")
async def read_all_books():
    return BOOKS


# Path Parameter
#http://127.0.0.1:8000/books/Title Two
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return book
        else :
            return "Book not found"

# Query Parameter
#http://127.0.0.1:8000/books/?category=Category%20Three
@app.get("/books/")
async def read_category_by_query(category : str):
    book_to_return = []
    for book in BOOKS:
        if book['category'].casefold() == category.casefold():
            book_to_return.append(book)
    return book_to_return


#http://127.0.0.1:8000/books/byauthor/?author=author%20two
@app.get('/books/byauthor/{author}')
async def read_books_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book['author'].casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return


# book auther (Path Parameter) / category (Query Parameter)
#http://127.0.0.1:8000/books/sadegh/?category=science
@app.get('/books/{book_author}/')
async def read_auther_category_by_query(book_author: str, category : str):
    book_to_return = []
    for book in BOOKS:
        if book.get('author', '').casefold() == book_author.casefold() and \
                book.get('category', '').casefold() == category.casefold():
            book_to_return.append(book)

    return book_to_return


#http://127.0.0.1:8000/books/create_book
@app.post('/books/create_book/')
async def create_book(new_book = Body()):
    BOOKS.append(new_book)


#http://127.0.0.1:8000/books/update_book
@app.put('/books/update_book/')
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title', '').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

    return updated_book


#http://127.0.0.1:8000/books/delete_book{book_title}
@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title : str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title', '').casefold() == book_title.casefold():
            BOOKS[i].pop(i)
            break


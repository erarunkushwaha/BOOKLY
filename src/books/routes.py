from fastapi import APIRouter,status
from src.books.book_data import books
from src.books.schemas import Book,BookUpdateModal
from typing import List
from fastapi.exceptions import HTTPException

book_router = APIRouter()

#pip freeze > requirements.txt

@book_router.get("/", response_model=List[Book])
async def get_all_books():
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_a_book(book: Book) -> dict:
    new_book = book.model_dump()
    books.append(new_book)
    return new_book


@book_router.get("/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")


@book_router.put("/{book_id}")
async def update_book(book_id: int, book_update_data: BookUpdateModal) -> dict:
    for book in books:
        if book["id"] == book_id:
            update_data = book_update_data.model_dump(exclude_unset=True)
            book.update(update_data)
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")


@book_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
    # """
    # This function deletes a book from a list of books based on the provided book_id.
    
    # :param book_id: The `book_id` parameter in the code snippet represents the unique identifier of the
    # book that is being requested for deletion. This identifier is used to locate the specific book
    # within the list of books and remove it from the collection
    # :type book_id: int
    # :return: An empty dictionary {} is being returned when a book with the specified book_id is found
    # and successfully deleted from the list of books. If the book with the specified book_id is not found
    # in the list, an HTTP 404 Not Found error is raised with the detail message "book not found".
    # """
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")

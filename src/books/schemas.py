from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str
    publication: str
    price: float


class BookUpdateModal(BaseModel):
    title: str
    author: str
    publication: str
    price: float
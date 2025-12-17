from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import date, datetime
from typing import Optional, List
import re

class AuthorBase(BaseModel):
    firstname: str
    lastname: str
    birth_date: date
    nationality: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    isbn: str
    publication_year: int
    author_id: int
    total_copies: int
    available_copies: int
    category: str
    language: str
    pages: int
    publisher: str

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v):
        clean = v.replace("-", "").replace(" ", "")
        if len(clean) != 13 or not clean.isdigit():
            raise ValueError("L'ISBN-13 doit comporter 13 chiffres")
        return clean

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        from_attributes = True

class LoanCreate(BaseModel):
    book_id: int
    borrower_name: str
    borrower_email: EmailStr
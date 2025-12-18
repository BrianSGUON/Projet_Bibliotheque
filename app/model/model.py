from enum import Enum
from typing import Optional, List
from datetime import date, datetime
from sqlmodel import Field, Relationship, SQLModel

# --- ÉNUMÉRATIONS ---

class BookCategory(str, Enum):
    FICTION = "Fiction"
    SCIENCE = "Science"
    HISTOIRE = "Histoire"
    PHILOSOPHIE = "Philosophie"
    BIOGRAPHIE = "Biographie"
    POESIE = "Poésie"
    THEATRE = "Théâtre"
    JEUNESSE = "Jeunesse"
    BD = "BD"
    AUTRE = "Autre"

class LoanStatus(str, Enum):
    ACTIF = "actif"
    RETOURNE = "retourné"
    RETARD = "en retard"

# --- MODÈLES AUTEUR ---

class Author(SQLModel, table=True):
    __tablename__ = "authors"
    id: Optional[int] = Field(default=None, primary_key=True)
    firstname: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    birth_date: date = Field(nullable=False)
    nationality: str = Field(max_length=3)
    
    books: List["Book"] = Relationship(back_populates="author")

# --- MODÈLES LIVRE ---

class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    isbn: str = Field(unique=True, index=True, max_length=17) 
    publication_year: int
    author_id: int = Field(foreign_key="authors.id", index=True)
    available_copies: int = Field(default=0, ge=0)
    total_copies: int = Field(gt=0)
    category: BookCategory = Field(default=BookCategory.AUTRE)
    language: str = Field(max_length=2)
    pages: int = Field(gt=0)
    publisher: str

    author: Author = Relationship(back_populates="books")
    loans: List["Loan"] = Relationship(back_populates="book")

# --- MODÈLES LOAN ---

class Loan(SQLModel, table=True):
    __tablename__ = "loans"
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="books.id")
    borrower_name: str
    borrower_email: str
    loan_date: datetime = Field(default_factory=datetime.now)
    return_deadline: datetime
    actual_return_date: Optional[datetime] = Field(default=None)
    status: LoanStatus = Field(default=LoanStatus.ACTIF)

    book: Book = Relationship(back_populates="loans")
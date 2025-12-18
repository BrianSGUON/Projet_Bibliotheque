from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

# --- ÉNUMÉRATIONS (Redéfinies ici pour éviter l'import circulaire avec model.py) ---

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

# --- SCHÉMAS POUR LES AUTEURS ---

class AuthorBase(BaseModel):
    firstname: str
    lastname: str
    birth_date: date
    nationality: str

class AuthorCreate(AuthorBase):
    """Utilisé pour le POST"""
    pass

class AuthorRead(AuthorBase):
    id: int
    class Config:
        from_attributes = True

# --- SCHÉMAS POUR LES LIVRES ---

class BookBase(BaseModel):
    title: str
    isbn: str
    publication_year: int
    author_id: int
    total_copies: int
    available_copies: int
    category: BookCategory
    language: str
    pages: int
    publisher: str

    @field_validator('isbn')
    @classmethod
    def validate_isbn(cls, v: str) -> str:
        clean = v.replace("-", "").replace(" ", "")
        if len(clean) != 13 or not clean.isdigit():
            raise ValueError("L'ISBN-13 doit comporter 13 chiffres")
        return clean

    @field_validator('language')
    @classmethod
    def validate_iso_lang(cls, v: str) -> str:
        if len(v) != 2 or not v.isalpha():
            raise ValueError("La langue doit être un code ISO de 2 lettres (ex: fr, en)")
        return v.lower()

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    available_copies: Optional[int] = None
    total_copies: Optional[int] = None
    category: Optional[BookCategory] = None

class BookRead(BookBase):
    id: int
    class Config:
        from_attributes = True

# --- SCHÉMAS POUR LES EMPRUNTS (LOANS) ---

class LoanCreate(BaseModel):
    book_id: int
    borrower_name: str
    borrower_email: EmailStr

class LoanRead(BaseModel):
    id: int
    book_id: int
    borrower_name: str
    borrower_email: EmailStr
    loan_date: datetime
    return_deadline: datetime
    actual_return_date: Optional[datetime] = None
    status: LoanStatus

    class Config:
        from_attributes = True
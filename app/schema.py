from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import date, datetime
from typing import Optional, List
from enum import Enum
import re

# --- ENUMÉRATIONS ---
class CategoryEnum(str, Enum):
    Fiction = "Fiction"
    Science = "Science"
    Histoire = "Histoire"
    Philosophie = "Philosophie"
    Autre = "Autre"

class LoanStatus(str, Enum):
    ACTIF = "actif"
    RETOURNE = "retourné"
    RETARD = "en retard"

# --- SCHÉMAS AUTEUR ---
class AuthorBase(BaseModel):
    firstname: str
    lastname: str
    birth_date: date
    nationality: str = Field(..., min_length=2, max_length=3, description="Code pays ISO")
    biography: Optional[str] = None
    death_date: Optional[date] = None
    website: Optional[str] = None

    @field_validator('birth_date')
    @classmethod
    def birth_date_not_future(cls, v):
        if v > date.today():
            raise ValueError("La date de naissance ne peut pas être dans le futur")
        return v

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    class Config:
        from_attributes = True

# --- SCHÉMAS LIVRE ---
class BookBase(BaseModel):
    title: str
    isbn: str
    publication_year: int = Field(..., ge=1450, le=datetime.now().year)
    author_id: int
    total_copies: int = Field(..., gt=0)
    available_copies: int = Field(..., ge=0)
    description: Optional[str] = None
    category: CategoryEnum
    language: str
    pages: int = Field(..., gt=0)
    publisher: str

    @field_validator('isbn')
    @classmethod
    def validate_isbn_13(cls, v):
        # Nettoyage : enlever tirets et espaces
        clean_isbn = v.replace("-", "").replace(" ", "")
        
        if not re.match(r"^\d{13}$", clean_isbn):
            raise ValueError("L'ISBN-13 doit contenir exactement 13 chiffres")
        
        # Validation du Checksum ISBN-13
        digits = [int(d) for d in clean_isbn]
        total = sum(digits[i] * (3 if i % 2 else 1) for i in range(12))
        check_digit = (10 - (total % 10)) % 10
        
        if digits[12] != check_digit:
            raise ValueError("Somme de contrôle (checksum) ISBN invalide")
        return clean_isbn

    @field_validator('available_copies')
    @classmethod
    def check_copies_consistency(cls, v, info):
        if 'total_copies' in info.data and v > info.data['total_copies']:
            raise ValueError("Les exemplaires disponibles ne peuvent pas dépasser le total")
        return v

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        from_attributes = True

# --- SCHÉMAS EMPRUNT ---
class LoanBase(BaseModel):
    book_id: int
    borrower_name: str
    borrower_email: EmailStr
    card_number: str
    notes: Optional[str] = None

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    loan_date: datetime
    return_deadline: datetime
    actual_return_date: Optional[datetime] = None
    status: LoanStatus

    class Config:
        from_attributes = True
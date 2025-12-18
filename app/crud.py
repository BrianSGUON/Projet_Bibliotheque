from sqlmodel import Session, select 
from typing import List, Optional
from app.model.model import Author, Book, Loan, LoanStatus
from app.schema import AuthorCreate, BookCreate

# --- AUTEURS ---

def get_author_by_name(db: Session, firstname: str, lastname: str) -> Optional[Author]:
    statement = select(Author).where(Author.firstname == firstname, Author.lastname == lastname)
    return db.exec(statement).first()

def create_author(db: Session, author: AuthorCreate) -> Author:
    """Crée un nouvel auteur en base de données."""
    db_author = Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(db: Session, skip: int = 0, limit: int = 10) -> List[Author]:
    """Récupère la liste des auteurs avec pagination."""
    statement = select(Author).offset(skip).limit(limit)
    return db.exec(statement).all()

# --- LIVRES ---

def get_book_by_isbn(db: Session, isbn: str) -> Optional[Book]:
    statement = select(Book).where(Book.isbn == isbn)
    return db.exec(statement).first()

def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.get(Book, book_id)

def create_book(db: Session, book: BookCreate) -> Book:
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 10) -> List[Book]:
    statement = select(Book).offset(skip).limit(limit)
    return db.exec(statement).all()

# --- EMPRUNTS ---

def get_active_loans_count(db: Session, email: str) -> int:
    statement = select(Loan).where(Loan.borrower_email == email, Loan.status == LoanStatus.ACTIF)
    results = db.exec(statement).all()
    return len(results)

def create_loan_entry(db: Session, db_loan: Loan) -> Loan:
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def get_loan_by_id(db: Session, loan_id: int) -> Optional[Loan]:
    return db.get(Loan, loan_id)
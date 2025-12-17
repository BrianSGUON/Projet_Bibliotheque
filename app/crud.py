from sqlalchemy.orm import Session
from . import model, schema

# --- OPÉRATIONS SUR LES AUTEURS ---

def get_author_by_name(db: Session, firstname: str, lastname: str):
    """Récupère un auteur par son nom complet pour vérifier l'unicité."""
    return db.query(model.Author).filter(
        model.Author.firstname == firstname,
        model.Author.lastname == lastname
    ).first()

def create_author(db: Session, author: schema.AuthorCreate):
    """Crée un nouvel auteur en base de données."""
    db_author = model.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(db: Session, skip: int = 0, limit: int = 10):
    """Liste les auteurs avec pagination."""
    return db.query(model.Author).offset(skip).limit(limit).all()


# --- OPÉRATIONS SUR LES LIVRES ---

def get_book_by_isbn(db: Session, isbn: str):
    """Vérifie si un ISBN existe déjà."""
    return db.query(model.Book).filter(model.Book.isbn == isbn).first()

def get_book(db: Session, book_id: int):
    """Récupère un livre par son ID (utilisé pour les emprunts et les détails)."""
    return db.query(model.Book).filter(model.Book.id == book_id).first()

def create_book(db: Session, book: schema.BookCreate):
    """Ajoute un livre au catalogue."""
    db_book = model.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 10):
    """Liste les livres avec pagination."""
    return db.query(model.Book).offset(skip).limit(limit).all()


# --- OPÉRATIONS SUR LES EMPRUNTS (LOANS) ---

def get_active_loans_count(db: Session, email: str):
    """Compte les emprunts 'actifs' d'un usager pour la limite de 5 livres."""
    return db.query(model.Loan).filter(
        model.Loan.borrower_email == email,
        model.Loan.status == model.LoanStatus.ACTIF
    ).count()

def create_loan_entry(db: Session, db_loan: model.Loan):
    """Enregistre techniquement l'objet Loan dans la base."""
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan

def get_loan_by_id(db: Session, loan_id: int):
    """Trouve un emprunt pour effectuer un retour."""
    return db.query(model.Loan).filter(model.Loan.id == loan_id).first()
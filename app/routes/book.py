from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import model, schema, database 

router = APIRouter(prefix="/books", tags=["Books"])

# Dépendance pour obtenir la session de base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schema.Book)
def create_book(book: schema.BookCreate, db: Session = Depends(get_db)):
    """
    Créer un nouveau livre dans le catalogue après validation de l'ISBN
    et de l'existence de l'auteur.
    """
    # 1. Vérification de l'unicité de l'ISBN 
    db_book = db.query(model.Book).filter(model.Book.isbn == book.isbn).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Un livre avec cet ISBN existe déjà")
    
    # 2. Vérification de l'existence de l'auteur référencé 
    db_author = db.query(model.Author).filter(model.Author.id == book.author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Auteur non trouvé")

    # 3. Création de l'entrée en base de données
    new_book = model.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/", response_model=List[schema.Book])
def list_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Récupérer la liste complète des livres avec pagination.
    """
    books = db.query(model.Book).offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=schema.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Récupérer les informations complètes d'un livre spécifique.
    """
    db_book = db.query(model.Book).filter(model.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Le livre n'existe pas")
    return db_book
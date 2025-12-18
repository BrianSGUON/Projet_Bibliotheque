from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schema, crud
from app.core.database import get_db
from app.schema import BookRead, BookCreate, BookUpdate

router = APIRouter(prefix="/Livres", tags=["Livres"])

@router.post("/", response_model=BookRead)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Pour ajouter un nouveau livre.
    Vérifie si l'ISBN existe déjà.
    """
    db_book = crud.get_book_by_isbn(db, isbn=book.isbn)
    if db_book:
        raise HTTPException(status_code=400, detail="Un livre avec cet ISBN existe déjà")
    
    return crud.create_book(db=db, book=book)

@router.get("/", response_model=List[BookRead])
def read_books(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    Récupérer la liste des livres (avec pagination).
    """
    return crud.get_books(db, skip=skip, limit=limit)

@router.get("/{book_id}", response_model=BookRead)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Récupérer les détails d'un livre spécifique par son ID.
    """
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return db_book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un livre de la base 
    """
    db_book = crud.get_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    
    db.delete(db_book)
    db.commit()
    return {"message": f"Le livre {book_id} a été supprimé avec succès"}
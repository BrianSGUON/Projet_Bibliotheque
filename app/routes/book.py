from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schema, database

router = APIRouter(prefix="/books", tags=["Books"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schema.Book)
def create_book(book: schema.BookCreate, db: Session = Depends(get_db)):
    # Vérification via le CRUD
    if crud.get_book_by_isbn(db, isbn=book.isbn):
        raise HTTPException(status_code=400, detail="ISBN déjà utilisé")
    
    return crud.create_book(db=db, book=book)

@router.get("/", response_model=List[schema.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)
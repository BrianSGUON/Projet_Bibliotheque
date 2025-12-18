from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud
from app.core.database import get_db
from app.schema import AuthorRead, AuthorCreate, BookCreate

router = APIRouter(prefix="/auteur", tags=["Auteurs"])

@router.post("/", response_model=AuthorRead)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, author.firstname, author.lastname)
    if db_author:
        raise HTTPException(status_code=400, detail="Cet auteur existe déjà")
    
    return crud.create_author(db=db, author=author)

@router.get("/", response_model=List[AuthorRead])
def list_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_authors(db, skip=skip, limit=limit)
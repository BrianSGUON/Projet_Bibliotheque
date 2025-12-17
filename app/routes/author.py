from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schema, database # Import de crud

router = APIRouter(prefix="/authors", tags=["Authors"])

# Dépendance pour injecter la session de base de données dans les fonctions
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schema.Author)
def create_author(author: schema.AuthorCreate, db: Session = Depends(get_db)):
    # Utilisation du CRUD pour vérifier l'existence
    db_author = crud.get_author_by_name(db, author.firstname, author.lastname)
    if db_author:
        raise HTTPException(status_code=400, detail="Cet auteur existe déjà")
    
    # Utilisation du CRUD pour la création
    return crud.create_author(db=db, author=author)

@router.get("/", response_model=list[schema.Author])
def list_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Utilisation du CRUD pour le listing
    return crud.get_authors(db, skip=skip, limit=limit)
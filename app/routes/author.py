from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import model, schema, database # 2 point pour remonter au fichier parent

router = APIRouter(prefix="/authors", tags=["Authors"])

# Fonction pour récupérer la session de base de données
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schema.Author)
def create_author(author: schema.AuthorCreate, db: Session = Depends(get_db)):
    # Vérification de la contrainte métier : le nom complet doit être unique 
    db_author = db.query(model.Author).filter(
        model.Author.firstname == author.firstname,
        model.Author.lastname == author.lastname
    ).first()
    
    if db_author:
        raise HTTPException(status_code=400, detail="Cet auteur existe déjà")
    
    # Création de l'auteur selon les attributs requis 
    new_author = model.Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author

@router.get("/", response_model=list[schema.Author])
def list_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # Récupération de la liste complète avec pagination 
    return db.query(model.Author).offset(skip).limit(limit).all()
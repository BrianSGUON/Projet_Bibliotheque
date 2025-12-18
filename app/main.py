from fastapi import FastAPI
from sqlmodel import SQLModel
from app.core.database import engine
from app.model.model import Book, Author, Loan 
from app.routes import author, book, loan
from app.core.database import create_db_and_tables

# Création des tables au démarrage de l'application
def create_db_and_tables():
    # SQLModel utilise les métadonnées de tous les modèles importés ci-dessus
    SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Bibliotheque API",
    description="API de gestion de bibliothèque utilisant SQLModel et fastapi",
    version="1.0.0"
)

# Exécuter la création des tables au lancement du serveur
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Montage des routeurs avec imports absolus
app.include_router(author.router)
app.include_router(book.router)
app.include_router(loan.router)

@app.get("/")
def home():
    return {
        "status": "online",
        "message": "Bienvenue sur l'API de la bibliothèque",
        "docs": "/docs"
    }
from fastapi import FastAPI
from . import model, database
from app.routes import author, book, loan

# Création des tables
model.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Bibliotheque API")

# Montage des routes
app.include_router(author.router)
app.include_router(book.router)
app.include_router(loan.router)

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de la bibliothèque"}
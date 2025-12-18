from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.model.model import Loan, LoanStatus, Book
from app.schema import LoanCreate
from app import crud

def create_loan(db: Session, loan_data: LoanCreate):
    """
    Logique pour créer un emprunt :
    1. Vérifier la disponibilité du livre.
    2. Vérifier le quota de l'emprunteur (max 5).
    3. Calculer les dates et décrémenter le stock.
    """
    # 1. Vérifier si le livre existe et est en stock
    book = crud.get_book(db, loan_data.book_id)
    if not book or book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Livre non disponible ou épuisé")

    # 2. Règle des 5 livres max par personne
    count = crud.get_active_loans_count(db, loan_data.borrower_email)
    if count >= 5:
        raise HTTPException(status_code=400, detail="Limite de 5 livres atteinte pour cet emprunteur")

    # 3. Préparation de l'objet Loan (J+14 pour le retour)
    now = datetime.now()
    db_loan = Loan(
        **loan_data.model_dump(),
        loan_date=now,
        return_deadline=now + timedelta(days=14),
        status=LoanStatus.ACTIF
    )

    # 4. Mise à jour du stock (-1)
    book.available_copies -= 1
    
    # On sauvegarde l'emprunt et la mise à jour du livre via le CRUD
    return crud.create_loan_entry(db, db_loan)

def process_return(db: Session, loan_id: int):
    """
    Logique pour traiter un retour :
    1. Valider l'emprunt.
    2. Marquer comme retourné ou en retard.
    3. Réincrémenter le stock (+1).
    """
    loan = crud.get_loan_by_id(db, loan_id)
    if not loan or loan.status != LoanStatus.ACTIF:
        raise HTTPException(status_code=404, detail="Emprunt actif non trouvé")

    # Mise à jour des dates
    loan.actual_return_date = datetime.now()
    
    # Détermination du statut (Retourné vs Retard)
    if loan.actual_return_date <= loan.return_deadline:
        loan.status = LoanStatus.RETOURNE
    else:
        loan.status = LoanStatus.RETARD

    # Remise en stock (+1)
    book = crud.get_book(db, loan.book_id)
    if book:
        book.available_copies += 1

    db.commit()
    db.refresh(loan)
    return loan
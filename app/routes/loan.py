from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlmodel import select
from app import schema
from app.model.model import Loan, LoanStatus
from app.core.database import get_db
from app.service import service
from datetime import datetime, date

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/", response_model=schema.LoanRead)
def create_new_loan(loan: schema.LoanCreate, db: Session = Depends(get_db)):
    """
    Enregistrer un nouvel emprunt dans le système.
    Cette route délègue la logique au 'service' pour :
    1. Vérifier la disponibilité du livre.
    2. Vérifier que l'usager n'a pas dépassé son quota de 3 ou 5 livres.
    3. Calculer automatiquement la date de retour (J+14).
    """
    # On appelle le service qui contient la logique métier complexe
    return service.create_loan(db=db, loan_data=loan)

@router.patch("/{loan_id}/return", response_model=schema.LoanRead)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    """
    Marquer un livre comme retourné .
    Le service va gérer la date de retour, le statut et la remise en stock (+1).
    """
    return service.process_return(db=db, loan_id=loan_id)

@router.get("/active", response_model=List[schema.LoanRead])
def list_active_loans(db: Session = Depends(get_db)):
    """
    Récupérer la liste de tous les emprunts qui n'ont pas encore été retournés.
    """
    statement = select(Loan).where(Loan.status == LoanStatus.ACTIF)
    results = db.exec(statement).all()
    return results

@router.get("/late", response_model=List[schema.LoanRead])
def list_late_loans(db: Session = Depends(get_db)):
    """
    Lister spécifiquement les emprunts dont la date limite est dépassée.
    """
    statement = select(Loan).where(Loan.status == LoanStatus.RETARD)
    results = db.exec(statement).all()
    return results

@router.patch("/{loan_id}/force-overdue")
def force_overdue(loan_id: int, db: Session = Depends(get_db)):
    loan = db.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Emprunt non trouvé")
    # On force une date passée
    loan.return_deadline = datetime(2024, 1, 1)
    db.add(loan)
    db.commit()
    return {"message": "L'emprunt est maintenant officiellement en retard !"}
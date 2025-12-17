from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException
from . import model, schema

def create_loan(db: Session, loan_data: schema.LoanCreate):
    """
    Logique métier pour la création d'un emprunt.
    Vérifie la disponibilité du livre et la limite d'emprunts par usager.
    """
    # 1. Vérifier si le livre existe et s'il reste des exemplaires 
    book = db.query(model.Book).filter(model.Book.id == loan_data.book_id).first()
    if not book or book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Livre non disponible")

    # 2. Vérifier la limite de 5 livres par usager 
    active_loans_count = db.query(model.Loan).filter(
        model.Loan.borrower_email == loan_data.borrower_email,
        model.Loan.status == model.LoanStatus.ACTIF
    ).count()
    
    if active_loans_count >= 5:
        raise HTTPException(status_code=400, detail="Limite de 5 emprunts atteinte")

    # 3. Calculer la date de retour automatique (+14 jours)
    loan_date = datetime.now()
    return_deadline = loan_date + timedelta(days=14)

    # 4. Créer l'emprunt et décrémenter le stock 
    new_loan = model.Loan(
        **loan_data.model_dump(),
        loan_date=loan_date,
        return_deadline=return_deadline,
        status=model.LoanStatus.ACTIF
    )
    
    # Mise à jour du stock disponible 
    book.available_copies -= 1 
    
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan
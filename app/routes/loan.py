from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schema, database, service

router = APIRouter(prefix="/loans", tags=["Loans"])

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/")
def create_loan(loan: schema.LoanCreate, db: Session = Depends(get_db)):
    return service.create_loan(db, loan)
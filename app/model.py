from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum, Text, UniqueConstraint
from sqlalchemy.orm import relationship
import enum
from database import Base

class CategoryEnum(enum.Enum):
    Fiction = "Fiction"
    Science = "Science"
    Histoire = "Histoire"
    Philosophie = "Philosophie"
    Autre = "Autre"

class LoanStatus(enum.Enum):
    ACTIF = "actif"
    RETOURNE = "retourné"
    RETARD = "en retard"

class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    nationality = Column(String(3), nullable=False)
    biography = Column(Text, nullable=True)
    death_date = Column(Date, nullable=True)
    website = Column(String, nullable=True)

    __table_args__ = (UniqueConstraint('firstname', 'lastname', name='_author_full_name_uc'),)
    
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    isbn = Column(String(13), unique=True, index=True, nullable=False)
    publication_year = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    
    available_copies = Column(Integer, default=1)
    total_copies = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(Enum(CategoryEnum), nullable=False)
    language = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    publisher = Column(String, nullable=False)

    author = relationship("Author", back_populates="books")
    loans = relationship("Loan", back_populates="book")

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_name = Column(String, nullable=False)
    borrower_email = Column(String, nullable=False)
    card_number = Column(String, nullable=False)
    
    loan_date = Column(DateTime, nullable=False)
    return_deadline = Column(DateTime, nullable=False)
    actual_return_date = Column(DateTime, nullable=True)
    status = Column(Enum(LoanStatus), default=LoanStatus.ACTIF)
    notes = Column(Text, nullable=True)

    book = relationship("Book", back_populates="loans")

class LoanHistory(Base):
    __tablename__ = "loan_history"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    total_loans = Column(Integer, default=0)
    average_duration = Column(Integer, default=0)
    popularity_score = Column(Integer, default=0)
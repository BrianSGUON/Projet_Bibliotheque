from sqlmodel import SQLModel, create_engine, Session # Importe Session 
import os

sqlite_file_name = "library.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    # Utilise la Session de SQLModel
    with Session(engine) as session:
        yield session

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# L'URL de connexion pour SQLite 
SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"

# Création de l'élément moteur(engine)
# 'check_same_thread' est spécifique à SQLite pour FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Configuration de la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe de base pour les modèles
Base = declarative_base()

# Bloc pour tester la création de la base de données
if __name__ == "__main__":
    import model
    # Cette ligne crée toutes les tables définies dans model.py 
    Base.metadata.create_all(bind=engine)
    print("La base de données et les tables ont été créées avec succès !")
# Projet_Bibliotheque

main.py : Lance l'application et regroupe les routes.  
routes/ : Gère les requêtes HTTP et les erreurs (404, 400).
service.py : Gère les calculs et règles complexes (ex: les 5 livres max).
crud.py : Gère uniquement les ordres SQL (SELECT, INSERT, DELETE).
model.py & schema.py : Définissent la structure des données.
fastapi dev pour lancer le serveur
http://127.0.0.1:8000/docs pour voir la page

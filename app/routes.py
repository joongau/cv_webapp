from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    cv_data = {
        "nom": "Jonathan Gaultier",
        "titre": "Conseiller commercial & futur Data Engineer",
        "profil": "Passionné par la tech, j'accompagne les clients chez Orange et me forme à la Data.",
        "experiences": [
            {
                "poste": "Conseiller commercial",
                "entreprise": "Orange",
                "periode": "2019 - aujourd’hui",
                "description": "Conseil, vente et fidélisation des clients en boutique."
            },
            {
                "poste": "Illustrateur indépendant",
                "entreprise": "Freelance",
                "periode": "2022 - aujourd’hui",
                "description": "Création de visuels artistiques et vente en ligne."
            }
        ],
        "competences": ["Python", "SQL", "Flask", "GitHub", "Vente", "Conseil client"]
    }
    return render_template("home.html", cv=cv_data)
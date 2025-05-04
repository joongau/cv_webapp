from flask import Blueprint, render_template
import json
import os

main = Blueprint('main', __name__)

@main.route('/')
def home():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, '../data/cv.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        cv_data = json.load(f)

    return render_template("home.html", cv=cv_data)

@main.route('/projets')
def projets():
    projets_data = [
        {
            "titre": "Mobrange",
            "description": "Application web de recommandation de smartphones basée sur les habitudes de vie des clients. Combine mes connaissances terrain et l’IA.",
            "année": "2025"
        },
        {
            "titre": "Clairdelunestudio.com",
            "description": "E-commerce de produits artisanaux personnalisés (affiches avec dorure), développé sur Shopify.",
            "année": "2023 – Aujourd’hui"
        }
    ]
    return render_template("projets.html", projets=projets_data)
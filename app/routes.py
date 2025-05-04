from flask import Blueprint, render_template
import json
import os
from flask import jsonify
from flask import request, redirect, url_for, session, flash


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

@main.route('/api/cv')
def api_cv():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, '../data/cv.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        cv_data = json.load(f)
    return jsonify(cv_data)

@main.route('/api/projets')
def api_projets():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, '../data/projets.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        projets_data = json.load(f)
    return jsonify(projets_data)

@main.route('/cv-js')
def cv_js():
    return render_template("cv_fetch.html")

@main.route('/projets-js')
def projets_js():
    return render_template("projets_fetch.html")


@main.route('/api/projets/ajouter', methods=['POST'])
def ajouter_projet():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, '../data/projets.json')

    try:
        # Charger les projets existants
        with open(json_path, 'r', encoding='utf-8') as f:
            projets = json.load(f)

        # Récupérer les données du nouveau projet
        data = request.get_json()
        if not data:
            return {"error": "Aucune donnée reçue"}, 400

        projets.append(data)

        # Sauvegarder
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(projets, f, ensure_ascii=False, indent=2)

        return {"message": "Projet ajouté"}, 201

    except Exception as e:
        return {"error": str(e)}, 500


# Nouvelle route DELETE pour supprimer un projet par son titre
@main.route('/api/projets/supprimer', methods=['DELETE'])
def supprimer_projet():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, '../data/projets.json')

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            projets = json.load(f)

        data = request.get_json()
        titre = data.get("titre")
        if not titre:
            return {"error": "Titre requis"}, 400

        projets = [p for p in projets if p["titre"] != titre]

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(projets, f, ensure_ascii=False, indent=2)

        return {"message": f"Projet '{titre}' supprimé"}, 200

    except Exception as e:
        return {"error": str(e)}, 500
    
@main.route('/admin/projets')
def admin_projets():
    if not session.get('logged_in'):
        return redirect(url_for('main.login'))
    return render_template("admin_projets.html")


# Route de connexion (login)
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'secret123':
            session['logged_in'] = True
            return redirect(url_for('main.admin_projets'))
        else:
            flash('Mot de passe incorrect')
    return render_template('login.html')


# Route de déconnexion (logout)
@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('main.login'))
import openai
from flask import Blueprint, render_template
import json
import os
from flask import jsonify
from flask import request, redirect, url_for, session, flash
# Set OpenAI API key for openai 0.28
openai.api_key = os.getenv("OPENAI_API_KEY")



base_dir = os.path.dirname(os.path.abspath(__file__))
cv_dir = os.path.join(base_dir, '../data/cv_parts')

main = Blueprint('main', __name__)

def charger_partie(nom_fichier):
    with open(os.path.join(cv_dir, nom_fichier), 'r', encoding='utf-8') as f:
        return json.load(f)

@main.route('/')
def home():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cv_dir = os.path.join(base_dir, '../data/cv_parts')

    cv_data = {
        **charger_partie('profil.json'),
        "competences_techniques": charger_partie('competences_techniques.json'),
        "competences_comportementales": charger_partie('competences_comportementales.json'),
        "experiences": charger_partie('experiences.json'),
        "formations": charger_partie('formations.json'),
        "contact": charger_partie('contact.json'),
        "projets": charger_partie('projets.json'),
    }

    return render_template("home.html", cv=cv_data)



@main.route('/api/cv')
def api_cv():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cv_dir = os.path.join(base_dir, '../data/cv_parts')

    cv_data = {
        **charger_partie('profil.json'),
        "competences_techniques": charger_partie('competences_techniques.json'),
        "competences_comportementales": charger_partie('competences_comportementales.json'),
        "experiences": charger_partie('experiences.json'),
        "formations": charger_partie('formations.json'),
        "contact": charger_partie('contact.json'),
        "projets": charger_partie('projets.json'),
    }
    return jsonify(cv_data)


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
        if request.form['password'] == os.getenv("ADMIN_PASSWORD"):
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


# Nouvelle route pour éditer les informations du CV
@main.route('/admin/cv', methods=['GET', 'POST'])
def admin_cv():
    if not session.get('logged_in'):
        return redirect(url_for('main.login'))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    cv_dir = os.path.join(base_dir, '../data/cv_parts')

    cv_data = {
        **charger_partie('profil.json'),
        "competences_techniques": charger_partie('competences_techniques.json'),
        "competences_comportementales": charger_partie('competences_comportementales.json'),
        "experiences": charger_partie('experiences.json'),
        "formations": charger_partie('formations.json'),
        "contact": charger_partie('contact.json'),
        "projets": charger_partie('projets.json'),
    }

    if request.method == 'POST':
        # Gestion de l'upload de la photo de profil
        upload = request.files.get("photo_file")
        photo_filename = request.form.get("profil_photo", "").strip()

        if upload and upload.filename:
            photo_filename = f"images/{upload.filename}"
            upload.save(os.path.join(base_dir, '../static/', photo_filename))
        try:
            data = {
                "nom": request.form["nom"],
                "titre": request.form["titre"],
                "profil": request.form["profil"],
                "competences_techniques": [],
                "competences_comportementales": [],
                "experiences": [],
                "formations": []
            }
            # Compétences techniques
            i = 0
            while True:
                nom = request.form.get(f"comptech_nom_{i}")
                note = request.form.get(f"comptech_note_{i}")
                if nom is None and note is None:
                    break
                if nom:
                    data["competences_techniques"].append({
                        "nom": nom.strip(),
                        "note": int(note) if note and note.isdigit() else 0
                    })
                i += 1

            # Compétences comportementales
            i = 0
            while True:
                nom = request.form.get(f"compsoft_nom_{i}")
                note = request.form.get(f"compsoft_note_{i}")
                if nom is None and note is None:
                    break
                if nom:
                    data["competences_comportementales"].append({
                        "nom": nom.strip(),
                        "note": int(note) if note and note.isdigit() else 0
                    })
                i += 1

            data["contact"] = {
                "téléphone": request.form.get("contact_téléphone", ""),
                "email": request.form.get("contact_email", ""),
                "adresse": request.form.get("contact_adresse", ""),
                "linkedin": request.form.get("contact_linkedin", ""),
                "github": request.form.get("contact_github", "")
            }

            for i in range(10):
                if f"exp_poste_{i}" in request.form:
                    data["experiences"].append({
                        "poste": request.form.get(f"exp_poste_{i}", ""),
                        "entreprise": request.form.get(f"exp_entreprise_{i}", ""),
                        "periode": request.form.get(f"exp_periode_{i}", ""),
                        "description": request.form.get(f"exp_description_{i}", "")
                    })

            for i in range(10):
                if f"form_diplome_{i}" in request.form:
                    data["formations"].append({
                        "diplome": request.form.get(f"form_diplome_{i}", ""),
                        "lieu": request.form.get(f"form_lieu_{i}", ""),
                        "periode": request.form.get(f"form_periode_{i}", ""),
                        "description": request.form.get(f"form_description_{i}", "")
                    })

            data["projets"] = []
            for i in range(10):
                if f"proj_titre_{i}" in request.form:
                    data["projets"].append({
                        "titre": request.form.get(f"proj_titre_{i}", ""),
                        "description": request.form.get(f"proj_description_{i}", ""),
                        "année": request.form.get(f"proj_année_{i}", ""),
                        "lien": request.form.get(f"proj_lien_{i}", "")
                    })

            with open(os.path.join(cv_dir, 'profil.json'), 'w', encoding='utf-8') as f:
                json.dump({
                    "nom": data["nom"],
                    "titre": data["titre"],
                    "profil": data["profil"],
                    "photo": photo_filename
                }, f, ensure_ascii=False, indent=2)

            with open(os.path.join(cv_dir, 'competences_techniques.json'), 'w', encoding='utf-8') as f:
                json.dump(data["competences_techniques"], f, ensure_ascii=False, indent=2)

            with open(os.path.join(cv_dir, 'competences_comportementales.json'), 'w', encoding='utf-8') as f:
                json.dump(data["competences_comportementales"], f, ensure_ascii=False, indent=2)

            with open(os.path.join(cv_dir, 'experiences.json'), 'w', encoding='utf-8') as f:
                json.dump(data["experiences"], f, ensure_ascii=False, indent=2)

            with open(os.path.join(cv_dir, 'formations.json'), 'w', encoding='utf-8') as f:
                json.dump(data["formations"], f, ensure_ascii=False, indent=2)

            with open(os.path.join(cv_dir, 'contact.json'), 'w', encoding='utf-8') as f:
                json.dump(data["contact"], f, ensure_ascii=False, indent=2)

            with open(os.path.join(cv_dir, 'projets.json'), 'w', encoding='utf-8') as f:
                json.dump(data["projets"], f, ensure_ascii=False, indent=2)

            flash("✅ CV mis à jour.")
            return redirect(url_for('main.admin_cv'))

        except Exception as e:
            flash(f"Erreur : {e}")

    return render_template("admin_cv.html", cv=cv_data)


# Nouvelle route /api/chat pour répondre aux questions sur le CV via OpenAI
@main.route('/api/chat', methods=['POST'])
def chatbot():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cv_dir = os.path.join(base_dir, '../data/cv_parts')

    try:
        cv_data = {
            **charger_partie('profil.json'),
            "competences_techniques": charger_partie('competences_techniques.json'),
            "competences_comportementales": charger_partie('competences_comportementales.json'),
            "experiences": charger_partie('experiences.json'),
            "formations": charger_partie('formations.json'),
            "contact": charger_partie('contact.json'),
            "projets": charger_partie('projets.json'),
        }

        data = request.get_json()
        question = data.get("question")

        if not question:
            return jsonify({"error": "Question manquante"}), 400

        cv_complet = "\n".join([
            f"Nom : {cv_data['nom']}",
            f"Titre : {cv_data['titre']}",
            f"Profil : {cv_data['profil']}",
            "Compétences techniques : " + ", ".join([f"{c['nom']} ({c['note']}/5)" for c in cv_data['competences_techniques']]),
            "Compétences comportementales : " + ", ".join([f"{c['nom']} ({c['note']}/5)" for c in cv_data['competences_comportementales']]),
            "Expériences :\n" + "\n".join([f"- {e['poste']} chez {e['entreprise']} ({e['periode']}) : {e['description']}" for e in cv_data['experiences']]),
            "Formations :\n" + "\n".join([f"- {f['diplome']} à {f['lieu']} ({f['periode']}) : {f['description']}" for f in cv_data['formations']]),
            "Projets :\n" + "\n".join([f"- {p['titre']} ({p['année']}) : {p['description']}" + (f" ({p['lien']})" if p.get("lien") else "") for p in cv_data['projets']])
        ])

        messages = [
            {
                "role": "system",
                "content": (
                    "Tu es un assistant intelligent et bienveillant qui connaît parfaitement le CV de Jonathan.\n"
                    "Réponds uniquement en te basant sur les informations suivantes :\n"
                    f"{cv_complet}"
                    "Voici quelques traits importants de sa personnalité à prendre en compte :\n"
                    "- Curieux, structuré, rigoureux, gentil, attentionné, polyvalent, auto-didacte, professionnel, passionné par l'informatique et les technologies\n"
                    "- Très bon relationnel client\n"
                    "- Aime apprendre et transmettre\n"
                    "- Passionné par l'IA, l'automatisation et la programmation\n"
                    "- Aime le travail en équipe et la collaboration\n"
                    "- Aime le challenge et la résolution de problèmes\n"
                    "- Aime la créativité et l'innovation\n"
                    "- Aime la musique, le cinéma, les jeux vidéo et la culture geek\n"
                    "- Aime la nature et les activités de plein air\n"
                    "- Aime la cuisine et la gastronomie\n"
                    "- Aime le voyage et la découverte de nouvelles cultures\n"
                    "- Aime la photographie et la vidéo\n"
                    "- Aime le sport et le fitness\n"
                    "- Aime la lecture et l'écriture\n"
                    "- Aime l'art et la culture\n"
                    "- Aime la technologie et l'innovation\n"
                    "- Aime la science et la recherche\n"
                    "- Aime l'éducation et la formation\n"
                    "- Aime la solidarité et l'entraide\n"
                    "- Aime la diversité et l'inclusion\n"
                    "- Aime la responsabilité et l'engagement\n"
                    "- Aime la durabilité et l'environnement\n"
                    "- Aime la sécurité et la confidentialité\n"
                    "- Aime la qualité et l'excellence\n"
                    "- Aime la transparence et l'intégrité\n"
                    "- Aime la confiance et le respect\n"
                    "- Aime la loyauté et la fidélité\n"
                    "- Aime la justice et l'équité\n"
                    "- Aime la paix et la tolérance\n"
                    "- Aime la liberté et l'autonomie\n"
                    "- Aime la créativité et l'innovation\n"
                    "- Aime la curiosité et l'ouverture d'esprit\n"
                    "- Aime la passion et l'enthousiasme\n"
                    "- Aime la détermination et la persévérance\n"
                    "- Aime la sécurité et la confidentialité\n"
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return jsonify({"answer": response.choices[0].message['content']})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
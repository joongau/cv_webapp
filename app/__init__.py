from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_key")
    CORS(app)
    from .routes import main
    app.register_blueprint(main)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    return app
"""Flask app factory."""

import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from api.routes import api_bp
from core.container import build_service
from core.logging import configure_logging


def create_app() -> Flask:
    load_dotenv()
    configure_logging()

    app = Flask(__name__, static_folder="../frontend", static_url_path="")
    CORS(app)

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app.config["UPLOAD_FOLDER"] = os.path.join(root_dir, "uploads")
    app.config["RAG_SERVICE"] = build_service()

    @app.route("/")
    def index():
        return app.send_static_file("index.html")

    @app.after_request
    def add_header(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response

    app.register_blueprint(api_bp)
    return app


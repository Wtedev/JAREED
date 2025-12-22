# backend/app/__init__.py
# backend/app/__init__.py

import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    CORS(app)

    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        db_url = "sqlite:///jareed.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # مهم: استيراد الموديلات هنا (بعد db.init_app) لتفادي الـ circular import
    with app.app_context():
        from . import models  # يكفي عشان يسجل InventoryItem
        db.create_all()

    from .routes import products_bp
    app.register_blueprint(products_bp)

    return app
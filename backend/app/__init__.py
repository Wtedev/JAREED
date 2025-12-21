# backend/app/__init__.py

import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# 1. نهيئ SQLAlchemy هنا ولكن بدون ربطه بالتطبيق بعد
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jareed.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    


    # 4. نستورد ونسجل المخطط (Blueprint)
    # نضع الاستيراد هنا لتجنب الأخطاء الدائرية (Circular Imports)
    from .routes import products_bp
    app.register_blueprint(products_bp)

    return app

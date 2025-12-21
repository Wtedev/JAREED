import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jareed.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # ✅ تسجيل صفحات الويب
    from .pages import pages_bp
    app.register_blueprint(pages_bp)

    # ✅ تسجيل API
    from .routes import products_bp
    app.register_blueprint(products_bp)

    return app

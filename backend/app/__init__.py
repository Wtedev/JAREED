import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    load_dotenv()

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "static"),
    )

    # ✅ Secrets
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-change-me")

    # ✅ DB
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///jareed.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ Secure cookies (كويس محليًا + ممتاز للإنتاج)
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    # في الإنتاج خليه True مع HTTPS:
    app.config["SESSION_COOKIE_SECURE"] = False  # True in production over HTTPS
    app.config["REMEMBER_COOKIE_HTTPONLY"] = True
    app.config["REMEMBER_COOKIE_SAMESITE"] = "Lax"
    app.config["REMEMBER_COOKIE_SECURE"] = False  # True in production over HTTPS

    db.init_app(app)

    # ✅ Auth
    login_manager.init_app(app)
    
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    login_manager.login_view = "auth.login"  # redirect if not logged in
    login_manager.login_message = "فضلاً سجّل الدخول للمتابعة."

    # ✅ CSRF (يحمي POST/PUT/DELETE في صفحات الويب)
    csrf.init_app(app)

    # ✅ Rate limit
    limiter.init_app(app)

    # Blueprints
    from .routes import products_bp
    app.register_blueprint(products_bp)
    csrf.exempt(products_bp) 

    from .pages import pages_bp
    app.register_blueprint(pages_bp)
    

    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    csrf.exempt(auth_bp)
    


    return app

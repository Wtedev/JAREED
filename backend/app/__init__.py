# backend/app/__init__.py

import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# 1. نهيئ SQLAlchemy هنا ولكن بدون ربطه بالتطبيق بعد
db = SQLAlchemy()

def create_app():
    # هذه هي دالة Application Factory.
    # وظيفتها إنشاء وتهيئة تطبيق Flask.
    app = Flask(__name__)
    CORS(app)

    # 2. ربط التطبيق برابط قاعدة البيانات من متغيرات البيئة
    # هذاالسطر يقرأ الرابط الذي سنضعه في رندر لاحقا
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # لتحسين الأداء

    # 3. نربط كائن قاعدة البيانات (db) بالتطبيق
    db.init_app(app)


    # 4. نستورد ونسجل المخطط (Blueprint)
    # نضع الاستيراد هنا لتجنب الأخطاء الدائرية (Circular Imports)
    from .routes import products_bp
    app.register_blueprint(products_bp)

    return app

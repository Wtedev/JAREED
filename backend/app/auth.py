from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User

auth_bp = Blueprint("auth", __name__)


def _is_valid_email(email: str) -> bool:
    return "@" in email and "." in email and len(email) <= 190


# =========================
# Register
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("pages.warehouse"))

    if request.method == "GET":
        return render_template("register.html", title="إنشاء حساب")

    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    confirm = request.form.get("confirm_password") or ""

    print("FORM:", request.form)
    print("EMAIL:", email, "PASS_LEN:", len(password), "CONF_LEN:", len(confirm))

    if not email or not password or not confirm:
        flash("فضلاً عبّي جميع الحقول.", "danger")
        return render_template("register.html", title="إنشاء حساب"), 400
    
    if not _is_valid_email(email):
        flash("البريد الإلكتروني غير صحيح.", "danger")
        return render_template("register.html", title="إنشاء حساب"), 400

    if len(password) < 8:
        flash("كلمة المرور لازم تكون 8 أحرف على الأقل.", "danger")
        return render_template("register.html", title="إنشاء حساب"), 400

    if password != confirm:
        flash("كلمتا المرور غير متطابقتين.", "danger")
        return render_template("register.html", title="إنشاء حساب"), 400

    if User.query.filter_by(email=email).first():
        flash("هذا البريد مسجّل مسبقًا. جرّبي تسجيل الدخول.", "danger")
        return render_template("register.html", title="إنشاء حساب"), 409

    try:
        user = User(email=email, is_active=True)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

    except Exception:
        db.session.rollback()
        flash("صار خطأ أثناء إنشاء الحساب. جرّبي مرة ثانية.", "danger")
        return render_template("register.html", title="إنشاء حساب"), 500

    login_user(user)
    flash("تم إنشاء الحساب بنجاح ✅", "success")
    return redirect(url_for("pages.warehouse"))


# =========================
# Login
# =========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("pages.warehouse"))

    if request.method == "GET":
        return render_template("login.html", title="تسجيل الدخول")

    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    remember = True if request.form.get("remember") else False

    if not email or not password:
        flash("فضلاً أدخلي البريد وكلمة المرور.", "danger")
        return render_template("login.html", title="تسجيل الدخول"), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        flash("بيانات الدخول غير صحيحة.", "danger")
        return render_template("login.html", title="تسجيل الدخول"), 401

    if not user.is_active:
        flash("هذا الحساب غير مفعل.", "danger")
        return render_template("login.html", title="تسجيل الدخول"), 403

    login_user(user, remember=remember)
    return redirect(request.args.get("next") or url_for("pages.warehouse"))

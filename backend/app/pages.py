from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required


pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
def home():
    return redirect(url_for("pages.warehouse"))

@pages_bp.route("/warehouse")
@login_required
def warehouse():
    return render_template("warehouse.html", title="Warehouse")

@pages_bp.route("/products")
@login_required
def products():
    return render_template("products.html", title="Products")

@pages_bp.route("/boxes")
@login_required
def boxes():
    return render_template("boxes.html", title="Boxes")

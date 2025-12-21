from flask import Blueprint, render_template, redirect, url_for

pages_bp = Blueprint("pages", __name__)

@pages_bp.route("/")
def home():
    return redirect(url_for("pages.warehouse"))

@pages_bp.route("/warehouse")
def warehouse():
    return render_template("warehouse.html", title="Warehouse")

@pages_bp.route("/products")
def products():
    return render_template("products.html", title="Products")

@pages_bp.route("/boxes")
def boxes():
    return render_template("boxes.html", title="Boxes")

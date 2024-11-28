"""Rutas públicas de la aplicación."""

from flask import Blueprint, render_template

public = Blueprint("public", __name__)


@public.route("/")
def index():
    """Ruta principal de la aplicación."""
    return render_template("index.html")

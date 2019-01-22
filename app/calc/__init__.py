from flask import Blueprint

bp = Blueprint('calc', __name__)

from app.calc import calculations

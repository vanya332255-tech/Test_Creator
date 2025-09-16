from flask import Blueprint

quizzes_bp = Blueprint("quizzes", __name__, url_prefix="/quizzes")

from . import routes

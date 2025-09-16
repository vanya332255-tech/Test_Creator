from flask import render_template

from .auth import auth_bp
from .quizzes import quizzes_bp


def create_app():
    app = Flask(__name__, template_folder="../../templates", static_folder="../../static")
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Регистрация blueprints
    app.register_blueprint(auth_bp)  # <-- это важно!
    app.register_blueprint(quizzes_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

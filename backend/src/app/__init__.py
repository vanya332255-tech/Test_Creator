from flask import Flask, render_template
from .config import Config
from .extensions import db, migrate, login_manager
from .auth import auth_bp
from .quizzes import quizzes_bp
from .auth.telegram import init_telegram
from .auth.google import init_google


def create_app():
    app = Flask(__name__, template_folder="../../templates", static_folder="../../static")
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(quizzes_bp)

    # init providers (Google, Telegram)
    with app.app_context():
        init_google(app)
        init_telegram(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return db.session.get(User, int(user_id))

    return app

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

    # CLI команди
    @app.cli.command()
    def createsuperuser():
        """Створити суперюзера"""
        from .models import User
        import getpass
        
        print("=== Створення суперюзера ===")
        
        # Запитуємо дані
        username = input("Username: ").strip()
        if not username:
            print("❌ Username не може бути порожнім!")
            return
            
        email = input("Email: ").strip()
        if not email:
            print("❌ Email не може бути порожнім!")
            return
            
        first_name = input("Ім'я: ").strip()
        last_name = input("Прізвище: ").strip()
        
        password = input("Пароль: ").strip()
        if not password:
            print("❌ Пароль не може бути порожнім!")
            return
        
        # Перевіряємо чи існує користувач
        existing_user = db.session.execute(
            db.select(User).filter(
                (User.email == email) | (User.username == username)
            )
        ).scalar_one_or_none()
        
        if existing_user:
            print(f"❌ Користувач з email {email} або username {username} вже існує!")
            return
        
        # Створюємо суперюзера
        superuser = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            auth_provider='admin',
            is_active=True,
            is_admin=True
        )
        superuser.set_password(password)
        
        db.session.add(superuser)
        db.session.commit()
        
        print(f"✅ Суперюзер створено: {email}")
        print(f"   ID: {superuser.id}")
        print(f"   Username: {username}")
        print(f"   Ім'я: {first_name} {last_name}")

    @app.cli.command()
    def listusers():
        """Показати всіх користувачів"""
        from .models import User
        
        users = db.session.execute(db.select(User)).scalars()
        
        print("=== Список користувачів ===")
        for user in users:
            print(f"ID: {user.id} | Email: {user.email} | Ім'я: {user.first_name} {user.last_name} | Провайдер: {user.auth_provider}")

    return app

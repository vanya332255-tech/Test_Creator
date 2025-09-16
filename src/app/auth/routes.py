from flask import render_template, redirect, url_for, request, flash, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from ..extensions import db
from ..models import User
from .google import init_google, login_google, handle_google_callback
from .telegram import init_telegram, codes, send_code
from .forms import LoginForm, RegistrationForm


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Сторінка входу"""
    if current_user.is_authenticated:
        return redirect(url_for('quizzes.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Шукаємо користувача за username або email
        user = db.session.execute(
            db.select(User).filter(
                (User.username == form.username.data) | 
                (User.email == form.username.data)
            )
        ).scalar_one_or_none()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Вітаємо, {user.first_name or user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('quizzes.dashboard'))
        else:
            flash('Невірний username/email або пароль', 'error')
    
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Сторінка реєстрації з верифікацією через Google Forms"""
    if current_user.is_authenticated:
        return redirect(url_for('quizzes.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Зберігаємо дані реєстрації в сесії для верифікації
        session['pending_registration'] = {
            'username': form.username.data,
            'email': form.email.data,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'password': form.password.data
        }
        
        flash('Будь ласка, заповніть Google Form для підтвердження реєстрації.', 'info')
        return redirect(url_for('auth.verify_registration'))
    
    return render_template("auth/register.html", form=form)


@auth_bp.route("/verify-registration", methods=["GET", "POST"])
def verify_registration():
    """Верифікація реєстрації через Google Forms"""
    if current_user.is_authenticated:
        return redirect(url_for('quizzes.dashboard'))
    
    # Перевіряємо, чи є дані реєстрації в сесії
    if 'pending_registration' not in session:
        flash('Немає даних для верифікації. Будь ласка, спочатку зареєструйтеся.', 'error')
        return redirect(url_for('auth.register'))
    
    if request.method == 'POST':
        verification_code = request.form.get('verification_code', '').strip()
        
        if verification_code:
            # Тут можна додати логіку перевірки коду з Google Forms
            # Поки що приймаємо будь-який код для демонстрації
            if len(verification_code) >= 6:  # Мінімальна довжина коду
                # Створюємо користувача
                user_data = session['pending_registration']
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    auth_provider='local'
                )
                user.set_password(user_data['password'])
                db.session.add(user)
                db.session.commit()
                
                # Очищаємо сесію
                session.pop('pending_registration', None)
                
                flash('Реєстрація успішна! Тепер ви можете увійти в систему.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash('Код верифікації повинен містити принаймні 6 символів.', 'error')
        else:
            flash('Будь ласка, введіть код верифікації.', 'error')
    
    return render_template("auth/verify_registration.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Вихід з системи"""
    logout_user()
    return redirect(url_for("index"))


# ======== Google OAuth ========

@auth_bp.route("/google")
def google_login():
    return login_google()


@auth_bp.route("/google/callback")
def google_callback():
    try:
        return handle_google_callback(db, User, login_user)
    except Exception as e:
        current_app.logger.error(f"Google OAuth error: {e}")
        flash('Помилка авторизації через Google. Спробуйте ще раз.', 'error')
        return redirect(url_for('auth.login'))


# ======== Telegram Auth ========

@auth_bp.route("/telegram")
def telegram_login():
    return render_template("auth/link_telegram.html")


@auth_bp.route("/telegram/send_code", methods=["POST"])
def telegram_send_code():
    phone = request.form.get("phone", "").strip()
    if not phone:
        flash("Введіть номер телефону", "error")
        return redirect(url_for("auth.telegram_login"))

    code = codes.issue_code(phone)

    # Отправляем код через бота
    import asyncio
    ok = asyncio.run(send_code(phone, code))
    if not ok:
        flash("Спочатку запустіть бота та поділіться номером, щоб ми могли надіслати код.", "error")
        return redirect(url_for("auth.telegram_login"))

    flash("Код надіслано в Telegram. Введіть його нижче.", "success")
    return render_template("auth/link_telegram.html", phone=phone, wait_code=True)


@auth_bp.route("/telegram/verify", methods=["POST"])
def telegram_verify():
    phone = request.form.get("phone", "").strip()
    code = request.form.get("code", "").strip()

    if not codes.verify(phone, code):
        flash("Невірний або прострочений код", "error")
        return redirect(url_for("auth.telegram_login"))

    # Находим или создаём пользователя
    user = db.session.execute(
        db.select(User).filter_by(phone=phone)
    ).scalar_one_or_none()

    if not user:
        user = User(phone=phone, auth_provider="telegram")
        db.session.add(user)
        db.session.commit()
        flash("Акаунт успішно створено!", "success")
    else:
        flash("Вітаємо! Ви успішно увійшли в систему.", "success")

    login_user(user)
    return redirect(url_for("quizzes.dashboard"))

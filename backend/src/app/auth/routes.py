from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, current_user, login_required
from . import auth_bp
from ..extensions import db
from ..models import User
from .google import init_google, login_google, handle_google_callback
from .telegram import init_telegram, codes, send_code


@auth_bp.before_app_first_request
def _init_providers():
    init_google(current_app)
    init_telegram(current_app)


@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@auth_bp.route('/google')
def google_login():
    return login_google()


@auth_bp.route('/google/callback')
def google_callback():
    return handle_google_callback(db, User, login_user)


@auth_bp.route('/telegram')
def telegram_login():
    return render_template('auth/link_telegram.html')


@auth_bp.route('/telegram/send_code', methods=['POST'])
def telegram_send_code():
    phone = request.form.get('phone', '').strip()
    if not phone:
        flash('Введите номер телефона')
        return redirect(url_for('auth.telegram_login'))
    code = codes.issue_code(phone)
    # Отправляем код через бота
    import asyncio
    ok = asyncio.run(send_code(phone, code))
    if not ok:
        flash('Сначала запустите бота и поделитесь номером, чтобы мы могли отправить код.')
        return redirect(url_for('auth.telegram_login'))
    flash('Код отправлен в Telegram. Введите его ниже.')
    return render_template('auth/link_telegram.html', phone=phone, wait_code=True)


@auth_bp.route('/telegram/verify', methods=['POST'])
def telegram_verify():
    phone = request.form.get('phone', '').strip()
    code = request.form.get('code', '').strip()
    if not codes.verify(phone, code):
        flash('Неверный или просроченный код')
        return redirect(url_for('auth.telegram_login'))
    # Находим/создаём пользователя по телефону
    user = db.session.execute(db.select(User).filter_by(phone=phone)).scalar_one_or_none()
    if not user:
        user = User(phone=phone, auth_provider='telegram')
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('quizzes.dashboard'))

from flask import current_app, url_for, redirect, request
from authlib.integrations.flask_client import OAuth

oauth = OAuth()


def init_google(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'}
    )


def login_google():
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


def handle_google_callback(db, User, login_user):
    token = oauth.google.authorize_access_token()
    userinfo = token.get('userinfo')
    if not userinfo:
        userinfo = oauth.google.parse_id_token(token)
    
    sub = userinfo.get('sub')
    email = userinfo.get('email')
    first = userinfo.get('given_name')
    last = userinfo.get('family_name')

    if not sub or not email:
        return redirect(url_for('auth.login'))

    user = db.session.execute(db.select(User).filter_by(google_sub=sub)).scalar_one_or_none()
    if not user and email:
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
    if not user:
        user = User(email=email, first_name=first, last_name=last, auth_provider='google', google_sub=sub)
        db.session.add(user)
    else:
        user.first_name = first or user.first_name
        user.last_name = last or user.last_name
        user.auth_provider = 'google'
        user.google_sub = sub
    db.session.commit()
    login_user(user)
    return redirect(url_for('quizzes.dashboard'))

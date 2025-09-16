from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from ..models import User


class LoginForm(FlaskForm):
    username = StringField('Username або Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Увійти')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=20, message='Username повинен бути від 3 до 20 символів')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Ім\'я', validators=[DataRequired(), Length(max=120)])
    last_name = StringField('Прізвище', validators=[DataRequired(), Length(max=120)])
    password = PasswordField('Пароль', validators=[
        DataRequired(), 
        Length(min=6, message='Пароль повинен бути мінімум 6 символів')
    ])
    password2 = PasswordField('Підтвердіть пароль', validators=[
        DataRequired(), 
        EqualTo('password', message='Паролі не співпадають')
    ])
    submit = SubmitField('Зареєструватися')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Цей username вже зайнятий. Оберіть інший.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Цей email вже зареєстрований. Оберіть інший.')

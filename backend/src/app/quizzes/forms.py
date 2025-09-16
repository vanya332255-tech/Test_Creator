from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional


class QuizTitleForm(FlaskForm):
    title = StringField(
        "Назва тесту",
        validators=[DataRequired(message="Назва тесту обов'язкова"), Length(min=3, max=255, message="Назва повинна бути від 3 до 255 символів")]
    )


class QuestionForm(FlaskForm):
    title = TextAreaField(
        "Текст питання",
        validators=[DataRequired(message="Текст питання обов'язковий"), Length(min=5, max=1000, message="Текст питання повинен бути від 5 до 1000 символів")]
    )
    qtype = SelectField(
        "Тип питання",
        choices=[('single', 'Один правильний відповідь'), ('multi', 'Кілька правильних відповідей'), ('open', 'Відкрите питання')],
        validators=[DataRequired(message="Оберіть тип питання")]
    )


class ChoiceForm(FlaskForm):
    text = StringField(
        "Варіант відповіді",
        validators=[DataRequired(message="Текст варіанту обов'язковий"), Length(min=1, max=500, message="Текст варіанту повинен бути від 1 до 500 символів")]
    )


class SearchForm(FlaskForm):
    code = StringField(
        "Код тесту",
        validators=[DataRequired(message="Введіть код тесту"), Length(min=6, max=6, message="Код повинен містити рівно 6 символів")]
    )

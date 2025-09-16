from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class QuizTitleForm(FlaskForm):
    title = StringField(
        "Название теста",
        validators=[DataRequired(), Length(max=255)]
    )

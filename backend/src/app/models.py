from datetime import datetime
from flask_login import UserMixin
from .extensions import db

google_sub = db.Column(db.String(255), unique=True)
telegram_user_id = db.Column(db.String(64), unique=True)
is_active = db.Column(db.Boolean, default=True)
created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True)
    phone = db.Column(db.String(32), unique=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    auth_provider = db.Column(db.String(20))  # 'google' | 'telegram'
    google_sub = db.Column(db.String(255), unique=True)
    telegram_user_id = db.Column(db.String(64), unique=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(6), unique=True, index=True, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = db.relationship('User', backref='quizzes')
    questions = db.relationship('Question', cascade='all, delete-orphan', backref='quiz', order_by='Question.id')


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    qtype = db.Column(db.String(10), nullable=False)  # 'single' | 'multi' | 'open'
    choices = db.relationship('Choice', cascade='all, delete-orphan', backref='question', order_by='Choice.id')


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    quiz = db.relationship('Quiz')
    answers = db.relationship('Answer', cascade='all, delete-orphan', backref='submission')


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    text = db.Column(db.Text)  # для open
    selected = db.relationship('AnswerChoice', cascade='all, delete-orphan', backref='answer')


class AnswerChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey('choice.id'), nullable=False)

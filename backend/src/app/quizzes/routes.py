from flask import render_template, redirect, url_for, request, abort, flash
from flask_login import login_required, current_user
from . import quizzes_bp
from ..extensions import db
from ..models import Quiz, Question, Choice, Submission, Answer, AnswerChoice
from .forms import QuizTitleForm
from .services import gen_code


@quizzes_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@quizzes_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_quiz():
    form = QuizTitleForm()
    if form.validate_on_submit():
        qz = Quiz(owner_id=current_user.id, title=form.title.data, code=gen_code())
        db.session.add(qz)
        db.session.commit()
        return redirect(url_for("quizzes.edit_quiz", quiz_id=qz.id))
    return render_template("quizzes/new.html", form=form)


@quizzes_bp.route("/<int:quiz_id>/edit", methods=["GET", "POST"])
@login_required
def edit_quiz(quiz_id):
    qz = db.session.get(Quiz, quiz_id)
    if not qz or qz.owner_id != current_user.id:
        abort(404)
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add_question":
            title = request.form.get("q_title")
            qtype = request.form.get("q_type")
            if title and qtype in ("single", "multi", "open"):
                q = Question(quiz_id=qz.id, title=title, qtype=qtype)
                db.session.add(q)
                db.session.commit()
        elif action == "delete_question":
            qid = int(request.form.get("qid"))
            q = db.session.get(Question, qid)
            if q and q.quiz_id == qz.id:
                db.session.delete(q)
                db.session.commit()
        elif action == "toggle_publish":
            qz.is_published = not qz.is_published
            db.session.commit()
        elif action == "add_choice":
            qid = int(request.form.get("qid"))
            text = request.form.get("choice_text")
            if text:
                ch = Choice(question_id=qid, text=text)
                db.session.add(ch)
                db.session.commit()
        elif action == "set_correct":
            cid = int(request.form.get("cid"))
            ch = db.session.get(Choice, cid)
            if ch and ch.question.quiz_id == qz.id:
                if ch.question.qtype == "single":
                    for other in ch.question.choices:
                        other.is_correct = (other.id == ch.id)
                else:
                    ch.is_correct = not ch.is_correct
                db.session.commit()
        elif action == "delete_choice":
            cid = int(request.form.get("cid"))
            ch = db.session.get(Choice, cid)
            if ch and ch.question.quiz_id == qz.id:
                db.session.delete(ch)
                db.session.commit()
        return redirect(url_for("quizzes.edit_quiz", quiz_id=qz.id))

    return render_template("quizzes/edit.html", quiz=qz)


@quizzes_bp.route("/my")
@login_required
def my_quizzes():
    items = db.session.execute(
        db.select(Quiz).filter_by(owner_id=current_user.id).order_by(Quiz.created_at.desc())
    ).scalars()
    return render_template("quizzes/my.html", items=items)


@quizzes_bp.route("/find", methods=["GET", "POST"])
@login_required
def find_quiz():
    if request.method == "POST":
        code = request.form.get("code", "").strip().upper()
        qz = db.session.execute(db.select(Quiz).filter_by(code=code, is_published=True)).scalar_one_or_none()
        if not qz:
            flash("Тест не найден или не опубликован")
        else:
            return redirect(url_for("quizzes.take_quiz", code=code))
    return render_template("quizzes/find.html")


@quizzes_bp.route("/take/<code>", methods=["GET", "POST"])
@login_required
def take_quiz(code):
    qz = db.session.execute(db.select(Quiz).filter_by(code=code, is_published=True)).scalar_one_or_none()
    if not qz:
        abort(404)
    if request.method == "POST":
        sub = Submission(quiz_id=qz.id, user_id=current_user.id)
        db.session.add(sub)
        score = 0
        total = 0
        for q in qz.questions:
            total += 1
            ans = Answer(submission_id=sub.id, question_id=q.id)
            db.session.add(ans)
            if q.qtype in ("single", "multi"):
                selected_ids = request.form.getlist(f"q_{q.id}")
                correct_ids = {str(c.id) for c in q.choices if c.is_correct}
                for sid in selected_ids:
                    db.session.add(AnswerChoice(answer_id=ans.id, choice_id=int(sid)))
                if set(selected_ids) == correct_ids:
                    score += 1
            else:
                ans.text = request.form.get(f"q_{q.id}", "")
        sub.score = score
        sub.total = total
        db.session.commit()
        return redirect(url_for("quizzes.results", quiz_id=qz.id))

    return render_template("quizzes/take.html", quiz=qz)


@quizzes_bp.route("/<int:quiz_id>/results")
@login_required
def results(quiz_id):
    qz = db.session.get(Quiz, quiz_id)
    if not qz:
        abort(404)
    subs = db.session.execute(
        db.select(Submission).filter_by(quiz_id=qz.id).order_by(Submission.created_at.desc())
    ).scalars()
    return render_template("quizzes/results.html", quiz=qz, subs=subs)

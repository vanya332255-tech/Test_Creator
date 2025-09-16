import random, string
from ..extensions import db
from ..models import Quiz

ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'


def gen_code(length=6):
    while True:
        code = ''.join(random.choice(ALPHABET) for _ in range(length))
        exists = db.session.execute(db.select(Quiz).filter_by(code=code)).scalar_one_or_none()
        if not exists:
            return code

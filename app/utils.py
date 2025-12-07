import string
import random
from sqlalchemy.orm import Session
from .models import URL


def generate_short_code(db: Session, length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(chars) for _ in range(length))
        existing = db.query(URL).filter(URL.short_code == code).first()
        if not existing:
            return code


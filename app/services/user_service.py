from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email.lower()).first()

    def authenticate(self, email: str, password: str):
        user = self.get_by_email(email)
        if not user:
            return None
        if not user.is_active:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def create_user(self, *, name: str, email: str, password: str, role: str):
        now = datetime.now(timezone.utc)
        user = User(
            name=name,
            email=email.lower(),
            password_hash=hash_password(password),
            role=role,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except IntegrityError:
            self.db.rollback()
            raise
        return user

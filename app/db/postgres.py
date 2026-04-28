from datetime import datetime, timezone
from typing import Generator

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings
from app.core.security import hash_password


class Base(DeclarativeBase):
    pass


settings = get_settings()
engine = create_engine(settings.postgres_dsn, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.models import User

    # Schema lifecycle is handled by Alembic migrations.
    # Startup should only perform data bootstrap tasks.
    if not inspect(engine).has_table("users"):
        return

    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.email == settings.bootstrap_admin_email.lower()).first()
        if not existing_admin:
            now = datetime.now(timezone.utc)
            admin_user = User(
                name=settings.bootstrap_admin_name,
                email=settings.bootstrap_admin_email.lower(),
                password_hash=hash_password(settings.bootstrap_admin_password),
                role="admin",
                is_active=True,
                created_at=now,
                updated_at=now,
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()

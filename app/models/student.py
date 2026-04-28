from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.postgres import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    father_name: Mapped[str] = mapped_column(String(120), nullable=False)
    mother_name: Mapped[str] = mapped_column(String(120), nullable=False)
    birthdate: Mapped[date] = mapped_column(Date, nullable=False)
    address: Mapped[str] = mapped_column(String(300), nullable=False)
    student_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    father_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    enrollment_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    class_name: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    batch: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    linkedin: Mapped[str | None] = mapped_column(String(255), nullable=True)
    github: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

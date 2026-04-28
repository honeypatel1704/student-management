from datetime import datetime, timezone
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.student import Student


class StudentService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _to_response(document):
        return {
            "id": str(document.id),
            "name": document.name,
            "father_name": document.father_name,
            "mother_name": document.mother_name,
            "birthdate": document.birthdate,
            "address": document.address,
            "student_phone": document.student_phone,
            "father_phone": document.father_phone,
            "enrollment_number": document.enrollment_number,
            "class_name": document.class_name,
            "batch": document.batch,
            "email": document.email,
            "linkedin": document.linkedin,
            "github": document.github,
            "created_at": document.created_at,
            "updated_at": document.updated_at,
        }

    def create(self, payload):
        now = datetime.now(timezone.utc)
        # Remove keys that we'll explicitly set to avoid duplicate keyword args
        sanitized = {k: v for k, v in payload.items() if k not in ("enrollment_number", "email")}

        document = Student(
            **sanitized,
            enrollment_number=payload["enrollment_number"].upper(),
            email=payload["email"].lower(),
            created_at=now,
            updated_at=now,
        )
        try:
            self.db.add(document)
            self.db.commit()
            self.db.refresh(document)
        except IntegrityError as exc:
            self.db.rollback()
            raise ValueError("Enrollment number already exists") from exc

        return self._to_response(document)

    def list(self, *, page: int, page_size: int, q: str | None, class_name: str | None, batch: str | None):
        base_query = self.db.query(Student)
        if q:
            like_term = f"%{q}%"
            base_query = base_query.filter(
                or_(
                    Student.name.ilike(like_term),
                    Student.enrollment_number.ilike(like_term),
                    Student.email.ilike(like_term),
                )
            )
        if class_name:
            base_query = base_query.filter(func.lower(Student.class_name) == class_name.lower())
        if batch:
            base_query = base_query.filter(func.lower(Student.batch) == batch.lower())

        total = base_query.count()
        items_raw = (
            base_query.order_by(Student.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        items = [self._to_response(item) for item in items_raw]
        return {"page": page, "page_size": page_size, "total": total, "items": items}

    def get_by_enrollment(self, enrollment_number: str):
        document = self.db.query(Student).filter(Student.enrollment_number == enrollment_number.upper()).first()
        if not document:
            return None
        return self._to_response(document)

    def update(self, enrollment_number: str, payload):
        existing = self.db.query(Student).filter(Student.enrollment_number == enrollment_number.upper()).first()
        if not existing:
            return None

        payload = {
            **payload,
            "email": payload["email"].lower(),
            "updated_at": datetime.now(timezone.utc),
            "enrollment_number": existing.enrollment_number,
        }

        for key, value in payload.items():
            setattr(existing, key, value)

        self.db.commit()
        self.db.refresh(existing)
        return self._to_response(existing)

    def delete(self, enrollment_number: str) -> bool:
        existing = self.db.query(Student).filter(Student.enrollment_number == enrollment_number.upper()).first()
        if not existing:
            return False
        self.db.delete(existing)
        self.db.commit()
        return True

    def stats(self):
        total = self.db.query(Student).count()
        classes = (
            self.db.query(Student.class_name, func.count(Student.id).label("count"))
            .group_by(Student.class_name)
            .order_by(func.count(Student.id).desc())
            .all()
        )
        return {
            "total_students": total,
            "students_by_class": [{"class_name": c.class_name, "count": c.count} for c in classes],
        }

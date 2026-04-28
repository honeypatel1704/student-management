from datetime import date, datetime, timezone

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.student import Student


class AttendanceService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def _to_response(document: Attendance, student: Student):
        return {
            "id": str(document.id),
            "student_id": str(student.id),
            "enrollment_number": student.enrollment_number,
            "student_name": student.name,
            "attendance_date": document.attendance_date,
            "status": document.status,
            "remarks": document.remarks,
            "created_at": document.created_at,
            "updated_at": document.updated_at,
        }

    def create(self, payload):
        student = (
            self.db.query(Student)
            .filter(Student.enrollment_number == payload["enrollment_number"].upper())
            .first()
        )
        if not student:
            raise LookupError("Student not found")

        now = datetime.now(timezone.utc)
        document = Attendance(
            student_id=student.id,
            attendance_date=payload["attendance_date"],
            status=payload["status"],
            remarks=payload.get("remarks"),
            created_at=now,
            updated_at=now,
        )
        try:
            self.db.add(document)
            self.db.commit()
            self.db.refresh(document)
        except IntegrityError as exc:
            self.db.rollback()
            raise ValueError("Attendance already marked for this student and date") from exc

        return self._to_response(document, student)

    def list(
        self,
        *,
        page: int,
        page_size: int,
        enrollment_number: str | None,
        attendance_date: date | None,
        status: str | None,
    ):
        base_query = self.db.query(Attendance, Student).join(Student, Student.id == Attendance.student_id)

        if enrollment_number:
            base_query = base_query.filter(Student.enrollment_number == enrollment_number.upper())
        if attendance_date:
            base_query = base_query.filter(Attendance.attendance_date == attendance_date)
        if status:
            base_query = base_query.filter(func.lower(Attendance.status) == status.lower())

        total = base_query.count()
        items_raw = (
            base_query.order_by(Attendance.attendance_date.desc(), Attendance.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        items = [self._to_response(attendance, student) for attendance, student in items_raw]
        return {"page": page, "page_size": page_size, "total": total, "items": items}

    def get_by_id(self, attendance_id: int):
        result = (
            self.db.query(Attendance, Student)
            .join(Student, Student.id == Attendance.student_id)
            .filter(Attendance.id == attendance_id)
            .first()
        )
        if not result:
            return None

        attendance, student = result
        return self._to_response(attendance, student)

    def update(self, attendance_id: int, payload):
        attendance = self.db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not attendance:
            return None

        attendance.attendance_date = payload["attendance_date"]
        attendance.status = payload["status"]
        attendance.remarks = payload.get("remarks")
        attendance.updated_at = datetime.now(timezone.utc)

        try:
            self.db.commit()
            self.db.refresh(attendance)
        except IntegrityError as exc:
            self.db.rollback()
            raise ValueError("Attendance already marked for this student and date") from exc

        student = self.db.query(Student).filter(Student.id == attendance.student_id).first()
        return self._to_response(attendance, student)

    def delete(self, attendance_id: int) -> bool:
        attendance = self.db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not attendance:
            return False

        self.db.delete(attendance)
        self.db.commit()
        return True

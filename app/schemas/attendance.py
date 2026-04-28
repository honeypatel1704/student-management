from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

AttendanceStatus = Literal["present", "absent", "late", "excused"]


class AttendanceCreateRequest(BaseModel):
    enrollment_number: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9\-_/]+$")
    attendance_date: date
    status: AttendanceStatus
    remarks: str | None = Field(default=None, max_length=300)


class AttendanceUpdateRequest(BaseModel):
    attendance_date: date
    status: AttendanceStatus
    remarks: str | None = Field(default=None, max_length=300)


class AttendanceResponse(BaseModel):
    id: str
    student_id: str
    enrollment_number: str
    student_name: str
    attendance_date: date
    status: AttendanceStatus
    remarks: str | None = None
    created_at: datetime
    updated_at: datetime


class AttendanceListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[AttendanceResponse]

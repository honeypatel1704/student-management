from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.schemas.attendance import (
    AttendanceCreateRequest,
    AttendanceListResponse,
    AttendanceResponse,
    AttendanceUpdateRequest,
)
from app.services.attendance_service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.post("", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def mark_attendance(
    payload: AttendanceCreateRequest,
    _admin=Depends(require_roles("admin", "user")),
    db: Session = Depends(get_db),
):
    service = AttendanceService(db)
    try:
        return service.create(payload.model_dump(mode="json"))
    except LookupError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("", response_model=AttendanceListResponse)
def list_attendance(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    enrollment_number: str | None = None,
    attendance_date: date | None = None,
    attendance_status: str | None = Query(default=None, alias="status"),
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AttendanceService(db)
    return service.list(
        page=page,
        page_size=page_size,
        enrollment_number=enrollment_number,
        attendance_date=attendance_date,
        status=attendance_status,
    )


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance(attendance_id: int, _user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = AttendanceService(db)
    attendance = service.get_by_id(attendance_id)
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    return attendance


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    payload: AttendanceUpdateRequest,
    _admin=Depends(require_roles("admin", "user")),
    db: Session = Depends(get_db),
):
    service = AttendanceService(db)
    try:
        attendance = service.update(attendance_id, payload.model_dump(mode="json"))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    return attendance


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(
    attendance_id: int,
    _admin=Depends(require_roles("admin", "user")),
    db: Session = Depends(get_db),
):
    service = AttendanceService(db)
    is_deleted = service.delete(attendance_id)
    if not is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendance record not found")
    return None

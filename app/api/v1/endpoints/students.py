from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.schemas.student import (
    StudentCreateRequest,
    StudentListResponse,
    StudentResponse,
    StudentUpdateRequest,
)
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreateRequest,
    _admin=Depends(require_roles("admin", "user")),
    db: Session = Depends(get_db),
):
    service = StudentService(db)
    try:
        return service.create(payload.model_dump(by_alias=False, mode="json"))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("", response_model=StudentListResponse)
def list_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    q: str | None = None,
    class_name: str | None = Query(default=None, alias="class"),
    batch: str | None = None,
    _user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = StudentService(db)
    return service.list(page=page, page_size=page_size, q=q, class_name=class_name, batch=batch)


@router.get("/{enrollment_number}", response_model=StudentResponse)
def get_student(enrollment_number: str, _user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = StudentService(db)
    student = service.get_by_enrollment(enrollment_number)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.put("/{enrollment_number}", response_model=StudentResponse)
def update_student(
    enrollment_number: str,
    payload: StudentUpdateRequest,
    _admin=Depends(require_roles("admin", "user")),
    db: Session = Depends(get_db),
):
    service = StudentService(db)
    student = service.update(enrollment_number, payload.model_dump(by_alias=False, mode="json"))
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.delete("/{enrollment_number}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(enrollment_number: str, _admin=Depends(require_roles("admin")), db: Session = Depends(get_db)):
    service = StudentService(db)
    is_deleted = service.delete(enrollment_number)
    if not is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return None

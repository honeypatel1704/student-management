import logging
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.dependencies.auth import require_roles
from app.schemas.agent import AgentEventRequest, AgentQueryRequest
from app.services.student_service import StudentService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/query")
def agent_query(
    payload: AgentQueryRequest,
    _agent=Depends(require_roles("admin", "agent")),
    db: Session = Depends(get_db),
):
    service = StudentService(db)

    if payload.action == "list_students":
        page = int(payload.payload.get("page", 1))
        page_size = int(payload.payload.get("page_size", 10))
        q = payload.payload.get("q")
        class_name = payload.payload.get("class")
        batch = payload.payload.get("batch")
        return service.list(page=page, page_size=page_size, q=q, class_name=class_name, batch=batch)

    if payload.action == "get_student":
        enrollment_number = str(payload.payload.get("enrollment_number", "")).strip()
        student = service.get_by_enrollment(enrollment_number)
        return {"found": bool(student), "student": student}

    return service.stats()


@router.post("/hooks/event")
def record_agent_event(payload: AgentEventRequest, _agent=Depends(require_roles("admin", "agent"))):
    now = datetime.now(timezone.utc).isoformat()
    logger.info("Agent event received | type=%s source=%s", payload.event_type, payload.source)
    return {
        "accepted": True,
        "received_at": now,
        "event_type": payload.event_type,
        "source": payload.source,
    }

from typing import Any, Literal

from pydantic import BaseModel, Field


class AgentQueryRequest(BaseModel):
    action: Literal["list_students", "get_student", "stats"]
    payload: dict[str, Any] = Field(default_factory=dict)


class AgentEventRequest(BaseModel):
    event_type: str = Field(min_length=2, max_length=80)
    source: str = Field(min_length=2, max_length=80)
    payload: dict[str, Any] = Field(default_factory=dict)

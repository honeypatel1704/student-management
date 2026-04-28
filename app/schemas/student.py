from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class StudentBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(min_length=2, max_length=120)
    father_name: str = Field(min_length=2, max_length=120)
    mother_name: str = Field(min_length=2, max_length=120)
    birthdate: date
    address: str = Field(min_length=5, max_length=300)
    student_phone: str = Field(pattern=r"^[0-9+\-\s]{8,15}$")
    father_phone: str = Field(pattern=r"^[0-9+\-\s]{8,15}$")
    enrollment_number: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9\-_/]+$")
    class_name: str = Field(alias="class", min_length=1, max_length=30)
    batch: str = Field(min_length=1, max_length=30)
    email: EmailStr
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None


class StudentCreateRequest(StudentBase):
    pass


class StudentUpdateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(min_length=2, max_length=120)
    father_name: str = Field(min_length=2, max_length=120)
    mother_name: str = Field(min_length=2, max_length=120)
    birthdate: date
    address: str = Field(min_length=5, max_length=300)
    student_phone: str = Field(pattern=r"^[0-9+\-\s]{8,15}$")
    father_phone: str = Field(pattern=r"^[0-9+\-\s]{8,15}$")
    class_name: str = Field(alias="class", min_length=1, max_length=30)
    batch: str = Field(min_length=1, max_length=30)
    email: EmailStr
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None


class StudentResponse(BaseModel):
    id: str
    name: str
    father_name: str
    mother_name: str
    birthdate: date
    address: str
    student_phone: str
    father_phone: str
    enrollment_number: str
    class_name: str
    batch: str
    email: EmailStr
    linkedin: Optional[str] = None
    github: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class StudentListResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[StudentResponse]

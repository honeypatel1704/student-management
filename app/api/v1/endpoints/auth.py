from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.db.postgres import get_db
from app.dependencies.auth import get_current_user, require_roles
from app.schemas.auth import LoginRequest, TokenResponse, UserCreateRequest, UserResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.authenticate(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.email, role=user.role)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.post("/users", response_model=UserResponse)
def create_user(payload: UserCreateRequest, _admin=Depends(require_roles("admin")), db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        user = service.create_user(
            name=payload.name,
            email=str(payload.email),
            password=payload.password,
            role=payload.role,
        )
    except IntegrityError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists") from exc

    return UserResponse.model_validate(user)

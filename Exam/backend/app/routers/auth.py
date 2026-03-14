from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.schemas import FaceLoginRequest, LoginRequest, RegisterRequest, TokenResponse
from backend.app.services.auth_service import login_user, login_with_face, register_user

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    try:
        result = register_user(db, payload)
        return TokenResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    result = login_user(db, payload.email, payload.password)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    return TokenResponse(**result)


@router.post("/face-login", response_model=TokenResponse)
def face_login(payload: FaceLoginRequest, db: Session = Depends(get_db)):
    result = login_with_face(db, payload.email, payload.password, payload.face_image)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Face verification failed.")
    return TokenResponse(**result)

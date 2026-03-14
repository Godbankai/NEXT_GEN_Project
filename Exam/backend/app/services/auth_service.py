from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token, hash_password, verify_password
from backend.app.models.db_models import User
from backend.app.services.face_service import FaceValidationError, compare_face_encoding, extract_face_encoding
from backend.app.services.file_service import save_base64_file


def serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "profile_image_path": user.profile_image_path,
    }


def register_user(db: Session, payload) -> dict:
    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise ValueError("User already exists with this email.")

    face_encoding = None
    profile_image_path = None
    if payload.face_image:
        try:
            face_encoding = extract_face_encoding(payload.face_image, require_single_face=True)
            profile_image_path = save_base64_file(payload.face_image, "profiles", ".jpg")
        except FaceValidationError as exc:
            raise ValueError(str(exc)) from exc

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        role=payload.role,
        hashed_password=hash_password(payload.password),
        face_encoding=face_encoding,
        profile_image_path=profile_image_path,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "access_token": create_access_token(str(user.id), user.role),
        "user": serialize_user(user),
    }


def login_user(db: Session, email: str, password: str) -> dict | None:
    user = db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(password, user.hashed_password):
        return None
    return {"access_token": create_access_token(str(user.id), user.role), "user": serialize_user(user)}


def login_with_face(db: Session, email: str, password: str, face_image: str) -> dict | None:
    user = db.scalar(select(User).where(User.email == email))
    if not user or not verify_password(password, user.hashed_password):
        return None
    try:
        matched = compare_face_encoding(user.face_encoding, face_image)
    except FaceValidationError:
        return None
    if not matched:
        return None
    return {"access_token": create_access_token(str(user.id), user.role), "user": serialize_user(user)}

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict[str, Any]


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6)
    role: str = Field(default="student")
    face_image: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class FaceLoginRequest(BaseModel):
    email: EmailStr
    password: str
    face_image: str


class ExamCreateRequest(BaseModel):
    title: str
    subject: str
    description: str
    duration_minutes: int = 30
    instructions: str = ""
    questions: list[dict[str, Any]]
    status: str = "published"


class SessionStartRequest(BaseModel):
    exam_id: int


class SessionSubmitRequest(BaseModel):
    answers: dict[str, Any]


class FrameAnalysisRequest(BaseModel):
    session_id: int
    frame_data: str
    browser_visibility: str = "visible"
    tab_switch_count: int = 0
    active_app: str | None = None


class AudioAnalysisRequest(BaseModel):
    session_id: int
    level: float
    speaking_detected: bool = False


class EventLogRequest(BaseModel):
    session_id: int
    event_type: str
    severity: str = "medium"
    message: str
    screenshot_data: str | None = None
    meta: dict[str, Any] | None = None


class VideoUploadRequest(BaseModel):
    session_id: int
    mime_type: str = "video/webm"
    video_data: str


class SessionActionRequest(BaseModel):
    reason: str | None = None


class ChatMessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    profile_image_path: str | None = None

    class Config:
        from_attributes = True


class EventResponse(BaseModel):
    id: int
    event_type: str
    severity: str
    message: str
    evidence_path: str | None
    created_at: datetime

    class Config:
        from_attributes = True

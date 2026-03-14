from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(20), default="student")
    hashed_password: Mapped[str] = mapped_column(String(255))
    face_encoding: Mapped[str | None] = mapped_column(Text, nullable=True)
    profile_image_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    exams_created = relationship("Exam", back_populates="created_by_user")
    sessions = relationship("ExamSession", back_populates="student")
    messages = relationship("ChatMessage", back_populates="sender")


class Exam(TimestampMixin, Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    subject: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30)
    instructions: Mapped[str] = mapped_column(Text, default="")
    questions_json: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    join_code: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    created_by_user = relationship("User", back_populates="exams_created")
    sessions = relationship("ExamSession", back_populates="exam")


class ExamSession(TimestampMixin, Base):
    __tablename__ = "exam_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(20), default="scheduled")
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    answers_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    suspicious_score: Mapped[int] = mapped_column(Integer, default=0)
    warning_count: Mapped[int] = mapped_column(Integer, default=0)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    lock_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    session_video_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    latest_snapshot_path: Mapped[str | None] = mapped_column(String(255), nullable=True)

    exam = relationship("Exam", back_populates="sessions")
    student = relationship("User", back_populates="sessions")
    events = relationship("ProctorEvent", back_populates="session", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ProctorEvent(TimestampMixin, Base):
    __tablename__ = "proctor_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("exam_sessions.id"))
    event_type: Mapped[str] = mapped_column(String(50))
    severity: Mapped[str] = mapped_column(String(20), default="low")
    message: Mapped[str] = mapped_column(Text)
    evidence_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    session = relationship("ExamSession", back_populates="events")


class ChatMessage(TimestampMixin, Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("exam_sessions.id"), index=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    sender_role: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(Text)

    session = relationship("ExamSession", back_populates="messages")
    sender = relationship("User", back_populates="messages")

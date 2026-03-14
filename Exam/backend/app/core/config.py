import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / ".env")


class Settings:
    def __init__(self) -> None:
        self.base_dir = BASE_DIR
        self.app_name = os.getenv("APP_NAME", "AI Smart Exam Monitoring")
        self.app_env = os.getenv("APP_ENV", "development")
        self.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))
        self.database_url = os.getenv("DATABASE_URL", f"sqlite:///{(BASE_DIR / 'smart_exam.db').as_posix()}")
        media_root_value = os.getenv("MEDIA_ROOT", "storage")
        self.media_root = str((BASE_DIR / media_root_value).resolve()) if not Path(media_root_value).is_absolute() else media_root_value
        self.session_recordings_dir = os.getenv("SESSION_RECORDINGS_DIR", "session_recordings")
        self.evidence_dir = os.getenv("EVIDENCE_DIR", "evidence")
        self.default_admin_email = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@example.com")
        self.default_admin_password = os.getenv("DEFAULT_ADMIN_PASSWORD", "Admin@123")
        self.default_admin_name = os.getenv("DEFAULT_ADMIN_NAME", "Chief Admin")


settings = Settings()

Path(settings.media_root).mkdir(parents=True, exist_ok=True)
Path(settings.media_root, settings.session_recordings_dir).mkdir(parents=True, exist_ok=True)
Path(settings.media_root, settings.evidence_dir).mkdir(parents=True, exist_ok=True)

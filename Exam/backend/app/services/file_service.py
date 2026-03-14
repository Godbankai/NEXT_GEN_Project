import base64
import uuid
from pathlib import Path

from backend.app.core.config import settings


def save_base64_file(data_url: str, folder: str, suffix: str) -> str:
    _, encoded = data_url.split(",", 1)
    file_bytes = base64.b64decode(encoded)
    target_dir = Path(settings.media_root) / folder
    target_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"{uuid.uuid4().hex}{suffix}"
    file_path = target_dir / file_name
    file_path.write_bytes(file_bytes)
    return str(file_path).replace("\\", "/")


def public_path(file_path: str | None) -> str | None:
    if not file_path:
        return None
    cleaned = file_path.replace("\\", "/")
    media_root = settings.media_root.replace("\\", "/")
    if cleaned.startswith(media_root):
        return "/" + cleaned
    return cleaned

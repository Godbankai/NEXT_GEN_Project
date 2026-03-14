import base64
import json

import cv2
import numpy as np

try:
    import face_recognition
except Exception:
    face_recognition = None


class FaceValidationError(ValueError):
    pass


def decode_image(data_url: str) -> np.ndarray:
    _, encoded = data_url.split(",", 1)
    image_bytes = np.frombuffer(base64.b64decode(encoded), dtype=np.uint8)
    frame = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
    return frame


def detect_face_count(frame: np.ndarray) -> int:
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    if face_recognition:
        return len(face_recognition.face_locations(rgb, model="hog"))
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return len(cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(90, 90)))


def validate_single_face(data_url: str) -> np.ndarray:
    frame = decode_image(data_url)
    face_count = detect_face_count(frame)
    if face_count == 0:
        raise FaceValidationError("No clear face detected. Please face the camera directly.")
    if face_count > 1:
        raise FaceValidationError("Multiple faces detected. Ensure only one person is visible.")
    return frame


def extract_face_encoding(data_url: str, require_single_face: bool = True) -> str | None:
    frame = validate_single_face(data_url) if require_single_face else decode_image(data_url)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if face_recognition:
        encodings = face_recognition.face_encodings(rgb)
        if encodings:
            return json.dumps(encodings[0].tolist())

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (64, 64)).flatten().astype("float32") / 255.0
    return json.dumps(resized.tolist())


def compare_face_encoding(stored_encoding: str | None, probe_data_url: str, tolerance: float = 0.48) -> bool:
    if not stored_encoding:
        return False

    probe = extract_face_encoding(probe_data_url, require_single_face=True)
    if not probe:
        return False

    stored = np.array(json.loads(stored_encoding))
    probe_array = np.array(json.loads(probe))

    if stored.shape != probe_array.shape:
        return False

    distance = np.linalg.norm(stored - probe_array)
    if len(stored) == 128:
        return bool(distance <= tolerance)
    return bool(distance <= 18.0)

const registerForm = document.getElementById("registerForm");
const registerStatus = document.getElementById("registerStatus");
const registerCameraBtn = document.getElementById("registerCameraBtn");
const captureRegisterBtn = document.getElementById("captureRegisterBtn");
const registerVideo = document.getElementById("registerVideo");
const registerCanvas = document.getElementById("registerCanvas");
const faceCaptureStatus = document.getElementById("faceCaptureStatus");
let registerFaceImage = null;

async function redirectAfterRegister() {
  if (window.JOIN_CODE) {
    const join = await SmartExam.request(`/api/exams/join/${window.JOIN_CODE}`);
    window.location.href = join.exam_url;
    return;
  }
  window.location.href = "/dashboard";
}

registerCameraBtn?.addEventListener("click", async () => {
  try {
    await SmartExam.startCamera(registerVideo);
    captureRegisterBtn.classList.remove("hidden");
    SmartExam.status(faceCaptureStatus, "Camera ready. Capture your face image.", "success");
  } catch (error) {
    SmartExam.status(faceCaptureStatus, error.message, "error");
  }
});

captureRegisterBtn?.addEventListener("click", () => {
  registerFaceImage = SmartExam.captureFrame(registerVideo, registerCanvas);
  SmartExam.status(faceCaptureStatus, "Face template captured successfully.", "success");
});

registerForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!registerFaceImage) {
    SmartExam.status(registerStatus, "Capture a clear face image before registering.", "error");
    return;
  }
  const formData = new FormData(registerForm);
  try {
    const data = await SmartExam.request("/api/auth/register", { method: "POST", body: JSON.stringify({ full_name: formData.get("full_name"), email: formData.get("email"), password: formData.get("password"), role: formData.get("role"), face_image: registerFaceImage }) });
    SmartExam.setSession(data.access_token, data.user);
    await redirectAfterRegister();
  } catch (error) {
    SmartExam.status(registerStatus, error.message, "error");
  }
});

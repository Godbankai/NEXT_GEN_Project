const loginForm = document.getElementById("loginForm");
const loginStatus = document.getElementById("loginStatus");
const startCameraBtn = document.getElementById("startCameraBtn");
const faceLoginBtn = document.getElementById("faceLoginBtn");
const authVideo = document.getElementById("authVideo");
const authCanvas = document.getElementById("authCanvas");

async function redirectAfterAuth() {
  if (window.JOIN_CODE) {
    const join = await SmartExam.request(`/api/exams/join/${window.JOIN_CODE}`);
    window.location.href = join.exam_url;
    return;
  }
  window.location.href = "/dashboard";
}

startCameraBtn?.addEventListener("click", async () => {
  try {
    await SmartExam.startCamera(authVideo);
    faceLoginBtn.classList.remove("hidden");
    SmartExam.status(loginStatus, "Camera started. You can now use face login.", "success");
  } catch (error) {
    SmartExam.status(loginStatus, error.message, "error");
  }
});

loginForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(loginForm);
  try {
    const data = await SmartExam.request("/api/auth/login", { method: "POST", body: JSON.stringify({ email: formData.get("email"), password: formData.get("password") }) });
    SmartExam.setSession(data.access_token, data.user);
    await redirectAfterAuth();
  } catch (error) {
    SmartExam.status(loginStatus, error.message, "error");
  }
});

faceLoginBtn?.addEventListener("click", async () => {
  const formData = new FormData(loginForm);
  try {
    const faceImage = SmartExam.captureFrame(authVideo, authCanvas);
    const data = await SmartExam.request("/api/auth/face-login", { method: "POST", body: JSON.stringify({ email: formData.get("email"), password: formData.get("password"), face_image: faceImage }) });
    SmartExam.setSession(data.access_token, data.user);
    await redirectAfterAuth();
  } catch (error) {
    SmartExam.status(loginStatus, error.message, "error");
  }
});

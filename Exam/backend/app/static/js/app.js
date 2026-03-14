const SmartExam = {
  apiBase: "",
  get token() {
    return localStorage.getItem("smart_exam_token");
  },
  setSession(token, user) {
    localStorage.setItem("smart_exam_token", token);
    localStorage.setItem("smart_exam_user", JSON.stringify(user));
  },
  clearSession() {
    localStorage.removeItem("smart_exam_token");
    localStorage.removeItem("smart_exam_user");
  },
  getUser() {
    const raw = localStorage.getItem("smart_exam_user");
    return raw ? JSON.parse(raw) : null;
  },
  extractErrorMessage(payload) {
    if (!payload) return "Request failed";
    if (typeof payload.detail === "string") return payload.detail;
    if (Array.isArray(payload.detail) && payload.detail.length) {
      return payload.detail.map((item) => item.msg || item.message || JSON.stringify(item)).join(" | ");
    }
    if (typeof payload.message === "string") return payload.message;
    return "Request failed";
  },
  async request(path, options = {}) {
    const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
    if (SmartExam.token) {
      headers.Authorization = `Bearer ${SmartExam.token}`;
    }
    const response = await fetch(`${SmartExam.apiBase}${path}`, { ...options, headers });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(SmartExam.extractErrorMessage(payload));
    }
    return payload;
  },
  status(el, message, kind = "info") {
    if (!el) return;
    el.textContent = message;
    el.className = `mt-4 text-sm font-medium ${kind === "error" ? "text-rose-600" : kind === "success" ? "text-emerald-700" : "text-slate-600"}`;
  },
  async startCamera(videoEl) {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    videoEl.srcObject = stream;
    videoEl.classList.remove("hidden");
    return stream;
  },
  captureFrame(videoEl, canvasEl) {
    canvasEl.width = videoEl.videoWidth || 640;
    canvasEl.height = videoEl.videoHeight || 480;
    const ctx = canvasEl.getContext("2d");
    ctx.drawImage(videoEl, 0, 0, canvasEl.width, canvasEl.height);
    return canvasEl.toDataURL("image/jpeg", 0.85);
  },
  stopStream(stream) {
    if (!stream) return;
    stream.getTracks().forEach((track) => track.stop());
  }
};

const currentUser = SmartExam.getUser();
if (!currentUser || currentUser.role !== "student") window.location.href = "/";

const examTitle = document.getElementById("examTitle");
const examDescription = document.getElementById("examDescription");
const examInstructions = document.getElementById("examInstructions");
const examForm = document.getElementById("examForm");
const examStatus = document.getElementById("examStatus");
const examVideo = document.getElementById("examVideo");
const examCanvas = document.getElementById("examCanvas");
const submitExamBtn = document.getElementById("submitExamBtn");
const panicSaveBtn = document.getElementById("panicSaveBtn");
const countdown = document.getElementById("countdown");
const faceCountEl = document.getElementById("faceCount");
const attentionScoreEl = document.getElementById("attentionScore");
const alertFeed = document.getElementById("alertFeed");
const riskBadge = document.getElementById("riskBadge");
const lockBanner = document.getElementById("lockBanner");
const chatMessages = document.getElementById("chatMessages");
const chatInput = document.getElementById("chatInput");
const sendChatBtn = document.getElementById("sendChatBtn");

let examData = null;
let sessionId = null;
let videoStream = null;
let recorder = null;
let recordedChunks = [];
let tabSwitchCount = 0;
let remainingSeconds = 0;
let countdownInterval = null;
let proctorInterval = null;
let audioInterval = null;
let statusInterval = null;
let chatInterval = null;
let cumulativeRisk = 0;
let locked = false;

async function initExamRoom() {
  await enterFullscreen();
  await loadExam();
  await startMedia();
  await startSession();
  if (locked) return;
  renderQuestions();
  restoreAnswers();
  startCountdown();
  startLockdown();
  startMonitoring();
  statusInterval = setInterval(checkSessionStatus, 4000);
  chatInterval = setInterval(loadChat, 5000);
  await loadChat();
}

async function loadExam() {
  const response = await SmartExam.request(`/api/exams/${window.EXAM_ID}`);
  examData = response.item;
  examTitle.textContent = examData.title;
  examDescription.textContent = `${examData.description} | Join code: ${examData.join_code}`;
  examInstructions.textContent = examData.instructions || "No additional instructions.";
  remainingSeconds = examData.duration_minutes * 60;
}

function renderQuestions() {
  examForm.innerHTML = examData.questions.map((question, index) => {
    const name = `q-${question.id}`;
    if (question.type === "mcq") {
      return `<section class="rounded-3xl border border-slate-200 p-5"><p class="text-sm font-semibold uppercase tracking-[0.25em] text-slate-500">Question ${index + 1}</p><h3 class="mt-2 text-lg font-bold text-ink">${question.question}</h3><div class="mt-4 space-y-3">${question.options.map((option) => `<label class="flex items-center gap-3 rounded-2xl bg-slate-50 px-4 py-3"><input type="radio" name="${name}" value="${option}"><span>${option}</span></label>`).join("")}</div></section>`;
    }
    return `<section class="rounded-3xl border border-slate-200 p-5"><p class="text-sm font-semibold uppercase tracking-[0.25em] text-slate-500">Question ${index + 1}</p><h3 class="mt-2 text-lg font-bold text-ink">${question.question}</h3><textarea name="${name}" rows="4" class="mt-4 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3"></textarea></section>`;
  }).join("");
}

function restoreAnswers() {
  const saved = JSON.parse(localStorage.getItem(`smart_exam_answers_${window.EXAM_ID}`) || "{}");
  Object.entries(saved).forEach(([questionId, value]) => {
    const radio = examForm.querySelector(`[name="q-${questionId}"][value="${value}"]`);
    const text = examForm.querySelector(`[name="q-${questionId}"]`);
    if (radio) radio.checked = true;
    else if (text) text.value = value;
  });
}

async function startMedia() {
  videoStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
  examVideo.srcObject = videoStream;
  recorder = new MediaRecorder(videoStream, { mimeType: "video/webm" });
  recorder.ondataavailable = (event) => { if (event.data.size > 0) recordedChunks.push(event.data); };
  recorder.start(3000);
}

async function startSession() {
  const response = await SmartExam.request("/api/exams/sessions/start", { method: "POST", body: JSON.stringify({ exam_id: window.EXAM_ID }) });
  sessionId = response.session_id;
  if (response.is_locked) await forceAutoSubmit(response.lock_reason || "Your exam has been stopped.");
}

function startCountdown() {
  countdownInterval = setInterval(() => {
    remainingSeconds -= 1;
    countdown.textContent = `${String(Math.max(0, Math.floor(remainingSeconds / 60))).padStart(2, "0")}:${String(Math.max(0, remainingSeconds % 60)).padStart(2, "0")}`;
    if (remainingSeconds <= 0) {
      clearInterval(countdownInterval);
      submitExam();
    }
  }, 1000);
}

function startLockdown() {
  document.addEventListener("contextmenu", (event) => event.preventDefault());
  document.addEventListener("copy", (event) => event.preventDefault());
  document.addEventListener("paste", (event) => event.preventDefault());
  document.addEventListener("cut", (event) => event.preventDefault());
  document.addEventListener("keydown", async (event) => {
    const blocked = ["F12", "Tab"];
    if (blocked.includes(event.key) || (event.ctrlKey && ["c", "v", "x", "u", "s"].includes(event.key.toLowerCase()))) {
      event.preventDefault();
      await logBrowserEvent("keyboard_block", `Blocked key combination: ${event.key}`, "medium");
    }
  });
  document.addEventListener("visibilitychange", async () => {
    if (document.hidden) {
      tabSwitchCount += 1;
      await logBrowserEvent("tab_switch", "Student switched tab or minimized exam window.", "high", true);
    }
  });
  document.addEventListener("fullscreenchange", async () => {
    if (!document.fullscreenElement) {
      await logBrowserEvent("fullscreen_exit", "Student exited fullscreen mode.", "high", true);
      enterFullscreen().catch(() => {});
    }
  });
  examForm.addEventListener("input", persistAnswers);
}

async function enterFullscreen() {
  const root = document.documentElement;
  if (root.requestFullscreen && !document.fullscreenElement) await root.requestFullscreen();
}

function startMonitoring() {
  proctorInterval = setInterval(analyzeFrame, 5000);
  audioInterval = setInterval(analyzeAudio, 4000);
}

async function analyzeFrame() {
  if (!sessionId || locked) return;
  const frame = SmartExam.captureFrame(examVideo, examCanvas);
  try {
    const result = await SmartExam.request("/api/proctor/analyze-frame", { method: "POST", body: JSON.stringify({ session_id: sessionId, frame_data: frame, browser_visibility: document.hidden ? "hidden" : "visible", tab_switch_count: tabSwitchCount, active_app: document.visibilityState }) });
    if (result.session_locked) return forceAutoSubmit(result.lock_reason);
    faceCountEl.textContent = result.face_count;
    attentionScoreEl.textContent = `${Math.round((result.attention_score || 0) * 100)}%`;
    cumulativeRisk += Number(result.suspicious_points || 0);
    updateRisk(cumulativeRisk);
    if (result.alerts.length) {
      alertFeed.innerHTML = result.alerts.map((alert) => `<div class="rounded-2xl bg-rose-50 p-3 text-rose-700"><p class="font-semibold uppercase tracking-[0.2em]">${alert.event_type}</p><p class="mt-1">${alert.message}</p></div>`).join("") + alertFeed.innerHTML;
    }
  } catch (error) { SmartExam.status(examStatus, error.message, "error"); }
}

async function analyzeAudio() {
  if (!videoStream || !sessionId || locked) return;
  const audioCtx = new AudioContext();
  const source = audioCtx.createMediaStreamSource(videoStream);
  const analyser = audioCtx.createAnalyser();
  source.connect(analyser);
  const dataArray = new Uint8Array(analyser.frequencyBinCount);
  analyser.getByteFrequencyData(dataArray);
  const avg = dataArray.reduce((sum, value) => sum + value, 0) / Math.max(dataArray.length, 1);
  const level = avg / 255;
  try {
    const result = await SmartExam.request("/api/proctor/analyze-audio", { method: "POST", body: JSON.stringify({ session_id: sessionId, level, speaking_detected: level > 0.18 }) });
    if (result.session_locked) return forceAutoSubmit(result.lock_reason);
    if (result.alerts.length) {
      cumulativeRisk += 10;
      updateRisk(cumulativeRisk);
      alertFeed.innerHTML = result.alerts.map((alert) => `<div class="rounded-2xl bg-amber-50 p-3 text-amber-700"><p class="font-semibold uppercase tracking-[0.2em]">${alert.event_type}</p><p class="mt-1">${alert.message}</p></div>`).join("") + alertFeed.innerHTML;
    }
  } finally { audioCtx.close(); }
}

async function logBrowserEvent(eventType, message, severity = "medium", includeShot = false) {
  if (!sessionId || locked) return;
  const screenshot = includeShot ? SmartExam.captureFrame(examVideo, examCanvas) : null;
  const result = await SmartExam.request("/api/proctor/event", { method: "POST", body: JSON.stringify({ session_id: sessionId, event_type: eventType, severity, message, screenshot_data: screenshot, meta: { tab_switch_count: tabSwitchCount } }) });
  if (result.session_locked) return forceAutoSubmit(result.lock_reason);
  cumulativeRisk += severity === "high" ? 20 : severity === "medium" ? 12 : 5;
  updateRisk(cumulativeRisk);
}

function collectAnswers() {
  const payload = {};
  examData.questions.forEach((question) => {
    const name = `q-${question.id}`;
    const input = examForm.querySelector(`[name="${name}"]:checked`) || examForm.querySelector(`[name="${name}"]`);
    payload[String(question.id)] = input ? input.value : "";
  });
  return payload;
}

function persistAnswers() { localStorage.setItem(`smart_exam_answers_${window.EXAM_ID}`, JSON.stringify(collectAnswers())); }

panicSaveBtn?.addEventListener("click", () => { persistAnswers(); SmartExam.status(examStatus, "Answers saved locally on this browser.", "success"); });
submitExamBtn?.addEventListener("click", submitExam);
sendChatBtn?.addEventListener("click", sendChatMessage);

async function uploadRecording() {
  if (!recorder) return;
  return new Promise((resolve) => {
    recorder.onstop = async () => {
      const blob = new Blob(recordedChunks, { type: "video/webm" });
      const reader = new FileReader();
      reader.onloadend = async () => {
        await SmartExam.request("/api/proctor/upload-session-video", { method: "POST", body: JSON.stringify({ session_id: sessionId, mime_type: "video/webm", video_data: reader.result }) });
        resolve();
      };
      reader.readAsDataURL(blob);
    };
    recorder.stop();
  });
}

async function submitExam(force = false) {
  if (!sessionId || (locked && !force)) return;
  clearTimers();
  persistAnswers();
  try {
    await uploadRecording();
    const result = await SmartExam.request(`/api/exams/sessions/${sessionId}/submit`, { method: "POST", body: JSON.stringify({ answers: collectAnswers() }) });
    localStorage.removeItem(`smart_exam_answers_${window.EXAM_ID}`);
    SmartExam.status(examStatus, `Exam submitted successfully. Score: ${result.score ?? "Pending evaluation"}%`, "success");
    SmartExam.stopStream(videoStream);
    setTimeout(() => { window.location.href = "/dashboard"; }, 3000);
  } catch (error) { SmartExam.status(examStatus, error.message, "error"); }
}

async function checkSessionStatus() {
  if (!sessionId || locked) return;
  const status = await SmartExam.request(`/api/exams/sessions/${sessionId}/status`);
  if (status.is_locked) handleLock(status.lock_reason);
}

async function loadChat() {
  if (!sessionId) return;
  const data = await SmartExam.request(`/api/exams/sessions/${sessionId}/chat`);
  chatMessages.innerHTML = data.items.map((item) => `<div class="rounded-2xl ${item.sender_role === 'admin' ? 'bg-amber-50 text-amber-900' : 'bg-slate-100 text-slate-700'} p-3"><p class="font-semibold">${item.sender_name}</p><p class="mt-1">${item.message}</p></div>`).join("") || `<p class="text-slate-500">No messages yet.</p>`;
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendChatMessage() {
  if (!sessionId || !chatInput.value.trim()) return;
  await SmartExam.request(`/api/exams/sessions/${sessionId}/chat`, { method: "POST", body: JSON.stringify({ message: chatInput.value.trim() }) });
  chatInput.value = "";
  await loadChat();
}

async function forceAutoSubmit(reason) {
  if (locked) return;
  locked = true;
  clearTimers();
  lockBanner.textContent = reason || "Exam locked due to suspicious activity.";
  lockBanner.classList.remove("hidden");
  SmartExam.status(examStatus, "Three warnings reached. Your exam is being auto-submitted.", "error");
  try {
    await submitExam(true);
  } catch (error) {
    SmartExam.status(examStatus, error.message, "error");
  }
}


function clearTimers() {
  clearInterval(proctorInterval);
  clearInterval(audioInterval);
  clearInterval(countdownInterval);
  clearInterval(statusInterval);
}

function updateRisk(points) {
  if (points >= 60) {
    riskBadge.textContent = "High";
    riskBadge.className = "rounded-full bg-rose-100 px-3 py-1 text-xs font-bold uppercase tracking-[0.3em] text-rose-700";
  } else if (points >= 20) {
    riskBadge.textContent = "Medium";
    riskBadge.className = "rounded-full bg-amber-100 px-3 py-1 text-xs font-bold uppercase tracking-[0.3em] text-amber-700";
  } else {
    riskBadge.textContent = "Low";
    riskBadge.className = "rounded-full bg-emerald-100 px-3 py-1 text-xs font-bold uppercase tracking-[0.3em] text-emerald-700";
  }
}

window.addEventListener("beforeunload", async (event) => {
  if (sessionId && !locked) {
    event.preventDefault();
    await logBrowserEvent("page_exit_attempt", "Student attempted to leave the exam page.", "high", true);
  }
});

initExamRoom().catch((error) => { SmartExam.status(examStatus, error.message, "error"); });




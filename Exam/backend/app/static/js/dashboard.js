const user = SmartExam.getUser();
const adminPanel = document.getElementById("adminPanel");
const studentPanel = document.getElementById("studentPanel");
const dashboardHeading = document.getElementById("dashboardHeading");
const dashboardSubheading = document.getElementById("dashboardSubheading");
const analyticsCards = document.getElementById("analyticsCards");
const examCreateForm = document.getElementById("examCreateForm");
const examCreateStatus = document.getElementById("examCreateStatus");
const sessionMonitorList = document.getElementById("sessionMonitorList");
const studentExamList = document.getElementById("studentExamList");
const logoutBtn = document.getElementById("logoutBtn");
const loadSampleExamBtn = document.getElementById("loadSampleExamBtn");

if (!user || !SmartExam.token) window.location.href = "/";
logoutBtn?.addEventListener("click", () => { SmartExam.clearSession(); window.location.href = "/"; });

loadSampleExamBtn?.addEventListener("click", () => {
  examCreateForm.title.value = "AI Behaviour Monitoring Test";
  examCreateForm.subject.value = "Artificial Intelligence";
  examCreateForm.duration_minutes.value = 20;
  examCreateForm.description.value = "Sample teacher-created exam for live testing.";
  examCreateForm.instructions.value = "Face the camera, remain in full-screen mode, and use support chat if an issue occurs.";
  examCreateForm.questions_json.value = JSON.stringify([{ id: 1, question: "Which library is used for FastAPI routing?", type: "text", answer: "fastapi" }], null, 2);
});

async function initDashboard() {
  if (user.role === "admin") {
    adminPanel.classList.remove("hidden");
    dashboardHeading.textContent = `Welcome, ${user.full_name}`;
    dashboardSubheading.textContent = "Manage exams, monitor live sessions, resume blocked students, and respond in chat.";
    await Promise.all([loadAnalytics(), loadSessions()]);
    setInterval(loadSessions, 8000);
    examCreateForm?.addEventListener("submit", createExam);
  } else {
    studentPanel.classList.remove("hidden");
    dashboardHeading.textContent = "Student Dashboard";
    dashboardSubheading.textContent = "Use the shared join link or start any published exam below.";
    await loadStudentExams();
  }
}

async function loadAnalytics() {
  const data = await SmartExam.request("/api/admin/analytics");
  analyticsCards.innerHTML = [["Published Exams", data.total_exams, "text-slateblue"], ["Exam Sessions", data.total_sessions, "text-glow"], ["Flagged Events", data.flagged_events, "text-rose-600"], ["Support Chats", data.total_messages, "text-ocean"]].map(([label, value, color]) => `<article class="rounded-[1.75rem] bg-white/85 p-5 shadow-panel"><p class="text-sm text-slate-500">${label}</p><p class="mt-3 text-4xl font-black ${color}">${value}</p></article>`).join("");
}

async function createExam(event) {
  event.preventDefault();
  try {
    const payload = { title: examCreateForm.title.value, subject: examCreateForm.subject.value, description: examCreateForm.description.value, duration_minutes: Number(examCreateForm.duration_minutes.value), instructions: examCreateForm.instructions.value, questions: JSON.parse(examCreateForm.questions_json.value), status: "published" };
    const result = await SmartExam.request("/api/exams", { method: "POST", body: JSON.stringify(payload) });
    SmartExam.status(examCreateStatus, `Exam created. Share link code: ${result.item.join_code}`, "success");
    examCreateForm.reset();
    await Promise.all([loadAnalytics(), loadSessions()]);
  } catch (error) { SmartExam.status(examCreateStatus, error.message, "error"); }
}

async function loadSessions() {
  const data = await SmartExam.request("/api/admin/sessions");
  if (!data.items.length) {
    sessionMonitorList.innerHTML = `<div class="rounded-3xl bg-slate-50 p-5 text-sm text-slate-500">No sessions yet. Students can join via shared links like /join/AI-DEMO-101.</div>`;
    return;
  }
  sessionMonitorList.innerHTML = data.items.map((item) => `<article class="rounded-3xl border border-slate-200 p-4"><div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between"><div><p class="text-sm font-semibold text-ocean">${item.exam_title}</p><h3 class="mt-1 text-xl font-black text-ink">${item.student_name}</h3><p class="mt-2 text-sm text-slate-500">Status: ${item.status} | Risk: ${item.suspicious_score} | Warnings: ${item.warning_count}</p><p class="mt-1 text-sm text-slate-500">Join code: ${item.join_code}</p></div><div class="flex flex-wrap gap-3"><a href="/api/admin/reports/${item.id}.pdf" target="_blank" class="rounded-full bg-ink px-4 py-2 text-sm font-semibold text-white">PDF Report</a><button data-session="${item.id}" class="sessionDetailBtn rounded-full bg-slateblue px-4 py-2 text-sm font-semibold text-white">View</button>${item.is_locked ? `<button data-resume="${item.id}" class="resumeBtn rounded-full bg-emerald-600 px-4 py-2 text-sm font-semibold text-white">Resume Student</button>` : `<button data-stop="${item.id}" class="stopBtn rounded-full bg-rose-600 px-4 py-2 text-sm font-semibold text-white">Stop Exam</button>`}</div></div><div id="detail-${item.id}" class="mt-4 space-y-3 text-sm text-slate-600"></div></article>`).join("");
  document.querySelectorAll(".sessionDetailBtn").forEach((button) => button.addEventListener("click", async () => { const id = button.dataset.session; const detail = await SmartExam.request(`/api/admin/sessions/${id}`); renderAdminDetail(id, detail); }));
  document.querySelectorAll(".resumeBtn").forEach((button) => button.addEventListener("click", async () => { await SmartExam.request(`/api/admin/sessions/${button.dataset.resume}/resume`, { method: "POST", body: JSON.stringify({ reason: "Resumed by admin" }) }); loadSessions(); }));
  document.querySelectorAll(".stopBtn").forEach((button) => button.addEventListener("click", async () => { await SmartExam.request(`/api/admin/sessions/${button.dataset.stop}/stop`, { method: "POST", body: JSON.stringify({ reason: "Stopped by admin due to suspicious activity." }) }); loadSessions(); }));
}

function renderAdminDetail(id, detail) {
  const host = document.getElementById(`detail-${id}`);
  const chatHtml = `<div class="rounded-2xl bg-slate-50 p-4"><p class="font-semibold text-slate-700">Support Chat</p><div class="mt-3 h-40 space-y-2 overflow-y-auto rounded-2xl bg-white p-3">${detail.messages.map((m) => `<div><span class="font-semibold">${m.sender_name}:</span> ${m.message}</div>`).join("") || "<p class='text-slate-500'>No chat yet.</p>"}</div><div class="mt-3 flex gap-2"><input id="admin-chat-${id}" class="flex-1 rounded-2xl border border-slate-200 px-3 py-2" placeholder="Reply to student"><button data-send-admin="${id}" class="rounded-2xl bg-ink px-4 py-2 text-white">Send</button></div></div>`;
  host.innerHTML = `${detail.session.is_locked ? `<div class="rounded-2xl bg-rose-50 p-3 font-semibold text-rose-700">Exam locked: ${detail.session.lock_reason}</div>` : ""}${detail.events.length ? detail.events.map((event) => `<div class="rounded-2xl bg-slate-50 p-3"><p class="font-semibold text-slate-700">${event.event_type} <span class="ml-2 rounded-full bg-slate-200 px-2 py-1 text-xs uppercase">${event.severity}</span></p><p class="mt-1">${event.message}</p>${event.evidence_path ? `<a class="mt-2 inline-block text-ocean underline" href="${event.evidence_path}" target="_blank">Open evidence</a>` : ""}</div>`).join("") : `<p class="text-slate-500">No suspicious events recorded.</p>`}${chatHtml}`;
  host.querySelector(`[data-send-admin="${id}"]`)?.addEventListener("click", async () => { const input = document.getElementById(`admin-chat-${id}`); if (!input.value.trim()) return; await SmartExam.request(`/api/exams/sessions/${id}/chat`, { method: "POST", body: JSON.stringify({ message: input.value.trim() }) }); const updated = await SmartExam.request(`/api/admin/sessions/${id}`); renderAdminDetail(id, updated); });
}

async function loadStudentExams() {
  const data = await SmartExam.request("/api/exams");
  studentExamList.innerHTML = data.items.map((item) => `<article class="rounded-[1.75rem] bg-white p-5 shadow-panel"><p class="text-sm font-semibold uppercase tracking-[0.25em] text-ocean">${item.subject}</p><h3 class="mt-3 text-2xl font-black text-ink">${item.title}</h3><p class="mt-3 text-sm leading-7 text-slate-600">${item.description}</p><p class="mt-3 text-xs font-semibold uppercase tracking-[0.25em] text-slate-500">Join Link: ${window.location.origin}/join/${item.join_code}</p><div class="mt-4 flex items-center justify-between"><span class="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] text-slate-600">${item.duration_minutes} min</span><a href="/exam/${item.id}" class="rounded-full bg-slateblue px-4 py-2 text-sm font-semibold text-white">Start exam</a></div></article>`).join("");
}

initDashboard().catch((error) => { dashboardSubheading.textContent = error.message; });

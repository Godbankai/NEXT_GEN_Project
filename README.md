
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600&display=swap');

  * { box-sizing: border-box; margin: 0; padding: 0; }

  .hero-wrap {
    font-family: 'Rajdhani', sans-serif;
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b3e 40%, #0a1628 70%, #06101e 100%);
    min-height: 100vh;
    padding: 0;
    position: relative;
    overflow: hidden;
  }

  .stars {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none; z-index: 0;
  }
  .star {
    position: absolute; background: #fff; border-radius: 50%;
    animation: twinkle 3s infinite alternate;
  }

  @keyframes twinkle {
    0% { opacity: 0.2; transform: scale(1); }
    100% { opacity: 1; transform: scale(1.4); }
  }

  .scanline {
    position: absolute; width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent);
    animation: scan 6s linear infinite;
    z-index: 1;
  }
  @keyframes scan { from { top: -2px; } to { top: 100%; } }

  .content { position: relative; z-index: 2; padding: 2rem 1.5rem; }

  .badge-row {
    display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 1.2rem;
    justify-content: center;
  }
  .badge {
    font-size: 11px; font-weight: 600; padding: 4px 12px;
    border-radius: 20px; letter-spacing: 0.5px; text-transform: uppercase;
    animation: fadeSlide 0.6s ease forwards; opacity: 0;
  }
  .badge-blue { background: rgba(0,162,255,0.15); color: #00c3ff; border: 1px solid rgba(0,180,255,0.35); animation-delay: 0.2s; }
  .badge-green { background: rgba(0,255,128,0.1); color: #00ff88; border: 1px solid rgba(0,255,128,0.3); animation-delay: 0.4s; }
  .badge-orange { background: rgba(255,150,0,0.1); color: #ffaa00; border: 1px solid rgba(255,150,0,0.3); animation-delay: 0.6s; }

  @keyframes fadeSlide {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }

  .hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 28px; font-weight: 900;
    background: linear-gradient(90deg, #00c3ff, #ffffff, #00ff88);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; line-height: 1.2; margin-bottom: 0.5rem;
    animation: fadeSlide 0.8s 0.1s ease forwards; opacity: 0;
    letter-spacing: 1px;
  }
  .hero-sub {
    text-align: center; color: rgba(180,210,255,0.7); font-size: 14px;
    margin-bottom: 2rem;
    animation: fadeSlide 0.8s 0.3s ease forwards; opacity: 0;
  }

  .monitor-box {
    background: rgba(0,180,255,0.04);
    border: 1px solid rgba(0,180,255,0.2);
    border-radius: 16px;
    padding: 1.25rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    animation: fadeSlide 0.7s ease forwards; opacity: 0;
  }
  .monitor-box::before {
    content: '';
    position: absolute; top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,195,255,0.06), transparent);
    animation: shimmer 4s infinite;
  }
  @keyframes shimmer { 0% { left: -100%; } 100% { left: 200%; } }

  .monitor-box:nth-child(1) { animation-delay: 0.5s; }
  .monitor-box:nth-child(2) { animation-delay: 0.7s; }
  .monitor-box:nth-child(3) { animation-delay: 0.9s; }
  .monitor-box:nth-child(4) { animation-delay: 1.1s; }

  .box-header {
    display: flex; align-items: center; gap: 10px; margin-bottom: 1rem;
  }
  .icon-circle {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
  }
  .ic-blue { background: rgba(0,180,255,0.15); color: #00c3ff; border: 1px solid rgba(0,180,255,0.3); }
  .ic-green { background: rgba(0,255,128,0.1); color: #00ff88; border: 1px solid rgba(0,255,128,0.25); }
  .ic-orange { background: rgba(255,160,0,0.1); color: #ffaa00; border: 1px solid rgba(255,160,0,0.25); }
  .ic-purple { background: rgba(160,80,255,0.1); color: #c080ff; border: 1px solid rgba(160,80,255,0.25); }

  .box-title {
    font-size: 15px; font-weight: 600; color: #e0f0ff; letter-spacing: 0.3px;
  }
  .box-subtitle { font-size: 12px; color: rgba(150,190,230,0.6); }

  .feature-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
  }
  .feat {
    background: rgba(0,140,200,0.07);
    border: 1px solid rgba(0,180,255,0.12);
    border-radius: 10px; padding: 10px 12px;
    display: flex; align-items: flex-start; gap: 8px;
  }
  .feat-dot {
    width: 6px; height: 6px; border-radius: 50%; margin-top: 5px; flex-shrink: 0;
  }
  .dot-blue { background: #00c3ff; box-shadow: 0 0 6px #00c3ff; }
  .dot-green { background: #00ff88; box-shadow: 0 0 6px #00ff88; }
  .dot-orange { background: #ffaa00; box-shadow: 0 0 6px #ffaa00; }
  .dot-purple { background: #c080ff; box-shadow: 0 0 6px #c080ff; }

  .feat-label { font-size: 12px; color: rgba(200,225,255,0.85); line-height: 1.4; }

  .tech-pills {
    display: flex; flex-wrap: wrap; gap: 6px;
  }
  .pill {
    font-size: 11px; font-weight: 600; padding: 5px 12px;
    border-radius: 20px; letter-spacing: 0.3px;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: default;
  }
  .pill:hover { transform: translateY(-2px); }
  .pill-b { background: rgba(0,180,255,0.12); color: #60d0ff; border: 1px solid rgba(0,180,255,0.25); }
  .pill-g { background: rgba(0,255,128,0.08); color: #40f090; border: 1px solid rgba(0,200,100,0.2); }
  .pill-o { background: rgba(255,160,0,0.08); color: #ffbb44; border: 1px solid rgba(255,160,0,0.2); }
  .pill-p { background: rgba(160,80,255,0.08); color: #cc88ff; border: 1px solid rgba(160,80,255,0.2); }

  .flow-section { margin-bottom: 1.5rem; }
  .flow-title {
    font-family: 'Orbitron', monospace; font-size: 12px; letter-spacing: 2px;
    color: rgba(100,180,255,0.6); text-align: center; margin-bottom: 1rem;
    text-transform: uppercase;
    animation: fadeSlide 0.8s 1.3s ease forwards; opacity: 0;
  }

  .flow-steps {
    display: flex; flex-direction: column; gap: 0;
    animation: fadeSlide 0.8s 1.4s ease forwards; opacity: 0;
  }
  .flow-step {
    display: flex; align-items: center; gap: 12px; padding: 12px 14px;
    background: rgba(0,150,220,0.05);
    border: 1px solid rgba(0,180,255,0.1);
    border-radius: 12px; margin-bottom: 4px;
    transition: background 0.2s, border-color 0.2s;
    cursor: default;
  }
  .flow-step:hover {
    background: rgba(0,180,255,0.1);
    border-color: rgba(0,180,255,0.3);
  }
  .step-num {
    font-family: 'Orbitron', monospace;
    font-size: 13px; font-weight: 700;
    color: #00c3ff; min-width: 22px;
  }
  .step-label { font-size: 13px; color: rgba(200,225,255,0.9); flex: 1; }
  .step-status {
    font-size: 10px; font-weight: 600; padding: 3px 8px;
    border-radius: 10px; letter-spacing: 0.3px;
  }
  .s-active { background: rgba(0,255,128,0.12); color: #00ff88; border: 1px solid rgba(0,200,100,0.25); }
  .s-ai { background: rgba(0,180,255,0.12); color: #60d0ff; border: 1px solid rgba(0,180,255,0.25); }
  .s-alert { background: rgba(255,80,80,0.12); color: #ff7070; border: 1px solid rgba(255,80,80,0.25); }
  .s-report { background: rgba(255,160,0,0.1); color: #ffbb44; border: 1px solid rgba(255,160,0,0.2); }

  .arrow-line {
    display: flex; justify-content: center; align-items: center;
    height: 20px; color: rgba(0,180,255,0.4); font-size: 18px;
    animation: pulse-arrow 2s infinite;
  }
  @keyframes pulse-arrow {
    0%, 100% { color: rgba(0,180,255,0.3); }
    50% { color: rgba(0,220,255,0.7); }
  }

  .live-section {
    background: rgba(0,180,255,0.04);
    border: 1px solid rgba(0,180,255,0.15);
    border-radius: 16px; padding: 1.25rem;
    margin-bottom: 1.2rem;
    animation: fadeSlide 0.8s 1.5s ease forwards; opacity: 0;
  }
  .live-header {
    display: flex; align-items: center; gap: 8px; margin-bottom: 1rem;
  }
  .live-dot {
    width: 8px; height: 8px; border-radius: 50%; background: #ff4444;
    animation: blink 1s infinite;
  }
  @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }

  .live-title { font-size: 13px; font-weight: 600; color: #ff6666; letter-spacing: 1px; text-transform: uppercase; font-family: 'Orbitron', monospace; }
  .live-subtitle { font-size: 12px; color: rgba(150,190,230,0.6); margin-left: auto; }

  .violation-list { display: flex; flex-direction: column; gap: 6px; }
  .v-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 8px 12px;
    border-radius: 8px; font-size: 12px;
  }
  .v-high { background: rgba(255,60,60,0.08); border: 1px solid rgba(255,60,60,0.2); }
  .v-med { background: rgba(255,160,0,0.07); border: 1px solid rgba(255,160,0,0.18); }
  .v-low { background: rgba(0,200,100,0.06); border: 1px solid rgba(0,200,100,0.16); }
  .v-name { color: rgba(210,230,255,0.9); }
  .v-badge {
    font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 8px;
    letter-spacing: 0.3px;
  }
  .vb-h { background: rgba(255,60,60,0.2); color: #ff6060; }
  .vb-m { background: rgba(255,160,0,0.15); color: #ffaa30; }
  .vb-l { background: rgba(0,200,100,0.12); color: #40e080; }

  .stats-row {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;
    margin-bottom: 1.2rem;
    animation: fadeSlide 0.8s 1.6s ease forwards; opacity: 0;
  }
  .stat-card {
    background: rgba(0,150,220,0.06);
    border: 1px solid rgba(0,180,255,0.15);
    border-radius: 12px; padding: 12px;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
    cursor: default;
  }
  .stat-card:hover { transform: translateY(-2px); border-color: rgba(0,200,255,0.35); }
  .stat-num {
    font-family: 'Orbitron', monospace;
    font-size: 22px; font-weight: 700; display: block; margin-bottom: 4px;
  }
  .stat-label { font-size: 11px; color: rgba(150,190,230,0.65); letter-spacing: 0.3px; }
  .sn-blue { color: #00c3ff; text-shadow: 0 0 12px rgba(0,195,255,0.5); }
  .sn-green { color: #00ff88; text-shadow: 0 0 12px rgba(0,255,136,0.4); }
  .sn-orange { color: #ffaa00; text-shadow: 0 0 12px rgba(255,170,0,0.4); }

  .cta-row {
    display: flex; gap: 10px; margin-top: 0.5rem;
    animation: fadeSlide 0.8s 1.8s ease forwards; opacity: 0;
  }
  .cta-btn {
    flex: 1; padding: 12px; border-radius: 12px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 13px; font-weight: 600; letter-spacing: 0.5px;
    cursor: pointer; border: none; transition: all 0.2s;
    text-align: center;
  }
  .cta-primary {
    background: linear-gradient(135deg, #0088cc, #0055aa);
    color: #fff; border: 1px solid rgba(0,200,255,0.4);
  }
  .cta-primary:hover { background: linear-gradient(135deg, #00aaee, #0077cc); transform: translateY(-1px); box-shadow: 0 4px 15px rgba(0,150,255,0.3); }
  .cta-secondary {
    background: rgba(0,180,255,0.07);
    color: #60d0ff; border: 1px solid rgba(0,180,255,0.2);
  }
  .cta-secondary:hover { background: rgba(0,180,255,0.14); border-color: rgba(0,200,255,0.35); transform: translateY(-1px); }

  .footer-line {
    text-align: center; font-size: 11px;
    color: rgba(100,150,200,0.4); margin-top: 1.5rem;
    font-family: 'Orbitron', monospace; letter-spacing: 1px;
    animation: fadeSlide 0.8s 2s ease forwards; opacity: 0;
  }

  .progress-bar-wrap { margin-top: 8px; }
  .bar-label { display: flex; justify-content: space-between; font-size: 11px; color: rgba(150,190,230,0.6); margin-bottom: 4px; }
  .bar-bg { height: 6px; background: rgba(0,180,255,0.1); border-radius: 4px; overflow: hidden; }
  .bar-fill { height: 100%; border-radius: 4px; animation: growBar 2s ease forwards; }
  @keyframes growBar { from { width: 0%; } }
  .bar-c { background: linear-gradient(90deg, #00c3ff, #0088ff); }
  .bar-a { background: linear-gradient(90deg, #00ff88, #00cc66); }
  .bar-s { background: linear-gradient(90deg, #ffaa00, #ff7700); }

  .section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,180,255,0.2), transparent);
    margin: 1.2rem 0;
  }
</style>

<div class="hero-wrap">
  <div class="stars" id="stars"></div>
  <div class="scanline"></div>
  <div class="content">

    <div class="badge-row">
      <span class="badge badge-blue">MIT License</span>
      <span class="badge badge-green">Active</span>
      <span class="badge badge-orange">Python 3.8+</span>
    </div>

    <h1 class="hero-title">Smart Exam<br>Monitoring System</h1>
    <p class="hero-sub">AI-powered proctoring · Real-time detection · Secure examinations</p>

    <div class="stats-row">
      <div class="stat-card">
        <span class="stat-num sn-blue" id="acc">0%</span>
        <span class="stat-label">Detection Accuracy</span>
      </div>
      <div class="stat-card">
        <span class="stat-num sn-green" id="exams">0</span>
        <span class="stat-label">Exams Monitored</span>
      </div>
      <div class="stat-card">
        <span class="stat-num sn-orange" id="fps">0</span>
        <span class="stat-label">FPS Processing</span>
      </div>
    </div>

    <div class="monitor-box" style="animation-delay:0.5s">
      <div class="box-header">
        <div class="icon-circle ic-blue"><i class="ti ti-eye" aria-hidden="true"></i></div>
        <div>
          <div class="box-title">Real-time monitoring</div>
          <div class="box-subtitle">Live AI surveillance engine</div>
        </div>
      </div>
      <div class="feature-grid">
        <div class="feat"><span class="feat-dot dot-blue"></span><span class="feat-label">Face detection & tracking</span></div>
        <div class="feat"><span class="feat-dot dot-green"></span><span class="feat-label">Eye gaze analysis</span></div>
        <div class="feat"><span class="feat-dot dot-orange"></span><span class="feat-label">Multiple face alert</span></div>
        <div class="feat"><span class="feat-dot dot-purple"></span><span class="feat-label">Head pose estimation</span></div>
      </div>
    </div>

    <div class="monitor-box" style="animation-delay:0.7s">
      <div class="box-header">
        <div class="icon-circle ic-green"><i class="ti ti-cpu" aria-hidden="true"></i></div>
        <div>
          <div class="box-title">AI analysis engine</div>
          <div class="box-subtitle">Behavior intelligence core</div>
        </div>
      </div>
      <div class="progress-bar-wrap">
        <div class="bar-label"><span>Computer Vision</span><span>96%</span></div>
        <div class="bar-bg"><div class="bar-fill bar-c" style="width:96%"></div></div>
      </div>
      <div class="progress-bar-wrap" style="margin-top:10px">
        <div class="bar-label"><span>Behavior Analysis</span><span>91%</span></div>
        <div class="bar-bg"><div class="bar-fill bar-a" style="width:91%"></div></div>
      </div>
      <div class="progress-bar-wrap" style="margin-top:10px">
        <div class="bar-label"><span>Security Scoring</span><span>88%</span></div>
        <div class="bar-bg"><div class="bar-fill bar-s" style="width:88%"></div></div>
      </div>
    </div>

    <div class="section-divider"></div>

    <div class="flow-section">
      <div class="flow-title">System flow</div>
      <div class="flow-steps">
        <div class="flow-step">
          <span class="step-num">01</span>
          <span class="step-label">Student login & camera verify</span>
          <span class="step-status s-active">Live</span>
        </div>
        <div class="arrow-line">↓</div>
        <div class="flow-step">
          <span class="step-num">02</span>
          <span class="step-label">Face authentication & enrollment</span>
          <span class="step-status s-ai">AI</span>
        </div>
        <div class="arrow-line">↓</div>
        <div class="flow-step">
          <span class="step-num">03</span>
          <span class="step-label">Exam starts with monitoring</span>
          <span class="step-status s-active">Active</span>
        </div>
        <div class="arrow-line">↓</div>
        <div class="flow-step">
          <span class="step-num">04</span>
          <span class="step-label">Violation detected & flagged</span>
          <span class="step-status s-alert">Alert</span>
        </div>
        <div class="arrow-line">↓</div>
        <div class="flow-step">
          <span class="step-num">05</span>
          <span class="step-label">Auto report & screenshot saved</span>
          <span class="step-status s-report">Report</span>
        </div>
      </div>
    </div>

    <div class="section-divider"></div>

    <div class="live-section">
      <div class="live-header">
        <div class="live-dot"></div>
        <span class="live-title">Violation alerts</span>
        <span class="live-subtitle">Severity levels</span>
      </div>
      <div class="violation-list">
        <div class="v-item v-high">
          <span class="v-name">Face not found (&gt;3s)</span>
          <span class="v-badge vb-h">🔴 High</span>
        </div>
        <div class="v-item v-high">
          <span class="v-name">Multiple faces detected</span>
          <span class="v-badge vb-h">🔴 High</span>
        </div>
        <div class="v-item v-high">
          <span class="v-name">Browser tab switched</span>
          <span class="v-badge vb-h">🔴 High</span>
        </div>
        <div class="v-item v-med">
          <span class="v-name">Gaze away (&gt;2s)</span>
          <span class="v-badge vb-m">🟡 Medium</span>
        </div>
        <div class="v-item v-med">
          <span class="v-name">Head turned sideways</span>
          <span class="v-badge vb-m">🟡 Medium</span>
        </div>
        <div class="v-item v-low">
          <span class="v-name">Mouth movement detected</span>
          <span class="v-badge vb-l">🟢 Low</span>
        </div>
      </div>
    </div>

    <div class="monitor-box" style="animation-delay:1.1s">
      <div class="box-header">
        <div class="icon-circle ic-purple"><i class="ti ti-stack-2" aria-hidden="true"></i></div>
        <div>
          <div class="box-title">Tech stack</div>
          <div class="box-subtitle">Powered by modern frameworks</div>
        </div>
      </div>
      <div class="tech-pills">
        <span class="pill pill-b">Python</span>
        <span class="pill pill-b">OpenCV</span>
        <span class="pill pill-b">MediaPipe</span>
        <span class="pill pill-g">React.js</span>
        <span class="pill pill-g">Node.js</span>
        <span class="pill pill-o">TensorFlow</span>
        <span class="pill pill-o">PyTorch</span>
        <span class="pill pill-p">PostgreSQL</span>
        <span class="pill pill-p">WebSocket</span>
        <span class="pill pill-b">Docker</span>
        <span class="pill pill-g">JWT Auth</span>
        <span class="pill pill-o">Flask</span>
      </div>
    </div>

    <div class="cta-row">
      <button class="cta-btn cta-primary" onclick="sendPrompt('Smart Exam Monitoring System ka installation guide step by step do')">⚙️ Installation Guide</button>
      <button class="cta-btn cta-secondary" onclick="sendPrompt('Smart Exam Monitoring System ke liye API documentation banao')">📄 API Docs</button>
    </div>

    <div class="footer-line">Made with ❤️ · Fair education · Secure examinations</div>

  </div>
</div>

<script>
  const s = document.getElementById('stars');
  for (let i = 0; i < 60; i++) {
    const d = document.createElement('div');
    d.className = 'star';
    const sz = Math.random() * 2.5 + 0.5;
    d.style.cssText = `width:${sz}px;height:${sz}px;top:${Math.random()*100}%;left:${Math.random()*100}%;animation-delay:${Math.random()*3}s;animation-duration:${2+Math.random()*3}s;`;
    s.appendChild(d);
  }

  function animCount(id, target, suffix, dur) {
    let start = null;
    const el = document.getElementById(id);
    function step(ts) {
      if (!start) start = ts;
      const prog = Math.min((ts - start) / dur, 1);
      const val = Math.round(prog * target);
      el.textContent = val + suffix;
      if (prog < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  setTimeout(() => {
    animCount('acc', 97, '%', 2000);
    animCount('exams', 12400, '', 2200);
    animCount('fps', 30, '', 1500);
  }, 800);
</script>

import os
from flask import Flask, Response, send_from_directory, abort

app = Flask(__name__, static_folder="static")

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Maths Made Easy With Oly - Game</title>
<style>
  *{box-sizing:border-box;font-family:'Segoe UI',Arial,sans-serif}
  body{margin:0;background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);min-height:100vh;display:flex;justify-content:center;padding:14px}
  .wrap{width:100%;max-width:720px;background:#fff;border-radius:24px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.35);align-self:flex-start}
  .logo{background:linear-gradient(90deg,#FFD700,#FF9A00,#FFD700);padding:14px 16px;text-align:center;border-bottom:5px solid #111}
  .logo img{width:100%;max-width:520px;border-radius:14px;border:3px solid #111;display:block;margin:0 auto 8px;background:#fff}
  .logo h1{margin:0;font-size:28px;line-height:1.1;color:#111;text-transform:uppercase}
  .logo h1 span{color:#0b6e2f}
  .logo p{margin:6px 0 0;font-weight:800;font-size:14px}
  .logo small{background:#111;color:#FFD700;padding:4px 12px;border-radius:20px;display:inline-block;margin-top:8px;font-weight:800}
  .topbar{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:#f1f5ff;font-weight:800;flex-wrap:wrap;gap:6px}
  .pill{background:#111;color:#fff;padding:6px 12px;border-radius:20px;font-size:13px}
  .pill.timer{background:#dc2626}
  .progress{height:10px;background:#e5e7eb}
  .progress i{display:block;height:100%;background:linear-gradient(90deg,#22c55e,#facc15);width:0;transition:width .3s}
  .timebar{height:8px;background:#fee2e2}
  .timebar i{display:block;height:100%;background:#dc2626;width:100%;transition:width 1s linear}
  .card{padding:18px 16px 22px}
  .step{font-size:13px;font-weight:900;color:#0b6e2f;letter-spacing:1px}
  .q{font-size:23px;font-weight:900;line-height:1.35;margin:10px 0 16px;color:#111}
  .opts{display:grid;gap:12px}
  .opt{display:flex;align-items:center;gap:12px;width:100%;text-align:left;background:#f8fafc;border:3px solid #111;border-radius:16px;padding:16px 14px;font-size:19px;font-weight:900;cursor:pointer;color:#111}
  .opt:hover:not(:disabled){background:#fff7cc}
  .opt:disabled{cursor:default}
  .opt.selected{background:#FFD700}
  .opt.correct{background:#bbf7d0!important}
  .opt.wrong{background:#fecaca!important}
  .letter{width:38px;height:38px;flex:0 0 38px;border-radius:50%;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;font-size:18px}
  .nav{display:flex;justify-content:space-between;align-items:center;margin-top:18px}
  .next{background:#000;color:#fff;border:none;padding:15px 22px;border-radius:50px;font-size:19px;font-weight:900;cursor:pointer;display:flex;align-items:center;gap:10px;box-shadow:0 6px 0 #333}
  .next:disabled{opacity:.35;cursor:not-allowed}
  .arrow{font-size:26px;line-height:1}
  .prev{background:#fff;border:2px solid #111;padding:12px 16px;border-radius:50px;font-weight:800;cursor:pointer;color:#111}
  .prev:disabled{opacity:.35;cursor:not-allowed}
  .feedback{min-height:28px;font-weight:900;text-align:center;margin-top:12px;font-size:16px}
  .result{text-align:center;padding:10px}
  .big{font-size:64px}
  .btn{background:#111;color:#fff;border:none;padding:15px 22px;border-radius:50px;font-weight:900;font-size:17px;cursor:pointer;margin:6px}
  .btn.yellow{background:#FFD700;color:#111}
  .sound-row{text-align:center;padding:6px;font-size:13px;font-weight:800}
  @media(max-width:480px){.logo h1{font-size:22px}.q{font-size:20px}.opt{font-size:17px}}
</style>
</head>
<body>
<div class="wrap">
  <div class="logo">
    <img src="/logo.jpg" alt="Maths Made Easy With Oly Logo" onerror="this.style.display='none'">
    <h1>Maths Made Easy <span>With Oly</span> 🎮</h1>
    <p>GRADE 8 (JSS 2) &amp; BASIC 1 • MATHEMATICS GAME</p>
    <small>✦ PLAY • LEARN • WIN ✦</small>
  </div>
  <div class="topbar">
    <span id="levelLabel">STEP 1: BASIC 1</span>
    <span class="pill timer">⏱️ <span id="timer">30</span>s</span>
    <span class="pill">⭐ Score: <span id="score">0</span></span>
    <span class="pill">Q <span id="qCount">1</span>/40</span>
  </div>
  <div class="progress"><i id="bar"></i></div>
  <div class="timebar"><i id="timeBar"></i></div>
  <div class="sound-row">🔊 Sound: <button onclick="toggleSound()" id="soundBtn">ON 🔊</button> • Timer: 30 seconds per question</div>

  <div class="card" id="game">
    <div class="step" id="stepLabel">STEP 1 — BASIC 1</div>
    <div class="q" id="question">Loading...</div>
    <div class="opts" id="options"></div>
    <div class="feedback" id="feedback"></div>
    <div class="nav">
      <button class="prev" id="prevBtn" onclick="prevQ()">← Back</button>
      <button class="next" id="nextBtn" onclick="nextQ()" disabled>Next <span class="arrow">➔</span></button>
    </div>
  </div>

  <div class="card result" id="result" style="display:none">
    <div class="big">🏆</div>
    <h2 id="resultTitle">Well Done!</h2>
    <p style="font-size:20px;font-weight:800" id="resultText"></p>
    <p id="resultMsg" style="font-weight:700"></p>
    <button class="btn yellow" onclick="location.reload()">🔁 Play Again</button>
    <button class="btn" onclick="shareScore()">📤 Share Score</button>
  </div>
</div>

<script>
/* ---------- SOUND (one shared AudioContext) ---------- */
let soundOn = true, audioCtx = null;
function getCtx(){
  if(!audioCtx){
    const C = window.AudioContext || window.webkitAudioContext;
    if(!C) return null;
    audioCtx = new C();
  }
  if(audioCtx.state === 'suspended') audioCtx.resume();
  return audioCtx;
}
function toggleSound(){
  soundOn = !soundOn;
  document.getElementById('soundBtn').textContent = soundOn ? 'ON 🔊' : 'OFF 🔇';
}
function beep(freq, dur, type){
  if(!soundOn) return;
  try{
    const ctx = getCtx(); if(!ctx) return;
    const o = ctx.createOscillator(), g = ctx.createGain();
    o.type = type || 'sine';
    o.frequency.value = freq;
    g.gain.value = 0.18;
    o.connect(g); g.connect(ctx.destination);
    o.start(); o.stop(ctx.currentTime + dur);
  }catch(e){}
}
function playCorrect(){beep(523,.12);setTimeout(()=>beep(659,.12),120);setTimeout(()=>beep(784,.25),240);}
function playWrong(){beep(220,.25,'sawtooth');}
function playClick(){beep(440,.07);}
function playWin(){[523,659,784,1046].forEach((f,i)=>setTimeout(()=>beep(f,.25),i*180));}

/* ---------- QUESTIONS: [question, [options], correctIndex] ---------- */
const basic1 = [
  ["What is 5 + 7 ?",["10","11","12","13"],2],
  ["What is 15 - 8 ?",["6","7","8","9"],1],
  ["What is 4 × 6 ?",["20","22","24","26"],2],
  ["What is 20 ÷ 4 ?",["4","5","6","20"],1],
  ["Which number is greater: 45 or 54 ?",["45","54","Equal","None"],1],
  ["What is the place value of 5 in 356 ?",["5","50","500","5,000"],1],
  ["What is 100 + 250 ?",["300","350","400","250"],1],
  ["How many sides does a triangle have?",["2","3","4","5"],1],
  ["What is 1/2 of 10 ?",["2","5","10","20"],1],
  ["What comes next? 10, 20, 30, ___",["35","40","45","50"],1],
  ["What is 9 × 3 ?",["21","24","27","30"],2],
  ["If you have ₦50 and spend ₦20, how much is left?",["₦20","₦30","₦40","₦70"],1],
  ["How many minutes are in 1 hour?",["30","45","60","90"],2],
  ["What is 7 + 8 + 5 ?",["18","19","20","21"],2],
  ["Which shape is round?",["Square","Triangle","Circle","Rectangle"],2],
  ["What is 48 - 19 ?",["29","30","31","39"],0],
  ["What is 6 × 7 ?",["36","40","42","48"],2],
  ["What is 1/4 of 20 ?",["4","5","10","20"],1],
  ["How many days are in a week?",["5","6","7","8"],2],
  ["What is 99 + 1 ?",["90","99","100","110"],2]
];
const jss2 = [
  ["Solve: 2x + 3 = 11",["x = 3","x = 4","x = 5","x = 8"],1],
  ["Which of these is a prime number?",["1","2","4","9"],1],
  ["Solve: 3(x + 2) = 15",["x = 1","x = 2","x = 3","x = 5"],2],
  ["Find x: 2x + 7 = 19",["x = 4","x = 6","x = 8","x = 10"],1],
  ["What is 3² ?",["3","6","9","27"],2],
  ["Simplify: (a²)³",["a³","a⁵","a⁶","a⁹"],2],
  ["Expand: (x + 3)²",["x² + 3x + 9","x² + 6x + 9","x² - 3x + 9","x² + 9x + 6"],1],
  ["Factorize: x² - 9",["(x + 3)(x - 3)","(x + 9)(x - 1)","(x + 3)²","(x - 3)²"],0],
  ["Next term: 2, 5, 8, 11, ...",["13","14","15","16"],1],
  ["What is 3/4 + 1/4 ?",["1/3","1/2","3/4","1"],3],
  ["Simplify: 5/6 + 1/3",["1/2","2/3","5/6","7/6"],3],
  ["Find the perimeter of a rectangle with length 7 cm and breadth 3 cm.",["10 cm","14 cm","18 cm","20 cm"],3],
  ["Which is equivalent to 50% ?",["1/4","1/2","3/4","100%"],1],
  ["Solve: 3x = 24",["x = 4","x = 6","x = 8","x = 12"],2],
  ["A box has 48 pencils. Each pack holds 8. How many packs are there?",["4","5","6","8"],2],
  ["What is the value of 5⁰ ?",["0","1","5","10"],1],
  ["Two angles are complementary. One is 62°. Find the other angle.",["28°","32°","38°","62°"],0],
  ["Convert 60 cm to metres.",["0.06 m","0.6 m","6 m","60 m"],1],
  ["Which number is divisible by 3?",["17","21","25","29"],1],
  ["Find the value of 7x - 3 when x = 2.",["11","10","7","1"],0]
];
const all = [
  ...basic1.map(x => ({q:x[0], o:x[1], a:x[2], step:1})),
  ...jss2.map(x => ({q:x[0], o:x[1], a:x[2], step:2}))
];
const TOTAL = all.length;
const TIME = 30;

/* ---------- STATE ---------- */
let idx = 0, score = 0, timeLeft = TIME, timerInt = null, autoNext = null;
const answers = new Array(TOTAL).fill(null);   // null = unanswered, -1 = timed out
const $ = id => document.getElementById(id);

/* ---------- TIMER ---------- */
function setTimeBar(pct, animate){
  const t = $('timeBar');
  t.style.transition = animate ? 'width 1s linear' : 'none';
  t.style.width = pct + '%';
  if(!animate) void t.offsetWidth;   // force reflow so the jump is instant
}
function startTimer(){
  clearInterval(timerInt);
  timeLeft = TIME;
  $('timer').textContent = timeLeft;
  setTimeBar(100, false);
  timerInt = setInterval(() => {
    timeLeft--;
    $('timer').textContent = Math.max(timeLeft, 0);
    setTimeBar(Math.max(timeLeft, 0) / TIME * 100, true);
    if(timeLeft <= 5 && timeLeft > 0) beep(880, .08);
    if(timeLeft <= 0){ clearInterval(timerInt); handleTimeout(); }
  }, 1000);
}
function handleTimeout(){
  if(answers[idx] !== null) return;
  answers[idx] = -1;
  playWrong();
  render();
  clearTimeout(autoNext);
  const at = idx;
  autoNext = setTimeout(() => { if(idx === at) nextQ(true); }, 1500);
}

/* ---------- RENDER ---------- */
function render(){
  const cur = all[idx], ans = answers[idx], answered = ans !== null;
  $('stepLabel').textContent = cur.step === 1 ? 'STEP 1 — BASIC 1 • EASY & FUN' : 'STEP 2 — JSS 2 • CHALLENGE TIME!';
  $('levelLabel').textContent = cur.step === 1 ? 'STEP 1: BASIC 1' : 'STEP 2: JSS 2';
  $('question').textContent = cur.q;
  $('qCount').textContent = idx + 1;
  $('score').textContent = score;
  $('bar').style.width = (idx / TOTAL * 100) + '%';
  $('prevBtn').disabled = idx === 0;
  $('nextBtn').disabled = !answered;
  $('nextBtn').innerHTML = idx === TOTAL - 1 ? 'Finish 🏁' : 'Next <span class="arrow">➔</span>';

  let fb = 'Choose one answer 👆';
  if(ans === -1) fb = '⏰ Time up! Correct answer: ' + cur.o[cur.a];
  else if(answered) fb = ans === cur.a ? '✅ Correct! +1 point' : '❌ Wrong. Correct answer: ' + cur.o[cur.a];
  $('feedback').textContent = fb;

  const box = $('options');
  box.innerHTML = '';
  cur.o.forEach((opt, i) => {
    const b = document.createElement('button');
    b.className = 'opt'
      + (ans === i ? ' selected' : '')
      + (answered && i === cur.a ? ' correct' : '')
      + (answered && ans === i && i !== cur.a ? ' wrong' : '');
    b.disabled = answered;
    const l = document.createElement('span'); l.className = 'letter'; l.textContent = 'ABCD'[i];
    const t = document.createElement('span'); t.textContent = opt;
    b.append(l, t);
    b.onclick = () => choose(i);
    box.appendChild(b);
  });

  if(!answered){ startTimer(); }
  else {
    clearInterval(timerInt);
    $('timer').textContent = '--';
    setTimeBar(0, false);
  }
}

function choose(i){
  if(answers[idx] !== null) return;
  answers[idx] = i;
  if(i === all[idx].a){ score++; playCorrect(); } else { playWrong(); }
  render();
}

/* ---------- NAVIGATION ---------- */
function nextQ(auto){
  clearTimeout(autoNext);
  if(auto !== true) playClick();
  if(idx < TOTAL - 1){ idx++; render(); } else { showResult(); }
}
function prevQ(){
  clearTimeout(autoNext);
  if(idx > 0){ idx--; render(); }
}

/* ---------- RESULT ---------- */
function showResult(){
  clearInterval(timerInt);
  clearTimeout(autoNext);
  playWin();
  $('game').style.display = 'none';
  $('result').style.display = 'block';
  $('bar').style.width = '100%';
  $('resultText').textContent = `You scored ${score} / ${TOTAL}`;
  $('resultTitle').textContent = score >= 35 ? '🏆 Maths Champion!' : score >= 25 ? '🌟 Great Job!' : score >= 15 ? '👍 Good Try!' : '💪 Keep Practising!';
  $('resultMsg').textContent = score >= 35 ? 'You are a Maths Star with Oly!' : 'Play again to beat your score!';
}

async function shareScore(){
  const t = `I scored ${score}/${TOTAL} in Maths Made Easy With Oly! Can you beat me?`;
  try{
    if(navigator.share){ await navigator.share({text:t}); return; }
    await navigator.clipboard.writeText(t);
    alert('Score copied! Paste it on TikTok');
  }catch(e){
    if(e && e.name === 'AbortError') return;
    prompt('Copy your score:', t);
  }
}

render();
</script>
</body>
</html>'''


@app.route("/")
def index():
    resp = Response(HTML, mimetype="text/html")
    resp.headers["Cache-Control"] = "no-cache"
    return resp


@app.route("/logo.jpg")
def logo():
    # Put your logo at static/logo.jpg (the page hides the image if it is missing)
    path = os.path.join(app.static_folder, "logo.jpg")
    if not os.path.isfile(path):
        abort(404)
    return send_from_directory(app.static_folder, "logo.jpg")


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

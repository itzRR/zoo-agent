"""
Zoo AI Assistant — FastAPI Application
Serves the agent via REST API, deployable on Google Cloud Run.
"""

import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from main import run_agent

# ── App Setup ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Zoo AI Assistant",
    description="Ask anything about animals, habitats, and zoo life!",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── UI (with_ui) ──────────────────────────────────────────────────────────────

UI_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>🦁 Zoo AI Assistant</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;900&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:        #0d1117;
      --surface:   #161b22;
      --card:      #1e2530;
      --accent1:   #f9a825;
      --accent2:   #43a047;
      --accent3:   #1e88e5;
      --text:      #e6edf3;
      --muted:     #8b949e;
      --radius:    16px;
    }

    body {
      font-family: 'Outfit', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    /* ── Hero ── */
    header {
      width: 100%;
      background: linear-gradient(135deg, #1a2a1a 0%, #0d1117 60%, #1a1a2e 100%);
      text-align: center;
      padding: 3rem 1rem 2.5rem;
      border-bottom: 1px solid #30363d;
    }
    header .emoji-row {
      font-size: 3rem;
      letter-spacing: 0.3rem;
      margin-bottom: 0.75rem;
      animation: bounce 2s ease-in-out infinite;
    }
    @keyframes bounce {
      0%, 100% { transform: translateY(0); }
      50%       { transform: translateY(-8px); }
    }
    header h1 {
      font-size: clamp(2rem, 5vw, 3.2rem);
      font-weight: 900;
      background: linear-gradient(90deg, var(--accent1), var(--accent2), var(--accent3));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    header p {
      margin-top: 0.5rem;
      color: var(--muted);
      font-size: 1.05rem;
    }

    /* ── Main Container ── */
    main {
      width: 100%;
      max-width: 760px;
      padding: 2rem 1rem 4rem;
    }

    /* ── Search Box ── */
    .search-card {
      background: var(--card);
      border: 1px solid #30363d;
      border-radius: var(--radius);
      padding: 1.75rem;
      box-shadow: 0 4px 30px rgba(0,0,0,0.4);
    }
    .search-row {
      display: flex;
      gap: 0.75rem;
    }
    #query-input {
      flex: 1;
      background: var(--surface);
      border: 1.5px solid #30363d;
      border-radius: 10px;
      color: var(--text);
      font-family: 'Outfit', sans-serif;
      font-size: 1rem;
      padding: 0.85rem 1.1rem;
      transition: border-color 0.2s;
      outline: none;
    }
    #query-input:focus { border-color: var(--accent1); }
    #query-input::placeholder { color: var(--muted); }

    #ask-btn {
      background: linear-gradient(135deg, var(--accent1), #e65100);
      border: none;
      border-radius: 10px;
      color: #fff;
      cursor: pointer;
      font-family: 'Outfit', sans-serif;
      font-size: 1rem;
      font-weight: 700;
      padding: 0.85rem 1.6rem;
      transition: transform 0.15s, box-shadow 0.15s;
      white-space: nowrap;
    }
    #ask-btn:hover  { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(249,168,37,0.4); }
    #ask-btn:active { transform: translateY(0); }
    #ask-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

    /* Quick suggestion chips */
    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 1rem;
    }
    .chip {
      background: var(--surface);
      border: 1px solid #30363d;
      border-radius: 20px;
      color: var(--muted);
      cursor: pointer;
      font-size: 0.85rem;
      padding: 0.35rem 0.9rem;
      transition: all 0.2s;
    }
    .chip:hover { border-color: var(--accent1); color: var(--accent1); }

    /* ── Response Area ── */
    #response-area {
      margin-top: 1.5rem;
      display: none;
    }
    .response-card {
      background: var(--card);
      border: 1px solid #30363d;
      border-left: 4px solid var(--accent2);
      border-radius: var(--radius);
      padding: 1.5rem;
      line-height: 1.7;
      font-size: 1.02rem;
      box-shadow: 0 4px 30px rgba(0,0,0,0.3);
      animation: fadeUp 0.4s ease;
    }
    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(16px); }
      to   { opacity: 1; transform: translateY(0);    }
    }
    .response-label {
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      color: var(--accent2);
      text-transform: uppercase;
      margin-bottom: 1rem;
    }
    
    /* Markdown Styles */
    #response-text p { margin-bottom: 0.8rem; }
    #response-text ul, #response-text ol { margin-left: 1.5rem; margin-bottom: 0.8rem; }
    #response-text li { margin-bottom: 0.4rem; padding-left: 0.2rem; }
    #response-text strong { color: var(--accent1); font-weight: 600; }
    #response-text em { color: var(--text); opacity: 0.9; }
    #response-text h1, #response-text h2, #response-text h3 { margin-top: 1.2rem; margin-bottom: 0.6rem; color: #fff; }

    /* ── Spinner ── */
    .spinner {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      color: var(--muted);
      font-size: 0.95rem;
    }
    .dot-pulse {
      display: flex;
      gap: 5px;
    }
    .dot-pulse span {
      width: 8px; height: 8px;
      background: var(--accent1);
      border-radius: 50%;
      animation: pulse 1.2s ease-in-out infinite;
    }
    .dot-pulse span:nth-child(2) { animation-delay: 0.2s; }
    .dot-pulse span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes pulse {
      0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
      40%            { transform: scale(1);   opacity: 1;   }
    }

    /* ── Fun Facts Ticker ── */
    .ticker-wrap {
      margin-top: 3rem;
      background: var(--surface);
      border: 1px solid #30363d;
      border-radius: 10px;
      overflow: hidden;
      padding: 0.6rem 1rem;
    }
    .ticker-label { font-size: 0.75rem; color: var(--accent1); font-weight: 700; margin-bottom: 0.25rem; }
    #ticker-text  { font-size: 0.9rem; color: var(--muted); }

    footer {
      margin-top: 1.5rem;
      text-align: center;
      color: var(--muted);
      font-size: 0.82rem;
    }
  </style>
</head>
<body>

<header>
  <div class="emoji-row">🦁 🐘 🦒 🐧 🐬</div>
  <h1>Zoo AI Assistant</h1>
  <p>Powered by Google ADK &amp; Gemini — Ask me anything about animals!</p>
</header>

<main>
  <div class="search-card">
    <div class="search-row">
      <input
        id="query-input"
        type="text"
        placeholder="e.g. Tell me about lions..."
        autocomplete="off"
      />
      <button id="ask-btn" onclick="askAgent()">Ask 🔍</button>
    </div>
    <div class="chips" id="chips"></div>
  </div>

  <div id="response-area">
    <div class="response-card" id="response-card">
      <div class="response-label">🤖 Zoo AI says</div>
      <div id="response-text"></div>
    </div>
  </div>

  <div class="ticker-wrap">
    <div class="ticker-label">🌿 Did you know?</div>
    <div id="ticker-text">Loading fun fact…</div>
  </div>

  <footer>Built by Rehan ❤️ using Google ADK · SequentialAgent · Gemini</footer>
</main>

<script>
  // Quick suggestion chips
  const suggestions = ["Lion","Elephant","Penguin","Blue Whale","Red Panda","Giraffe","Chimpanzee","Snow Leopard"];
  const chipsEl = document.getElementById("chips");
  suggestions.forEach(s => {
    const c = document.createElement("button");
    c.className = "chip";
    c.textContent = "🔎 " + s;
    c.onclick = () => { document.getElementById("query-input").value = s; askAgent(); };
    chipsEl.appendChild(c);
  });

  // Fun facts ticker
  const facts = [
    "A group of flamingos is called a flamboyance. 🦩",
    "Elephants are the only animals that can't jump. 🐘",
    "A day in the life of a sloth: eat, sleep, hang. 🦥",
    "Otters hold hands while sleeping so they don't drift apart. 🦦",
    "A shrimp's heart is located in its head. 🦐",
    "Penguins propose with pebbles. 🐧",
    "Octopuses have three hearts and blue blood. 🐙",
    "Crows can recognise and remember human faces. 🐦‍⬛",
  ];
  let fi = 0;
  function rotateFact() {
    document.getElementById("ticker-text").textContent = facts[fi % facts.length];
    fi++;
  }
  rotateFact();
  setInterval(rotateFact, 5000);

  // Ask the agent
  async function askAgent() {
    const q = document.getElementById("query-input").value.trim();
    if (!q) return;

    const btn = document.getElementById("ask-btn");
    const area = document.getElementById("response-area");
    const text = document.getElementById("response-text");
    const card = document.getElementById("response-card");

    btn.disabled = true;
    btn.textContent = "Thinking…";
    area.style.display = "block";
    card.style.borderLeftColor = "var(--accent3)";
    text.innerHTML = `<div class="spinner"><div class="dot-pulse"><span></span><span></span><span></span></div> Searching for information…</div>`;

    try {
      const res = await fetch("/ask?q=" + encodeURIComponent(q));
      const data = await res.json();
      card.style.borderLeftColor = "var(--accent2)";
      if (data.response && !data.response.startsWith("Error:")) {
        text.innerHTML = marked.parse(data.response);
      } else {
        text.textContent = data.error || data.response || "No response.";
      }
    } catch (e) {
      card.style.borderLeftColor = "#f44336";
      text.textContent = "⚠️ Error connecting to agent. Please try again.";
    } finally {
      btn.disabled = false;
      btn.textContent = "Ask 🔍";
    }
  }

  // Allow Enter key
  document.getElementById("query-input").addEventListener("keydown", e => {
    if (e.key === "Enter") askAgent();
  });
</script>
</body>
</html>"""


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    """Serve the Zoo AI Assistant UI."""
    return UI_HTML

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Silence favicon 404 errors."""
    return Response(content=b"", media_type="image/x-icon", status_code=204)


@app.get("/health")
def health():
    """Health-check endpoint for Cloud Run."""
    return {"status": "ok", "service": "zoo-agent"}


@app.get("/ask")
def ask(q: str = Query(..., description="Your animal/zoo question")):
    """Run the SequentialAgent pipeline and return the response."""
    try:
        response = run_agent(q)
        return {"query": q, "response": response}
    except Exception as exc:  # noqa: BLE001
        return {"query": q, "error": str(exc), "response": f"Error: {str(exc)}"}


# ── Local Dev Entry Point ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)

"""
Phishing Link Checker — Streamlit Web App
Deploy to: https://share.streamlit.io
"""

import re
from datetime import datetime

import requests
import streamlit as st

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Phishing Link Checker",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Sora:wght@400;600;800&display=swap');

  /* Global */
  html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
    background-color: #060B14;
    color: #CBD5E1;
  }

  .stApp {
    background: radial-gradient(ellipse at 20% 0%, #0D2137 0%, #060B14 60%);
    min-height: 100vh;
  }

  /* Hide default streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }

  /* ── Hero Header ── */
  .hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
  }
  .hero-icon {
    font-size: 3.5rem;
    display: block;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 24px #3B82F680);
  }
  .hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #F1F5F9;
    letter-spacing: -0.5px;
    margin: 0;
  }
  .hero-title span { color: #3B82F6; }
  .hero-sub {
    font-size: 0.9rem;
    color: #475569;
    margin-top: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
  }

  /* ── Input Card ── */
  .input-card {
    background: #0F1C2E;
    border: 1px solid #1E3A5F;
    border-radius: 16px;
    padding: 1.6rem;
    margin: 1.2rem 0;
  }
  .input-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.6rem;
  }

  /* Override streamlit input */
  .stTextInput > div > div > input {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
    background: #060B14 !important;
    border: 1.5px solid #1E3A5F !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    padding: 0.75rem 1rem !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px #3B82F620 !important;
  }

  /* ── Scan Button ── */
  .stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #2563EB, #3B82F6) !important;
    color: white !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    letter-spacing: 0.3px;
    transition: all 0.2s ease;
    cursor: pointer;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8, #2563EB) !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 20px #2563EB40;
  }

  /* ── Result Cards ── */
  .result-card {
    border-radius: 16px;
    padding: 1.8rem;
    text-align: center;
    margin: 1rem 0;
    animation: fadeIn 0.4s ease;
  }
  .result-safe {
    background: linear-gradient(135deg, #052E16, #064E3B);
    border: 1px solid #065F46;
  }
  .result-threat {
    background: linear-gradient(135deg, #1C0B0B, #3B0A0A);
    border: 1px solid #7F1D1D;
  }
  .result-warning {
    background: linear-gradient(135deg, #1C1208, #3B2608);
    border: 1px solid #7C4A00;
  }
  .result-icon { font-size: 3rem; display: block; margin-bottom: 0.5rem; }
  .result-title {
    font-size: 1.4rem;
    font-weight: 800;
    margin: 0.2rem 0;
  }
  .result-title-safe  { color: #34D399; }
  .result-title-threat { color: #F87171; }
  .result-title-warn  { color: #FBBF24; }
  .result-url {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #64748B;
    word-break: break-all;
    margin-top: 0.5rem;
  }

  /* ── Threat Badges ── */
  .badge-row { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 1rem; }
  .badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
  .badge-malware    { background: #FF4C4C22; color: #FF4C4C; border: 1px solid #FF4C4C55; }
  .badge-social     { background: #FF8C0022; color: #FF8C00; border: 1px solid #FF8C0055; }
  .badge-unwanted   { background: #FFD70022; color: #FFD700; border: 1px solid #FFD70055; }
  .badge-harmful    { background: #FF634722; color: #FF6347; border: 1px solid #FF634755; }

  /* ── History ── */
  .history-section { margin-top: 2rem; }
  .history-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #334155;
    margin-bottom: 0.8rem;
    padding-left: 4px;
  }
  .history-row {
    display: flex;
    align-items: center;
    background: #0A1628;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 0.65rem 1rem;
    margin-bottom: 6px;
    gap: 12px;
    animation: fadeIn 0.3s ease;
  }
  .history-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #334155;
    min-width: 52px;
  }
  .history-url {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #64748B;
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .history-status { font-size: 0.75rem; font-weight: 700; white-space: nowrap; }
  .status-safe    { color: #34D399; }
  .status-threat  { color: #F87171; }
  .status-error   { color: #FBBF24; }

  /* ── Stats Bar ── */
  .stats-bar {
    display: flex;
    gap: 12px;
    margin: 1.2rem 0;
  }
  .stat-chip {
    flex: 1;
    background: #0A1628;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 0.8rem;
    text-align: center;
  }
  .stat-value { font-size: 1.6rem; font-weight: 800; color: #E2E8F0; }
  .stat-label { font-size: 0.68rem; color: #334155; text-transform: uppercase; letter-spacing: 1px; }

  /* ── Footer ── */
  .footer {
    text-align: center;
    font-size: 0.72rem;
    color: #1E293B;
    padding: 2rem 0 1rem;
    font-family: 'JetBrains Mono', monospace;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
</style>
""", unsafe_allow_html=True)


# ── Constants ──────────────────────────────────────────────────────────────────
THREAT_META = {
    "MALWARE":                         ("Malware",               "badge-malware"),
    "SOCIAL_ENGINEERING":              ("Phishing / Social Eng", "badge-social"),
    "UNWANTED_SOFTWARE":               ("Unwanted Software",     "badge-unwanted"),
    "POTENTIALLY_HARMFUL_APPLICATION": ("Harmful App",          "badge-harmful"),
}

# ── Session State ──────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []           # list of dicts
if "total_safe" not in st.session_state:
    st.session_state.total_safe   = 0
if "total_threat" not in st.session_state:
    st.session_state.total_threat = 0


# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize_url(url: str) -> str:
    url = url.strip()
    if url and not re.match(r"^https?://", url, re.IGNORECASE):
        url = "https://" + url
    return url


def is_valid_url(url: str) -> bool:
    pattern = re.compile(
        r"^https?://"
        r"(?:[A-Za-z0-9\-]+\.)+[A-Za-z]{2,}"
        r"(?::\d+)?(?:/[^\s]*)?$",
        re.IGNORECASE,
    )
    return bool(pattern.match(url))


def check_safe_browsing(url: str, api_key: str):
    """
    Returns (is_threat: bool, threats: list[str]).
    Raises on any error.
    """
    endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    payload = {
        "client": {"clientId": "phishing-checker-streamlit", "clientVersion": "2.0"},
        "threatInfo": {
            "threatTypes": [
                "MALWARE",
                "SOCIAL_ENGINEERING",
                "UNWANTED_SOFTWARE",
                "POTENTIALLY_HARMFUL_APPLICATION",
            ],
            "platformTypes":    ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries":    [{"url": url}],
        },
    }

    resp = requests.post(endpoint, json=payload, timeout=10)

    if resp.status_code != 200:
        raise ValueError(f"API returned status {resp.status_code}: {resp.text[:200]}")

    try:
        data = resp.json()
    except Exception:
        raise ValueError("Received an invalid response from the API.")

    matches   = data.get("matches", [])
    is_threat = bool(matches)
    threats   = list({m.get("threatType", "UNKNOWN") for m in matches})
    return is_threat, threats


def get_api_key() -> str | None:
    """Read key from Streamlit secrets, fall back to None."""
    try:
        return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        return None


# ── Render Helpers ─────────────────────────────────────────────────────────────

def render_hero():
    st.markdown("""
    <div class="hero">
      <span class="hero-icon">🛡️</span>
      <h1 class="hero-title">Phishing <span>Link</span> Checker</h1>
      <p class="hero-sub">powered by google safe browsing api • v2.0</p>
    </div>
    """, unsafe_allow_html=True)


def render_stats():
    total = len(st.session_state.history)
    safe  = st.session_state.total_safe
    threat = st.session_state.total_threat
    st.markdown(f"""
    <div class="stats-bar">
      <div class="stat-chip">
        <div class="stat-value">{total}</div>
        <div class="stat-label">Total Scans</div>
      </div>
      <div class="stat-chip">
        <div class="stat-value" style="color:#34D399">{safe}</div>
        <div class="stat-label">Safe</div>
      </div>
      <div class="stat-chip">
        <div class="stat-value" style="color:#F87171">{threat}</div>
        <div class="stat-label">Threats</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_result_safe(url: str):
    st.markdown(f"""
    <div class="result-card result-safe">
      <span class="result-icon">✅</span>
      <div class="result-title result-title-safe">URL Appears Safe</div>
      <div class="result-url">{url}</div>
      <p style="color:#6EE7B7;font-size:0.85rem;margin-top:0.8rem;">
        No known threats found in Google's Safe Browsing database.
      </p>
    </div>
    """, unsafe_allow_html=True)


def render_result_threat(url: str, threats: list):
    badges = ""
    for t in threats:
        label, css = THREAT_META.get(t, (t, "badge-harmful"))
        badges += f'<span class="badge {css}">{label}</span>'

    st.markdown(f"""
    <div class="result-card result-threat">
      <span class="result-icon">🚨</span>
      <div class="result-title result-title-threat">Threat Detected!</div>
      <div class="result-url">{url}</div>
      <p style="color:#FCA5A5;font-size:0.85rem;margin-top:0.6rem;">
        Matched {len(threats)} threat {'category' if len(threats)==1 else 'categories'} in Google's database.
      </p>
      <div class="badge-row">{badges}</div>
    </div>
    """, unsafe_allow_html=True)


def render_result_warning(msg: str):
    st.markdown(f"""
    <div class="result-card result-warning">
      <span class="result-icon">⚠️</span>
      <div class="result-title result-title-warn">Warning</div>
      <p style="color:#FCD34D;font-size:0.85rem;margin-top:0.5rem;">{msg}</p>
    </div>
    """, unsafe_allow_html=True)


def render_history():
    history = st.session_state.history
    if not history:
        return

    rows_html = ""
    for item in reversed(history[-15:]):   # show last 15
        sc  = "status-safe"   if item["status"] == "safe" else \
              "status-threat" if item["status"] == "threat" else "status-error"
        label = "✓ Safe" if item["status"] == "safe" else \
                "⚠ Threat" if item["status"] == "threat" else "✕ Error"
        url_short = item["url"][:55] + "…" if len(item["url"]) > 55 else item["url"]
        rows_html += f"""
        <div class="history-row">
          <span class="history-time">{item['time']}</span>
          <span class="history-url">{url_short}</span>
          <span class="history-status {sc}">{label}</span>
        </div>
        """

    st.markdown(f"""
    <div class="history-section">
      <div class="history-title">Scan History</div>
      {rows_html}
    </div>
    """, unsafe_allow_html=True)


# ── Main App ───────────────────────────────────────────────────────────────────

def main():
    render_hero()

    api_key = get_api_key()

    # ── API Key warning ──
    if not api_key:
        st.markdown("""
        <div class="result-card result-warning">
          <span class="result-icon">🔑</span>
          <div class="result-title result-title-warn">API Key Not Configured</div>
          <p style="color:#FCD34D;font-size:0.85rem;margin-top:0.5rem;">
            Add your Google Safe Browsing API key to
            <code>.streamlit/secrets.toml</code> as<br>
            <code>GOOGLE_API_KEY = "your_key_here"</code>
          </p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # ── Stats ──
    if st.session_state.history:
        render_stats()

    # ── Input Card ──
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">🔗 Enter URL to scan</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1.3])
    with col1:
        url_input = st.text_input(
            label="url",
            label_visibility="collapsed",
            placeholder="https://suspicious-site.com",
            key="url_input",
        )
    with col2:
        scan_clicked = st.button("🔍  Scan", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Scan Logic ──
    if scan_clicked:
        if not url_input.strip():
            render_result_warning("Please enter a URL before scanning.")
        else:
            url = normalize_url(url_input)

            if not is_valid_url(url):
                render_result_warning(f'"{url}" does not look like a valid URL. Make sure it includes a domain like <code>example.com</code>.')
            else:
                with st.spinner(f"Scanning {url} …"):
                    try:
                        is_threat, threats = check_safe_browsing(url, api_key)

                        ts = datetime.now().strftime("%H:%M:%S")

                        if is_threat:
                            render_result_threat(url, threats)
                            st.session_state.total_threat += 1
                            st.session_state.history.append({
                                "url": url, "status": "threat", "time": ts
                            })
                        else:
                            render_result_safe(url)
                            st.session_state.total_safe += 1
                            st.session_state.history.append({
                                "url": url, "status": "safe", "time": ts
                            })

                    except requests.exceptions.ConnectionError:
                        render_result_warning("Network error — check your internet connection.")
                        st.session_state.history.append({"url": url, "status": "error", "time": datetime.now().strftime("%H:%M:%S")})

                    except requests.exceptions.Timeout:
                        render_result_warning("The request timed out. Please try again.")
                        st.session_state.history.append({"url": url, "status": "error", "time": datetime.now().strftime("%H:%M:%S")})

                    except ValueError as e:
                        render_result_warning(str(e))
                        st.session_state.history.append({"url": url, "status": "error", "time": datetime.now().strftime("%H:%M:%S")})

                    except Exception as e:
                        render_result_warning(f"Unexpected error: {e}")
                        st.session_state.history.append({"url": url, "status": "error", "time": datetime.now().strftime("%H:%M:%S")})

                # Rerun to refresh the stats bar immediately
                st.rerun()

    # ── History ──
    render_history()

    # ── Footer ──
    st.markdown("""
    <div class="footer">
      phishing-checker • google safe browsing api v4 • not a substitute for full security audits
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

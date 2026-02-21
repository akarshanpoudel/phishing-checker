# 🛡️ Phishing Link Checker

A web app that checks any URL against **Google's Safe Browsing API** to detect malware, phishing, unwanted software, and harmful applications — instantly, in your browser.

**Live demo:** `https://your-app-name.streamlit.app` ← update this after deploying

---

## Features

- ✅ Checks 4 threat categories: Malware, Phishing/Social Engineering, Unwanted Software, Harmful Apps
- 🕐 Per-session scan history with timestamps
- 📊 Live stats (total scans, safe, threats)
- 🌐 Works on any device — no install needed
- 🔒 API key stored securely via Streamlit Secrets

---

## Deploy Your Own (Free)

### 1. Get a Google Safe Browsing API Key
Go to https://developers.google.com/safe-browsing/v4/get-started and create a free key.

### 2. Fork this repo on GitHub

### 3. Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click **New app** → connect your GitHub repo
3. Set **Main file path** to `app.py`
4. Open **Advanced settings → Secrets** and paste:
   ```toml
   GOOGLE_API_KEY = "your_actual_key_here"
   ```
5. Click **Deploy** — you'll get a live public URL in ~60 seconds

---

## Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/phishing-checker
cd phishing-checker
pip install -r requirements.txt

# Create local secrets file
mkdir -p .streamlit
echo 'GOOGLE_API_KEY = "your_key_here"' > .streamlit/secrets.toml

streamlit run app.py
```

---

## Tech Stack

- [Streamlit](https://streamlit.io) — Python web framework
- [Google Safe Browsing API v4](https://developers.google.com/safe-browsing/v4) — threat database
- [Requests](https://requests.readthedocs.io) — HTTP client

---

## ⚠️ Disclaimer

This tool queries Google's Safe Browsing database, which is comprehensive but not exhaustive.
A "safe" result does not guarantee a URL is completely harmless. Always exercise caution with unknown links.

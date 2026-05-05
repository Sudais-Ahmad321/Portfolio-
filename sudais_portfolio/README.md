# Sudais Ahmad — Portfolio (Flask)

## 📁 Project Structure

```
sudais_portfolio/
├── app.py              ← Flask app + /contact API
├── requirements.txt
├── Procfile            ← for Render / Railway / Heroku
├── runtime.txt
└── templates/
    └── index.html      ← Your portfolio page
```

---

## 🚀 Run Locally

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
#    Windows:
venv\Scripts\activate
#    macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## ☁️ Deploy for FREE — 3 Options

### Option A — Render.com (Recommended ⭐)

1. Push code to GitHub
2. Go to https://render.com → New → Web Service
3. Connect your repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Click **Deploy** — you get a live HTTPS URL

---

### Option B — Railway.app

1. Push code to GitHub
2. Go to https://railway.app → New Project → Deploy from GitHub
3. Railway auto-detects Flask and uses your Procfile
4. Your site is live in ~2 minutes

---

### Option C — PythonAnywhere (no GitHub needed)

1. Go to https://www.pythonanywhere.com → Sign up (free)
2. Upload your files via the Files tab
3. Go to **Web** tab → Add new web app → Flask
4. Set the path to `app.py`
5. Reload — done!

---

## 📩 Enable Real Email on Contact Form

Open `app.py` and uncomment the `smtplib` block.
Replace the placeholder Gmail + App Password (generate at
https://myaccount.google.com/apppasswords).

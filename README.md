# 🗣️ Tongues — Culturally Aware Translation

> *Natural, human translation — meaning for meaning, not word for word.*

**[Live App →](https://tongues-9zi1.onrender.com)**

---

## What Is Tongues?

Tongues is a translation app built for people who speak Indian languages — not just people who *read* them.

Most translation tools give you dictionary definitions. Tongues gives you what a real person would actually say. It understands idioms, proverbs, slang, and cultural context across 9 languages.

**The problem it solves:**
Ask Google Translate what *"દૂધનો દાઝેલો છાશ પણ ફૂંકી ફૂંકીને પીએ"* means in English. You'll get gibberish. Tongues gives you *"Once bitten, twice shy"* — because that's what it actually means.

---

## Features

- 🌐 **9 Languages** — English, Hindi, Gujarati, Marathi, Tamil, Telugu, Spanish, German, Japanese
- 🔤 **Romanised Output** — Every non-English translation includes a phonetic pronunciation so anyone can read it aloud
- 🎤 **Voice Input** — Speak instead of type (Chrome on HTTPS)
- 📋 **Copy Buttons** — One click to copy translation or romanised text
- 👍👎 **Feedback** — Thumbs up/down on every translation; thumbs down opens an inline comment box for detailed feedback
- 📊 **Dashboard** — Private analytics at `/dashboard`
- 🧠 **Proverb Database** — SQLite database of culturally verified proverbs with correct meanings
- ↔️ **All 72 directions** — Any language to any language

---

## Why It's Different

| Feature | Google Translate | DeepL | Tongues |
|---------|-----------------|-------|---------|
| Word-for-word translation | ✅ | ✅ | ❌ |
| Cultural meaning | ❌ | ❌ | ✅ |
| Gujarati idioms | ❌ | ❌ | ✅ |
| Romanised phonetic output | ❌ | ❌ | ✅ |
| Proverb knowledge base | ❌ | ❌ | ✅ |
| Tone & cultural notes | ❌ | ❌ | ✅ |
| Pronoun preservation | ❌ | ❌ | ✅ |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3, Flask |
| AI Engine | Anthropic Claude API (claude-sonnet-4) |
| Database | SQLite via Python sqlite3 |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Deployment | Render |
| Version Control | Git / GitHub |

---

## Architecture

```
User (Browser)
     │
     │  GET /          → serves index.html
     │  POST /translate → returns translation JSON
     │  POST /feedback  → logs rating and comment to SQLite
     │  GET /dashboard  → returns analytics dashboard
     ▼
Flask Backend (app.py)
     │
     ├── Validates input
     ├── Checks proverb database for known idioms
     ├── Calls Claude API with V5 system prompt (15 rules)
     ├── Parses TRANSLATION / ROMANISED / CULTURAL_NOTE
     ├── Logs usage stats to SQLite
     └── Returns JSON to browser

SQLite Database (tongues.db)
     ├── proverbs      — culturally verified proverb meanings
     ├── feedback      — thumbs up/down with comment and translation context
     └── usage_stats   — every translation request logged
```

---

## Project Structure

```
tongues-python/
├── app.py                 # Flask backend, routes, Claude API integration
├── database.py            # SQLite setup, proverb lookup, stats logging
├── requirements.txt       # Python dependencies
├── .env                   # API key — never committed (see .gitignore)
├── .gitignore
└── templates/
    ├── index.html         # Full frontend — HTML, CSS, JavaScript
    └── dashboard.html     # Private analytics dashboard
```

---

## System Prompt

Tongues uses a carefully engineered V5 system prompt with 15 rules covering:

- Never translate word for word — always translate meaning and cultural intent
- Language separation firewall — Hindi, Gujarati, and Marathi never bleed into each other
- Idiom and proverb detection — finds the closest natural equivalent, never literal
- Romanised input support — handles typed phonetic input (kem cho, majama, tumhi kase ahat)
- Smart borrowed word handling — keeps pizza, coffee, chocolate as-is
- Pronoun preservation — explicit gender pronouns (she/her, he/him) are always honoured
- Strict output format — TRANSLATION / ROMANISED / CULTURAL_NOTE

---

## Run Locally

```bash
# Clone the repo
git clone https://github.com/avaniupadhyaya/tongues.git
cd tongues

# Install dependencies
pip3 install -r requirements.txt

# Add your Anthropic API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# Run the app
python3 app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## Built By

**Avani Upadhyaya** — AI Linguist & Prompt Engineering Specialist

Native speaker of Gujarati, Hindi, Marathi and English. 7+ years experience in AI language work across Amazon, Google, Meta and LinkedIn.

Tongues was built because every major translation tool consistently fails Indian language speakers — especially for idioms, proverbs, and the natural way people actually talk.

---

*Built with Python, Flask, and the Anthropic Claude API.*

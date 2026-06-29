# 🤖 AI Coding Buddy Pro — v4.0 Analytics Edition

> *Paste your code. Get instant explanations, fixes, quizzes, roadmaps, language conversion, and full learning analytics — powered by Mistral AI + LangChain.*

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.1+-1C3C3C?logo=chainlink&logoColor=white)
![Mistral AI](https://img.shields.io/badge/Mistral-Large-FF7000?logo=mistralai&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.20+-3F4F75?logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 About

**AI Coding Buddy Pro** is an intelligent coding companion built for **engineering students learning to code**. Paste any broken or working code in **Python, Java, C, C++, or JavaScript** and get instant, beginner-friendly help — plus a full analytics dashboard that tracks your progress over time.

---

## 🎯 Features

| # | Tab | What it does |
|---|---|---|
| 1 | 🔍 **Full Analysis** | Deep scan — explains your code, finds every error, gives corrected code, a line-by-line diff, and inline metrics/error charts |
| 2 | ⚡ **Quick Fix** | Paste your exact error message → instant root cause + fix |
| 3 | 📚 **Explain Code** | Line-by-line breakdown — perfect for studying and exam revision |
| 4 | 🧠 **Quiz Me** | Auto-generated 4-question quiz on your code, with scoring + a correct/incorrect chart |
| 5 | 💬 **Chat Tutor** | Free-form chat with an AI tutor, with your code as context |
| 6 | 🗺️ **Roadmap** | Personalized 5-step learning path, skill gauge, known-vs-gaps chart, weekly goals & resources |
| 7 | 🔀 **Compare** | Compare buggy vs. fixed code versions — see what changed, why, and what you learned |
| 8 | ✍️ **Generate Code** | Describe a task → get complete, commented practice code |
| 9 | 📊 **Analytics** | Score-progress line chart, language-usage donut, feature-usage bar chart, error-type breakdown, full session log |
| 10 | 🔄 **Convert Language** | Translate your code into another language with key differences & gotchas explained |
| 11 | 🎯 **Daily Challenge** | Topic-based coding challenges with starter code, hints, and a reveal-to-see solution |
| 12 | 🏆 **Achievements** | 9 unlockable badges (Bug Hunter, Quiz Master, Polyglot, Veteran Coder, etc.) with progress donut |

**Plus:** an XP/score system, daily streaks, session history, a built-in library of buggy code examples per language, and a dark, animated, glassmorphism-style UI throughout.

---

## 🚀 Quick Start

### Step 1 — Clone the project
```bash
git clone https://github.com/yourname/ai-coding-buddy.git
cd ai-coding-buddy
```

### Step 2 — Create a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Get your FREE Mistral AI API Key
1. Go to [https://console.mistral.ai/api-keys](https://console.mistral.ai/api-keys)
2. Sign in or create a Mistral AI account
3. Click **"Create new key"**
4. Copy the key

> ✅ Mistral AI offers a generous free tier — more than enough for student use.

### Step 5 — Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** in your browser.

---

## 🖥️ How to Use

### 🔍 Full Analysis
1. Pick your **language** and **level** in the sidebar
2. Paste your code (or click a built-in buggy example)
3. Click **🚀 Run Full Analysis**
4. Review the metrics chart, error breakdown, explanation, corrected code, and diff

### ⚡ Quick Fix
1. Paste your code **and** the exact error message from your terminal/IDE
2. Click **⚡ Get Quick Fix** for a focused root-cause + fix

### 🧠 Quiz Me
1. Paste your code → **🧠 Generate Quiz**
2. Answer the 4 questions → **✅ Submit Answers**
3. See your score, explanations, and a correct/incorrect chart

### 🗺️ Roadmap
1. Paste your code → **🗺️ Build My Roadmap**
2. Get a skill-quality gauge, a 5-step learning path, weekly goals, and resources

### 🔄 Convert Language
1. Choose **From** / **To** languages
2. Paste your code → **🔄 Convert Code**
3. Review the translated code side-by-side with key differences and gotchas

### 🎯 Daily Challenge
1. Pick a topic (or "Surprise Me")
2. Click **🎲 Get a Challenge**
3. Try the starter code yourself, use hints if stuck, then **👀 Reveal Solution**

### 📊 Analytics & 🏆 Achievements
- Visit anytime to see your score trend, language mix, feature usage, error types, and which badges you've unlocked

---

## 🗂️ Project Structure

```
ai-coding-buddy/
│
├── app.py              # Main Streamlit application (all 12 tabs)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🔧 Tech Stack

| Technology | Purpose |
|---|---|
| **Streamlit** | Web UI framework |
| **LangChain Core** | Prompt templates + LLM chain orchestration |
| **langchain-mistralai** | Mistral AI integration via LangChain |
| **Mistral AI (`mistral-large-latest`)** | Code analysis, fixes, quizzes, roadmaps, conversion, challenges |
| **Plotly** | All interactive charts — line, bar, pie/donut, gauge |
| **PromptTemplate** | Structured prompts for consistent, parseable output |

---

## 🧠 LangChain Architecture

```
User Code / Question
        │
        ▼
PromptTemplate  ──── fills ────▶  Formatted Prompt
        │
        ▼
ChatMistralAI (mistral-large-latest)
        │
        ▼
StrOutputParser
        │
        ▼
Structured ## Sections  or  Raw JSON
        │
        ▼
Streamlit UI + Plotly Charts
```

Dedicated `PromptTemplate`s power each feature:
- `P_FULL` → Full code analysis & fix
- `P_QUICKFIX` → Fast error-message-based fix
- `P_EXPLAIN` → Line-by-line educational breakdown
- `P_QUIZ` → JSON quiz generation
- `P_CHAT` → Conversational tutoring with history
- `P_ROADMAP` → JSON learning roadmap
- `P_COMPARE` → Before/after code comparison
- `P_GENERATE` → Practice code generation
- `P_CONVERT` → Cross-language code translation
- `P_CHALLENGE` → JSON daily coding challenge

---

## 📊 Analytics & Gamification

- **XP / Score system** — every action earns points; level = score ÷ 100
- **Streaks** — tracked across actions in a session
- **Session history** — every analysis, fix, or roadmap is logged with timestamp
- **Charts** — score progression (line), language usage (donut), feature usage (bar), error types (bar), quiz results (donut), code-quality gauge, known-vs-gaps comparison
- **Achievements** — 9 badges with live unlock-state tracking based on your session stats

---

## 📸 UI Highlights

- 🌑 Deep dark theme with animated gradient hero banner
- 🃏 Glassmorphism-style cards for errors, fixes, tips, and badges
- 💻 JetBrains Mono for all code blocks
- 📈 Dark-themed Plotly charts matching the app's color palette
- 📱 Responsive multi-column layout across all 12 tabs

---

## ⚙️ Environment Variables (Optional)

Instead of entering your API key in the UI every time, set it as an environment variable and read it as a default:

```bash
# Linux/macOS
export MISTRAL_API_KEY="your-key-here"

# Windows CMD
set MISTRAL_API_KEY=your-key-here

# Windows PowerShell
$env:MISTRAL_API_KEY="your-key-here"
```

Then in `app.py`:
```python
import os
default_key = os.getenv("MISTRAL_API_KEY", "")
```

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|---|---|
| `Unauthorized` / `401` | Double-check you copied the full API key from the Mistral console |
| `rate limit exceeded` | You've hit the free tier limit — wait a bit and retry |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again inside the venv |
| App won't open | Make sure you're in the right folder and the venv is activated |
| Charts not showing | Make sure `plotly` installed correctly (`pip show plotly`) |
| Blank result | Your code box might be empty — paste code before clicking the action button |

---

## 🗺️ Roadmap / Future Ideas

- [ ] Support for **more languages** (SQL, Go, Rust)
- [ ] **Persistent history** across sessions (currently per-session only)
- [ ] **Voice explanation** — read out errors aloud
- [ ] **Team/classroom leaderboard** mode
- [ ] **Dark/Light theme toggle**
- [ ] **Export reports** (PDF/Markdown) of your analyses

---

## 👨‍💻 Made For

Engineering students in **Semester I–IV** learning to code, especially those studying:
- **B.Tech CSE/CST/IT** — Python, Java, C, C++, JavaScript programs
- **Lab assignments** — debug quickly and understand why
- **Exam prep** — understand concepts through real code examples and quizzes
- **Self-paced learners** — track progress with analytics and earn badges along the way

---

## 📄 License

MIT License — free to use, modify, and distribute for educational purposes.

---

<div align="center">
Built with ❤️ using Streamlit + LangChain + Mistral AI + Plotly<br>
<em>Because every error is a lesson waiting to be learned.</em>
</div>


https://ai-coding-buddy-jnecfcot4tnrd8zyce4wum.streamlit.app/- The link of the app.

# ╔══════════════════════════════════════════════════════════════════╗
# ║          AI CODING BUDDY PRO  v4.0  — ANALYTICS EDITION         ║
# ║   Streamlit + LangChain Core + Mistral AI + Plotly              ║
# ║   12 Tabs · Quiz · Chat · Roadmap · Diff · Convert · Analytics  ║
# ╚══════════════════════════════════════════════════════════════════╝

import streamlit as st
import re, json, datetime
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ── PAGE CONFIG ────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Coding Buddy Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ─ RESET & ROOT ─ */
:root{
  --bg:#060b14; --bg2:#0c1220; --bg3:#111827; --bg4:#1a2540;
  --blue:#3b82f6; --cyan:#06b6d4; --green:#10b981;
  --purple:#8b5cf6; --orange:#f59e0b; --red:#ef4444; --pink:#ec4899;
  --txt:#f1f5f9; --txt2:#94a3b8; --txt3:#475569;
  --border:#1a2840; --border2:#243450;
  --mono:'JetBrains Mono',monospace;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}
html,body,[data-testid="stAppViewContainer"]{
  background:var(--bg) !important;
  font-family:'Inter',sans-serif;
  color:var(--txt);
}
[data-testid="stSidebar"]{
  background:var(--bg2) !important;
  border-right:1px solid var(--border);
}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stDecoration"]{display:none;}
.block-container{padding-top:1.4rem !important; padding-bottom:3rem !important;}

/* ─ ANIMATIONS ─ */
@keyframes gradShift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes orbit{from{transform:rotate(0deg) translateX(90px) rotate(0deg)}to{transform:rotate(360deg) translateX(90px) rotate(-360deg)}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(59,130,246,.5)}70%{box-shadow:0 0 0 10px rgba(59,130,246,0)}}
@keyframes scanline{0%{top:-5%}100%{top:105%}}
@keyframes typewriter{from{width:0}to{width:100%}}

/* ─ HERO ─ */
.hero{
  background:linear-gradient(135deg,#070e1f 0%,#0d0b2e 50%,#060e1e 100%);
  border:1px solid var(--border2);
  border-radius:28px;
  padding:44px 52px;
  margin-bottom:28px;
  position:relative;
  overflow:hidden;
  animation:fadeUp .6s ease both;
}
.hero-scan{
  position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(to bottom,transparent,rgba(59,130,246,.03),transparent);
  height:60px;width:100%;
  animation:scanline 3s linear infinite;
}
.orb{position:absolute;border-radius:50%;pointer-events:none;}
.orb1{width:320px;height:320px;top:-100px;right:-80px;
  background:radial-gradient(circle,rgba(59,130,246,.18),transparent 65%);}
.orb2{width:220px;height:220px;bottom:-70px;left:60px;
  background:radial-gradient(circle,rgba(139,92,246,.15),transparent 65%);}
.orb3{width:160px;height:160px;top:40%;left:-50px;
  background:radial-gradient(circle,rgba(6,182,212,.12),transparent 65%);}
.hero-eye{
  font-size:.72rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;
  color:var(--cyan);margin-bottom:14px;display:flex;align-items:center;gap:8px;
}
.hero-eye::before{content:'';display:inline-block;width:28px;height:2px;background:var(--cyan);}
.hero-title{
  font-size:3rem;font-weight:900;letter-spacing:-1.5px;
  line-height:1.05;margin-bottom:14px;
  background:linear-gradient(90deg,#60a5fa,#06b6d4,#a78bfa,#60a5fa);
  background-size:300%;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:gradShift 5s ease infinite;
}
.hero-sub{color:var(--txt2);font-size:1.05rem;max-width:580px;line-height:1.7;margin-bottom:26px;}
.hero-pills{display:flex;gap:8px;flex-wrap:wrap;}
.hp{
  padding:5px 14px;border-radius:20px;font-size:.72rem;font-weight:700;
  font-family:var(--mono);letter-spacing:.5px;
}
.hp-py{background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.4);color:#34d399;}
.hp-jv{background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.4);color:#fbbf24;}
.hp-c {background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.4);color:#60a5fa;}
.hp-cp{background:rgba(6,182,212,.12); border:1px solid rgba(6,182,212,.4); color:#22d3ee;}
.hp-js{background:rgba(234,179,8,.12); border:1px solid rgba(234,179,8,.4); color:#facc15;}
.hp-ai{background:rgba(139,92,246,.12);border:1px solid rgba(139,92,246,.4);color:#a78bfa;}

/* ─ STATS STRIP ─ */
.stats-strip{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:24px;}
.stat-box{
  background:var(--bg3);border:1px solid var(--border);border-radius:14px;
  padding:16px 22px;flex:1;min-width:100px;animation:fadeUp .5s ease both;
}
.stat-box .sv{
  font-size:1.8rem;font-weight:900;font-family:var(--mono);
  background:linear-gradient(90deg,var(--blue),var(--cyan));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.stat-box .sl{font-size:.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--txt3);margin-top:2px;}

/* ─ SECTION LABEL ─ */
.lbl{
  font-size:.68rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;
  color:var(--cyan);margin-bottom:8px;display:flex;align-items:center;gap:8px;
}
.lbl::after{content:'';flex:1;height:1px;background:var(--border);}

/* ─ CARDS ─ */
.card{
  background:var(--bg3);border:1px solid var(--border);
  border-radius:16px;padding:20px;margin-bottom:14px;
  transition:border-color .2s,transform .15s;
  animation:fadeUp .4s ease both;
}
.card:hover{border-color:var(--border2);}

/* ─ RESULT BLOCKS ─ */
.rb{
  background:var(--bg2);border:1px solid var(--border);
  border-left:3px solid var(--blue);border-radius:12px;
  padding:16px 20px;margin-bottom:12px;font-size:.9rem;
  line-height:1.8;color:var(--txt);animation:fadeUp .3s ease both;
}
.rb.e{border-left-color:var(--red);}
.rb.g{border-left-color:var(--green);}
.rb.p{border-left-color:var(--purple);}
.rb.o{border-left-color:var(--orange);}
.rb h4{font-size:.8rem;font-weight:700;margin-bottom:10px;display:flex;align-items:center;gap:7px;}
.rb.e h4{color:var(--red);}
.rb.g h4{color:var(--green);}
.rb.p h4{color:var(--purple);}
.rb.o h4{color:var(--orange);}
.rb   h4{color:var(--blue);}
.dot{width:7px;height:7px;border-radius:50%;display:inline-block;animation:blink 2s ease infinite;flex-shrink:0;}
.rb.e .dot{background:var(--red);}
.rb.g .dot{background:var(--green);}
.rb.p .dot{background:var(--purple);}
.rb.o .dot{background:var(--orange);}
.rb   .dot{background:var(--blue);}

/* ─ DIFF ─ */
.diff-add{font-family:var(--mono);font-size:.83rem;padding:3px 10px;border-radius:5px;margin:2px 0;
  background:rgba(16,185,129,.12);color:#6ee7b7;display:block;}
.diff-del{font-family:var(--mono);font-size:.83rem;padding:3px 10px;border-radius:5px;margin:2px 0;
  background:rgba(239,68,68,.1);color:#fca5a5;text-decoration:line-through;display:block;}
.diff-ctx{font-family:var(--mono);font-size:.83rem;padding:2px 10px;color:var(--txt3);display:block;}

/* ─ CHAT BUBBLES ─ */
.cb{border-radius:18px;padding:14px 18px;margin-bottom:10px;font-size:.9rem;line-height:1.7;animation:fadeUp .3s ease both;}
.cb.u{background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.25);margin-left:32px;}
.cb.a{background:var(--bg3);border:1px solid var(--border);margin-right:32px;}
.cb .who{font-size:.68rem;font-weight:800;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px;}
.cb.u .who{color:var(--blue);}
.cb.a .who{color:var(--cyan);}

/* ─ QUIZ ─ */
.qbox{background:var(--bg3);border:1px solid var(--border2);border-radius:16px;padding:22px;margin-bottom:16px;animation:fadeUp .4s ease both;}
.qnum{font-size:.72rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--purple);margin-bottom:6px;}
.qtxt{font-size:.97rem;font-weight:600;color:var(--txt);margin-bottom:14px;line-height:1.5;}

/* ─ ROADMAP ─ */
.rstep{display:flex;gap:16px;align-items:flex-start;padding:16px 0;border-bottom:1px solid var(--border);}
.rstep:last-child{border-bottom:none;}
.rnum{width:34px;height:34px;border-radius:50%;flex-shrink:0;
  display:flex;align-items:center;justify-content:center;
  font-size:.78rem;font-weight:800;font-family:var(--mono);}
.rdone{background:rgba(16,185,129,.2);border:1px solid rgba(16,185,129,.5);color:#34d399;}
.rcurr{background:rgba(59,130,246,.2);border:1px solid rgba(59,130,246,.5);color:#60a5fa;animation:pulse 2s ease infinite;}
.rnext{background:var(--bg3);border:1px solid var(--border);color:var(--txt3);}

/* ─ LEVEL BADGE ─ */
.lvl{display:inline-flex;align-items:center;gap:6px;padding:4px 14px;border-radius:20px;font-size:.75rem;font-weight:700;}
.lvl-b{background:rgba(16,185,129,.15);border:1px solid rgba(16,185,129,.4);color:#34d399;}
.lvl-i{background:rgba(245,158,11,.15);border:1px solid rgba(245,158,11,.4);color:#fbbf24;}
.lvl-a{background:rgba(239,68,68,.15); border:1px solid rgba(239,68,68,.4); color:#f87171;}

/* ─ LIVE DOT ─ */
.ldot{display:inline-block;width:8px;height:8px;background:var(--green);
  border-radius:50%;margin-right:5px;animation:blink 1.6s ease infinite;}

/* ─ PROGRESS BAR ─ */
.pbwrap{background:var(--bg2);border-radius:99px;height:6px;overflow:hidden;margin:6px 0;}
.pbfill{height:100%;border-radius:99px;transition:width .6s ease;}

/* ─ SIDEBAR ─ */
.sblogo{text-align:center;padding:18px 0 22px;border-bottom:1px solid var(--border);margin-bottom:18px;}
.sblogo .ico{font-size:2.6rem;}
.sblogo .nm{
  font-size:1.1rem;font-weight:900;display:block;margin-top:6px;
  background:linear-gradient(90deg,#60a5fa,#06b6d4);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}
.sblogo .vr{font-size:.68rem;color:var(--txt3);}
.sbs{
  background:var(--bg3);border:1px solid var(--border);
  border-radius:11px;padding:12px 14px;margin-bottom:8px;
  display:flex;align-items:center;gap:10px;
}
.sbs .si{font-size:1.3rem;}
.sbs .sv{font-size:1.1rem;font-weight:800;color:var(--txt);}
.sbs .sl{font-size:.67rem;color:var(--txt3);text-transform:uppercase;letter-spacing:1px;}

/* ─ CODE CONCEPT CHIP ─ */
.chip{
  display:inline-block;padding:3px 10px;border-radius:99px;margin:3px;
  font-size:.75rem;font-weight:600;
  background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.3);color:#60a5fa;
}

/* ─ BADGES ─ */
.badge-card{transition:transform .15s ease;}
.badge-card:hover{transform:translateY(-3px);}

/* ─ STREAMLIT OVERRIDES ─ */
.stTextArea textarea{
  background:var(--bg2) !important;color:#e2e8f0 !important;
  border:1px solid var(--border) !important;border-radius:12px !important;
  font-family:var(--mono) !important;font-size:.87rem !important;
  line-height:1.65 !important;padding:14px !important;
}
.stTextArea textarea:focus{border-color:var(--blue) !important;box-shadow:0 0 0 3px rgba(59,130,246,.15) !important;}
.stSelectbox [data-baseweb="select"]>div{
  background:var(--bg2) !important;border-color:var(--border) !important;
  border-radius:10px !important;color:var(--txt) !important;
}
.stButton>button{
  background:linear-gradient(135deg,#3b82f6,#6d28d9) !important;
  color:#fff !important;border:none !important;border-radius:11px !important;
  padding:11px 24px !important;font-size:.93rem !important;font-weight:700 !important;
  width:100% !important;letter-spacing:.3px !important;transition:opacity .2s !important;
}
.stButton>button:hover{opacity:.85 !important;}
.stTabs [data-baseweb="tab-list"]{
  background:var(--bg2) !important;
  border:1px solid var(--border) !important;
  border-radius:14px !important;padding:4px !important;gap:2px !important;
  flex-wrap:wrap !important;
}
.stTabs [data-baseweb="tab"]{
  background:transparent !important;border-radius:10px !important;
  color:var(--txt2) !important;font-weight:600 !important;font-size:.83rem !important;
  padding:9px 16px !important;border:none !important;
}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,rgba(59,130,246,.22),rgba(139,92,246,.22)) !important;
  color:var(--txt) !important;border:1px solid rgba(59,130,246,.3) !important;
}
.stTabs [data-baseweb="tab-panel"]{padding-top:20px !important;}
.stExpander{background:var(--bg3) !important;border:1px solid var(--border) !important;border-radius:12px !important;}
.stExpander summary{color:var(--txt2) !important;}
.stAlert{border-radius:11px !important;}
[data-testid="stFileUploader"]{
  background:var(--bg3) !important;border:1px dashed var(--border2) !important;
  border-radius:12px !important;
}
::-webkit-scrollbar{width:5px;height:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:#1e2d45;border-radius:3px;}
</style>
""", unsafe_allow_html=True)


# ── SESSION STATE ──────────────────────────────────────────────────
DEFAULTS = dict(
    api_key="", analysis_count=0, history=[], last_result=None,
    chat_history=[], quiz_data=None, quiz_answers={},
    quiz_submitted=False, score=0, total_errors=0, streak=0,
    uploaded_code="", roadmap_data=None,
    # New in v4.0 — analytics & extra features
    error_types={}, lang_usage={}, mode_usage={}, score_log=[],
    challenge_data=None, challenge_revealed=False,
)
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── LLM FACTORY ───────────────────────────────────────────────────
def get_llm():
    return ChatMistralAI(
        model="mistral-large-latest",
        api_key=st.session_state.api_key,
        temperature=0.3,
        max_tokens=4096,
    )

_parser = StrOutputParser()

def run(prompt_tpl, **kw):
    chain = prompt_tpl | get_llm() | _parser
    return chain.invoke(kw)


# ── PLOTLY THEME HELPERS ───────────────────────────────────────────
PLOTLY_COLORS = ["#3b82f6","#06b6d4","#8b5cf6","#10b981","#f59e0b","#ef4444","#ec4899","#94a3b8"]

def style_fig(fig, height=320):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#f1f5f9", size=12),
        height=height,
        margin=dict(l=10, r=10, t=36, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig


# ── PROMPTS ───────────────────────────────────────────────────────
P_FULL = PromptTemplate(input_variables=["lang","code","level"], template="""
You are a world-class coding mentor helping a {level} engineering student.

Language: {lang}
Code:
```{lang}
{code}
```

Reply using EXACTLY these ## headers:

## 🔍 WHAT YOUR CODE DOES
2-3 simple sentences using everyday analogies.

## 📊 CODE METRICS
- Complexity: BEGINNER / INTERMEDIATE / ADVANCED
- Lines of Code: <number>
- Functions/Methods: <number>
- Logic Depth: Simple / Medium / Complex
- Estimated Fix Time: <X minutes for a beginner>

## ❌ ERRORS FOUND
For EACH error:
- LINE: <line number or 'general'>
- TYPE: <Syntax/Logic/Runtime/Semantic/Style>
- PROBLEM: <explain like talking to a 15-year-old>
- WHY IT FAILS: <1 sentence technical reason>
- ANALOGY: <memorable real-world analogy>

If none: write "✅ No errors — your code looks correct!"

## ✅ CORRECTED CODE
Full corrected working code in triple backticks with inline comments on every changed line.

## 🔀 WHAT CHANGED (DIFF)
For each change:
OLD: <original line>
NEW: <corrected line>
WHY: <one sentence reason>

## 🏆 WHAT YOU DID WELL
2 specific things the student got right. Be genuine and encouraging.

## 💡 BEGINNER TIPS
3 numbered actionable tips based on mistakes seen.

## 🚀 NEXT CONCEPT TO LEARN
Topic: <name>
Why: <1 sentence>
Challenge: <a small coding exercise to try>
""")

P_QUICKFIX = PromptTemplate(input_variables=["lang","code","err"], template="""
Fast fix for a beginner student.
Language: {lang}
Code:
```{lang}
{code}
```
Error message: {err}

## ⚡ ROOT CAUSE
One sentence: exactly what went wrong and why.

## 🔧 FIXED CODE
Corrected working code in triple backticks. Comment every changed line.

## 📖 PLAIN ENGLISH
Explain in 3 sentences why this error happened. Use a real-world analogy.

## ✋ PREVENT NEXT TIME
2 bullet points: how to avoid this error in future code.
""")

P_EXPLAIN = PromptTemplate(input_variables=["lang","code"], template="""
Explain this code to a complete beginner.
Language: {lang}
Code:
```{lang}
{code}
```

## 📋 ONE-LINE SUMMARY
What does this code do in one sentence?

## 🔢 LINE-BY-LINE BREAKDOWN
For each line or logical block (use format):
[LINE X] <code> → <plain English meaning>

## 🔑 KEY CONCEPTS USED
For each concept:
CONCEPT: <name>
DEFINITION: <1-sentence beginner explanation>
USED HERE: <how it appears in this specific code>

## ✅ GOOD PRACTICES SPOTTED
What the student did well.

## 🛠️ SUGGESTED IMPROVEMENTS
2-3 specific improvements with beginner-friendly explanations.
""")

P_QUIZ = PromptTemplate(input_variables=["lang","code"], template="""
Create 4 multiple-choice quiz questions for a beginner student about this {lang} code:
```{lang}
{code}
```

Return ONLY raw JSON — no markdown fences, no explanation, just the JSON array:
[
  {{"q":"Question?","options":["A","B","C","D"],"answer":0,"explanation":"Why correct."}}
]
answer must be index 0-3. Test: output values, error identification, variable values, logic understanding.
""")

P_CHAT = PromptTemplate(input_variables=["lang","code","history","question"], template="""
You are a warm, patient coding tutor for beginners.
Language context: {lang}
Code being discussed:
```{lang}
{code}
```
Recent conversation:
{history}

Student asks: {question}

Reply in simple, encouraging language. Max 180 words. Show code snippet if helpful.
Always end with a gentle follow-up question or encouragement.
""")

P_ROADMAP = PromptTemplate(input_variables=["lang","code","level"], template="""
Analyze this {lang} code from a {level} student and build a learning roadmap.
```{lang}
{code}
```

Return ONLY raw JSON, no fences:
{{
  "level": "Beginner/Intermediate/Advanced",
  "score": <1-10 code quality score>,
  "known": ["concept1","concept2","concept3"],
  "gaps": ["gap1","gap2","gap3"],
  "roadmap": [
    {{"step":1,"topic":"Topic","desc":"1 sentence","status":"done"}},
    {{"step":2,"topic":"Topic","desc":"1 sentence","status":"done"}},
    {{"step":3,"topic":"Topic","desc":"1 sentence","status":"current"}},
    {{"step":4,"topic":"Topic","desc":"1 sentence","status":"next"}},
    {{"step":5,"topic":"Topic","desc":"1 sentence","status":"next"}}
  ],
  "weekly_goal": "Specific achievable goal this week",
  "daily_practice": "One 15-minute daily practice suggestion",
  "resources": ["Resource 1","Resource 2","Resource 3"],
  "motivational_message": "Short encouraging message for the student"
}}
""")

P_COMPARE = PromptTemplate(input_variables=["lang","v1","v2"], template="""
Compare two {lang} code versions for a beginner student.
Version A (original):
```{lang}
{v1}
```
Version B (improved):
```{lang}
{v2}
```

## 📊 IMPROVEMENT SCORE
Rate improvement: X/10. One sentence explaining the rating.

## 🔀 ALL CHANGES
For each difference:
- WHAT: <what changed>
- WHY BETTER: <simple reason>
- SKILL LEARNED: <programming concept this teaches>

## 📈 SKILLS GAINED
What programming skills does fixing this code teach?

## ⚡ PERFORMANCE
Any speed/memory improvement? Explain for beginners.

## 🎯 FINAL VERDICT
1 paragraph summary: how much progress was made and what to focus on next.
""")

P_GENERATE = PromptTemplate(input_variables=["lang","task","level"], template="""
You are helping a {level} student learn {lang} by generating practice code.

Task: {task}

Generate a complete, working {lang} program that:
1. Solves the task correctly
2. Has detailed comments explaining every line
3. Uses concepts appropriate for a {level} student
4. Includes a brief explanation of how it works

## 📝 CODE
Full working code in triple backticks.

## 🔍 HOW IT WORKS
Step-by-step explanation in simple language.

## 🎯 KEY CONCEPTS USED
List 3-5 concepts this code teaches.

## 🚀 CHALLENGE EXTENSION
One way to extend/modify this code to practice more.
""")

P_CONVERT = PromptTemplate(input_variables=["from_lang","to_lang","code"], template="""
Convert the following {from_lang} code into idiomatic, working {to_lang} code for a student
who already understands {from_lang} but is new to {to_lang}.

{from_lang} code:
```{from_lang}
{code}
```

Reply using EXACTLY these ## headers:

## 🔄 CONVERTED CODE
Full working {to_lang} code in triple backticks, with comments on any non-obvious lines.

## 🔑 KEY DIFFERENCES
3-5 bullet points on syntax/concept differences between {from_lang} and {to_lang} relevant to this code.

## ⚠️ GOTCHAS
1-2 things a student should watch out for when moving from {from_lang} to {to_lang}.
""")

P_CHALLENGE = PromptTemplate(input_variables=["lang","level","topic"], template="""
Create one fresh, original coding challenge in {lang} for a {level} student.
Topic focus: {topic} (if topic is "Surprise Me", pick any fundamental topic).

Return ONLY raw JSON, no markdown fences:
{{
  "title": "Short challenge title",
  "difficulty": "Easy/Medium/Hard",
  "problem": "Clear problem statement, 2-4 sentences",
  "starter_code": "starter code with TODO comments for the student to fill in",
  "hints": ["hint1","hint2","hint3"],
  "solution": "full working solution code, well commented",
  "explanation": "2-3 sentence explanation of the approach used in the solution"
}}
""")


# ── HELPERS ───────────────────────────────────────────────────────
def render_sections(text):
    """Parse ## sections and render styled blocks."""
    sections = text.split("##")
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        parts = sec.split("\n", 1)
        header = parts[0].strip()
        body   = parts[1].strip() if len(parts) > 1 else ""
        if not header:
            continue
        hu = header.upper()
        cls = ("e" if any(x in hu for x in ["ERROR","❌","WRONG","ISSUE","CAUSE","ROOT"])
          else "g" if any(x in hu for x in ["CORRECT","✅","FIX","GOOD","WELL","SOLUTION","SUMMARY","HOW IT WORK"])
          else "p" if any(x in hu for x in ["TIP","NEXT","LEARN","CONCEPT","SKILL","CHALLENGE","VERDICT","DAILY","WEEK"])
          else "o" if any(x in hu for x in ["METRIC","CHANGE","DIFF","PERFORM","SCORE","IMPROVE","PREVENT","AVOID","WARN","GOTCHA","DIFFERENCE"])
          else "")
        body_html = (body.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
                        .replace("\n","<br>"))
        st.markdown(f"""
        <div class="rb {cls}">
          <h4><span class="dot"></span>{header}</h4>
          <div>{body_html}</div>
        </div>""", unsafe_allow_html=True)

def extract_code_blocks(text):
    return re.findall(r'```(?:\w+)?\n(.*?)```', text, re.DOTALL)

def error_count(text):
    return max(text.count("LINE:"), text.upper().count("TYPE:"))

def track_error_types(text):
    """Extract TYPE: <error type> lines and log them for the Analytics dashboard."""
    found = re.findall(r'TYPE:\s*([A-Za-z/ ]+)', text)
    for t in found:
        clean = t.strip().split("/")[0].split("\n")[0].strip().title()
        if clean:
            st.session_state.error_types[clean] = st.session_state.error_types.get(clean, 0) + 1

def log_error_type_manual(label):
    label = (label or "Unknown").strip().title()
    if not label:
        label = "Unknown"
    st.session_state.error_types[label] = st.session_state.error_types.get(label, 0) + 1

def parse_metrics(text):
    loc   = re.search(r'Lines of Code:\s*\**(\d+)', text)
    funcs = re.search(r'Functions/Methods:\s*\**(\d+)', text)
    out = {}
    if loc:   out["Lines of Code"] = int(loc.group(1))
    if funcs: out["Functions"]     = int(funcs.group(1))
    return out

def save_history(lang, mode, code):
    st.session_state.history.append({
        "n": st.session_state.analysis_count,
        "lang": lang, "mode": mode,
        "time": datetime.datetime.now().strftime("%H:%M"),
        "snippet": code[:55] + "…"
    })
    st.session_state.lang_usage[lang] = st.session_state.lang_usage.get(lang, 0) + 1
    st.session_state.mode_usage[mode] = st.session_state.mode_usage.get(mode, 0) + 1
    st.session_state.score_log.append({"n": st.session_state.analysis_count, "score": st.session_state.score})

def need_key():
    if not st.session_state.api_key:
        st.error("🔑 Enter your Mistral API key in the sidebar first!")
        return True
    return False


# ── ACHIEVEMENTS / BADGES ─────────────────────────────────────────
BADGES = [
    {"id":"first_step", "name":"First Step",     "icon":"🎯", "desc":"Run your first analysis",
     "cond": lambda s: s.get("analysis_count", 0) >= 1},
    {"id":"bug_hunter",  "name":"Bug Hunter",      "icon":"🐛", "desc":"Catch 10 bugs total",
     "cond": lambda s: s.get("total_errors", 0) >= 10},
    {"id":"on_fire",     "name":"On Fire",         "icon":"🔥", "desc":"Reach a 5-action streak",
     "cond": lambda s: s.get("streak", 0) >= 5},
    {"id":"scholar",     "name":"Scholar",         "icon":"⭐", "desc":"Score 100 points",
     "cond": lambda s: s.get("score", 0) >= 100},
    {"id":"quiz_master", "name":"Quiz Master",     "icon":"🧠", "desc":"Get a perfect quiz score",
     "cond": lambda s: bool(s.get("quiz_submitted")) and bool(s.get("quiz_data")) and
        all(s.get("quiz_answers", {}).get(i) == q["answer"] for i, q in enumerate(s.get("quiz_data") or []))},
    {"id":"polyglot",    "name":"Polyglot",        "icon":"🌐", "desc":"Use 3 different languages",
     "cond": lambda s: len(s.get("lang_usage", {})) >= 3},
    {"id":"explorer",    "name":"Explorer",        "icon":"🧭", "desc":"Try 5 different features",
     "cond": lambda s: len(s.get("mode_usage", {})) >= 5},
    {"id":"veteran",     "name":"Veteran Coder",   "icon":"🏆", "desc":"Reach Level 5 (500 score)",
     "cond": lambda s: s.get("score", 0) >= 500},
    {"id":"converter",   "name":"Code Whisperer",  "icon":"🔄", "desc":"Convert code to another language",
     "cond": lambda s: s.get("mode_usage", {}).get("Convert", 0) >= 1},
]


# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sblogo">
      <div class="ico">🤖</div>
      <span class="nm">AI Coding Buddy Pro</span>
      <div class="vr">v4.0 · Mistral AI · LangChain · Plotly</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("#### 🔑 Mistral API Key")
    k = st.text_input("key", type="password", placeholder="Your Mistral API key…",
                      value=st.session_state.api_key, label_visibility="collapsed")
    if k:
        st.session_state.api_key = k
        st.markdown('<p style="color:#34d399;font-size:.8rem;margin-top:4px"><span class="ldot"></span>Connected — Ready</p>',
                    unsafe_allow_html=True)
    else:
        st.warning("Paste your free Mistral API key")
        st.markdown("[Get free key →](https://console.mistral.ai/api-keys)")

    st.markdown("---")
    st.markdown("#### ⚙️ Settings")
    language = st.selectbox("Language", ["Python","Java","C","C++","JavaScript"])
    level    = st.selectbox("Your Level", ["🟢 Complete Beginner","🟡 Some Experience","🔴 Intermediate"])

    st.markdown("---")
    st.markdown("#### 📂 Upload Code File")
    up = st.file_uploader("Upload", type=["py","java","c","cpp","js","txt"],
                          label_visibility="collapsed")
    if up:
        st.session_state.uploaded_code = up.read().decode("utf-8", errors="ignore")
        st.success(f"✅ {up.name} loaded!")

    st.markdown("---")
    st.markdown("#### 📊 Your Stats")
    c1,c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="sbs"><div class="si">🔍</div><div><div class="sv">{st.session_state.analysis_count}</div><div class="sl">Analyses</div></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sbs"><div class="si">🔥</div><div><div class="sv">{st.session_state.streak}</div><div class="sl">Streak</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="sbs"><div class="si">🐛</div><div><div class="sv">{st.session_state.total_errors}</div><div class="sl">Bugs Fixed</div></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sbs"><div class="si">⭐</div><div><div class="sv">{st.session_state.score}</div><div class="sl">Score</div></div></div>', unsafe_allow_html=True)

    # XP progress bar
    xp_pct = min((st.session_state.score % 100), 100)
    xp_lvl = st.session_state.score // 100
    st.markdown(f"""
    <div style="margin-top:4px">
      <div style="display:flex;justify-content:space-between;font-size:.7rem;color:var(--txt3);margin-bottom:3px">
        <span>Level {xp_lvl}</span><span>{xp_pct}/100 XP</span>
      </div>
      <div class="pbwrap"><div class="pbfill" style="width:{xp_pct}%;background:linear-gradient(90deg,var(--blue),var(--cyan))"></div></div>
    </div>""", unsafe_allow_html=True)

    # Mini language-usage donut, only once there's data
    if st.session_state.lang_usage:
        st.markdown("---")
        st.markdown("#### 🌐 Language Mix")
        mini = px.pie(names=list(st.session_state.lang_usage.keys()),
                      values=list(st.session_state.lang_usage.values()),
                      hole=.55, color_discrete_sequence=PLOTLY_COLORS)
        mini.update_traces(textinfo="none")
        mini.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.15, font=dict(size=9)))
        st.plotly_chart(style_fig(mini, height=200), use_container_width=True)

    st.markdown("---")
    if st.button("🗑️ Reset Session"):
        for k2, v2 in DEFAULTS.items():
            st.session_state[k2] = v2
        st.rerun()


# ── HERO ──────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-scan"></div>
  <div class="orb orb1"></div><div class="orb orb2"></div><div class="orb orb3"></div>
  <div class="hero-eye">Engineering Student Assistant · AI Powered · Free to Use</div>
  <div class="hero-title">AI Coding Buddy Pro</div>
  <div class="hero-sub">
    Paste broken code → get instant explanations, auto-fixes, line-by-line diffs,
    interactive quizzes, AI chat tutoring, personalized roadmaps, language conversion,
    daily challenges, and full learning analytics.
  </div>
  <div class="hero-pills">
    <span class="hp hp-py">🐍 Python</span>
    <span class="hp hp-jv">☕ Java</span>
    <span class="hp hp-c">⚙️ C</span>
    <span class="hp hp-cp">🔵 C++</span>
    <span class="hp hp-js">💛 JavaScript</span>
    <span class="hp hp-ai">✨ Mistral AI</span>
    <span class="hp hp-ai">🔗 LangChain</span>
    <span class="hp hp-ai">📊 Plotly</span>
  </div>
</div>""", unsafe_allow_html=True)

# ── STATS STRIP ───────────────────────────────────────────────────
st.markdown(f"""
<div class="stats-strip">
  <div class="stat-box"><div class="sv">{st.session_state.analysis_count}</div><div class="sl">Analyses Run</div></div>
  <div class="stat-box"><div class="sv">{st.session_state.total_errors}</div><div class="sl">Bugs Caught</div></div>
  <div class="stat-box"><div class="sv">{len(st.session_state.history)}</div><div class="sl">Sessions</div></div>
  <div class="stat-box"><div class="sv">{st.session_state.streak}🔥</div><div class="sl">Streak</div></div>
  <div class="stat-box"><div class="sv">{st.session_state.score}⭐</div><div class="sl">Score</div></div>
  <div class="stat-box"><div class="sv">Lv {st.session_state.score//100}</div><div class="sl">Level</div></div>
</div>""", unsafe_allow_html=True)


# ── TABS ──────────────────────────────────────────────────────────
T = st.tabs([
    "🔍 Full Analysis",
    "⚡ Quick Fix",
    "📚 Explain Code",
    "🧠 Quiz Me",
    "💬 Chat Tutor",
    "🗺️ Roadmap",
    "🔀 Compare",
    "✍️ Generate Code",
    "📊 Analytics",
    "🔄 Convert Language",
    "🎯 Daily Challenge",
    "🏆 Achievements",
])


# ════════════════════════════════════════════════════════════════════
# TAB 1 ── FULL ANALYSIS
# ════════════════════════════════════════════════════════════════════
with T[0]:
    st.markdown('<div class="lbl">📝 Paste Your Code</div>', unsafe_allow_html=True)
    left, right = st.columns([3,2], gap="large")

    with left:
        code1 = st.text_area("c1", height=300,
            value=st.session_state.uploaded_code,
            placeholder=f"# Paste your {language} code here — errors are welcome! 😊",
            label_visibility="collapsed")
        run1 = st.button("🚀 Run Full Analysis", key="b1")

    with right:
        st.markdown('<div class="lbl">💡 Example Bugs</div>', unsafe_allow_html=True)
        EXAMPLES = {
            "Python":[
                ("❌ NameError",     'def greet():\n    msg = "Hi " + nme\n    print(msg)\ngreet()'),
                ("❌ IndentError",   'for i in range(5):\nprint(i)'),
                ("❌ TypeError",     'age = "20"\nif age > 18:\n    print("Adult")'),
                ("❌ Logic Bug",     'def is_even(n):\n    return n % 2 == 1'),
            ],
            "Java":[
                ("❌ No semicolon",  'public class Hi{\n  public static void main(String[]a){\n    System.out.println("Hi")\n  }\n}'),
                ("❌ Wrong type",    'int x = "hello";\nSystem.out.println(x);'),
                ("❌ Missing return",'public static int add(int a,int b){\n  int c=a+b;\n}'),
            ],
            "C":[
                ("❌ No return",     '#include<stdio.h>\nint add(int a,int b){int s=a+b;}\nint main(){printf("%d",add(3,4));}'),
                ("❌ Undeclared",    '#include<stdio.h>\nint main(){printf("%d",num);return 0;}'),
            ],
            "C++":[
                ("❌ No include",    'int main(){cout<<"Hello";return 0;}'),
                ("❌ No namespace",  '#include<iostream>\nint main(){cout<<"Hi";return 0;}'),
            ],
            "JavaScript":[
                ("❌ Undefined var", 'function greet(){\n  console.log("Hi " + nme);\n}\ngreet();'),
                ("❌ == vs ===",     'if("5" == 5){\n  console.log("equal");\n}'),
            ],
        }
        for lbl_ex, code_ex in EXAMPLES.get(language, EXAMPLES["Python"]):
            with st.expander(lbl_ex):
                st.code(code_ex, language=language.lower())
                if st.button("Use This Example", key=f"ex_{lbl_ex}"):
                    st.session_state.uploaded_code = code_ex
                    st.rerun()
        st.markdown("""
        <div class="card" style="margin-top:10px">
          <div style="font-size:.82rem;font-weight:700;color:var(--cyan);margin-bottom:8px">🎯 Full Analysis gives you:</div>
          <div style="font-size:.83rem;color:var(--txt2);line-height:2.1">
            ✅ Plain-English error explanation<br>
            ✅ Auto-corrected working code<br>
            ✅ Line-by-line diff (what changed & why)<br>
            ✅ Code complexity metrics + charts<br>
            ✅ Personal tips + what you did well<br>
            ✅ Next concept to learn with a challenge
          </div>
        </div>""", unsafe_allow_html=True)

    # ── EXECUTE ──
    if run1:
        if need_key(): pass
        elif not code1.strip():
            st.warning("📋 Paste some code above!")
        else:
            with st.spinner("🤖 AI is carefully reading your code…"):
                try:
                    res = run(P_FULL, lang=language, code=code1, level=level)
                    ec  = error_count(res)
                    st.session_state.last_result    = {"r":res,"code":code1,"lang":language,"mode":"Full Analysis"}
                    st.session_state.analysis_count += 1
                    st.session_state.streak         += 1
                    st.session_state.total_errors   += ec
                    st.session_state.score          += 10
                    track_error_types(res)
                    save_history(language, "Full Analysis", code1)
                    st.success(f"✅ Done! Found {ec} issue(s) · +10 pts ⭐")
                except Exception as ex:
                    st.error(f"❌ {ex}")

    # ── RESULTS ──
    lr = st.session_state.last_result
    if lr and lr.get("mode") == "Full Analysis":
        txt = lr["r"]
        st.markdown("---")
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;flex-wrap:wrap">
          <span style="font-size:1.2rem;font-weight:800">📋 Analysis Results</span>
          <span style="background:rgba(59,130,246,.15);border:1px solid rgba(59,130,246,.3);
                       border-radius:20px;padding:3px 12px;font-size:.73rem;font-weight:700;color:#60a5fa">{lr["lang"]}</span>
        </div>""", unsafe_allow_html=True)

        # ── Quick visual snapshot: metrics bar + error-type pie ──
        ec_here    = error_count(txt)
        metrics    = parse_metrics(txt)
        types_here = re.findall(r'TYPE:\s*([A-Za-z/ ]+)', txt)
        vc1, vc2 = st.columns(2, gap="large")
        with vc1:
            vals = dict(metrics)
            vals["Errors Found"] = ec_here
            fig_m = px.bar(x=list(vals.keys()), y=list(vals.values()),
                           color=list(vals.keys()), color_discrete_sequence=PLOTLY_COLORS,
                           title="📊 Code Metrics at a Glance")
            fig_m.update_layout(showlegend=False, xaxis_title="", yaxis_title="")
            st.plotly_chart(style_fig(fig_m, height=260), use_container_width=True)
        with vc2:
            if types_here:
                cnt = Counter(t.strip().title() for t in types_here)
                fig_p = px.pie(names=list(cnt.keys()), values=list(cnt.values()), hole=.5,
                               color_discrete_sequence=PLOTLY_COLORS, title="🐛 Error Types in This Run")
                st.plotly_chart(style_fig(fig_p, height=260), use_container_width=True)
            else:
                st.markdown("""
                <div class="card" style="display:flex;align-items:center;justify-content:center;height:260px;text-align:center">
                  <div>
                    <div style="font-size:2rem">✅</div>
                    <div style="color:var(--txt2);font-size:.85rem;margin-top:6px">No errors detected — clean run!</div>
                  </div>
                </div>""", unsafe_allow_html=True)

        rc1, rc2 = st.columns([3,2], gap="large")
        with rc1:
            st.markdown('<div class="lbl">🤖 AI Explanation</div>', unsafe_allow_html=True)
            render_sections(txt)

        with rc2:
            st.markdown('<div class="lbl">💻 Code</div>', unsafe_allow_html=True)
            with st.expander("📄 Your Original Code", expanded=False):
                st.code(lr["code"], language=lr["lang"].lower())
            blocks = extract_code_blocks(txt)
            if blocks:
                st.markdown("**✅ Corrected Code:**")
                for b in blocks:
                    st.code(b.strip(), language=lr["lang"].lower())
            # Diff
            diffs = re.findall(r'OLD:\s*(.+?)\nNEW:\s*(.+?)\nWHY:\s*(.+?)(?:\n|$)', txt, re.DOTALL)
            if diffs:
                st.markdown('<div class="lbl" style="margin-top:14px">🔀 Diff View</div>', unsafe_allow_html=True)
                for old, new, why in diffs:
                    st.markdown(f"""
                    <div style="background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:12px;margin-bottom:8px;">
                      <span class="diff-del">− {old.strip()}</span>
                      <span class="diff-add">+ {new.strip()}</span>
                      <div style="font-size:.78rem;color:var(--txt3);margin-top:6px">💬 {why.strip()}</div>
                    </div>""", unsafe_allow_html=True)
            st.markdown("""
            <div class="card" style="margin-top:10px">
              <div style="font-weight:700;font-size:.85rem;margin-bottom:8px">📋 Next Steps</div>
              <ol style="color:var(--txt2);font-size:.85rem;padding-left:16px;line-height:2.2;margin:0">
                <li>Copy the corrected code</li><li>Run it in your IDE</li>
                <li>Read each changed line</li><li>Go to Quiz Me tab to test yourself!</li>
              </ol>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 2 ── QUICK FIX
# ════════════════════════════════════════════════════════════════════
with T[1]:
    st.markdown('<div class="lbl">⚡ Paste Code + Error Message → Get Instant Fix</div>', unsafe_allow_html=True)
    q1, q2 = st.columns([3,2], gap="large")
    with q1:
        code2  = st.text_area("Your Code", height=220, placeholder=f"Paste your {language} code…", label_visibility="visible")
        errmsg = st.text_area("Error Message", height=90,
                              placeholder="Paste the exact error message from your terminal / IDE…\ne.g.  NameError: name 'x' is not defined on line 5",
                              label_visibility="visible")
        run2 = st.button("⚡ Get Quick Fix", key="b2")
    with q2:
        st.markdown("""
        <div class="card">
          <div style="font-weight:700;color:var(--orange);margin-bottom:10px">🔴 Common Error Types</div>
          <div style="font-size:.85rem;color:var(--txt2);line-height:2.3">
            🔴 <b>SyntaxError</b> — typo, missing bracket/colon<br>
            🟠 <b>NameError</b> — variable not defined yet<br>
            🟡 <b>TypeError</b> — wrong data type<br>
            🔵 <b>IndentationError</b> — bad spaces/tabs<br>
            🟣 <b>IndexError</b> — list position out of range<br>
            🟢 <b>LogicError</b> — wrong output, no crash<br>
            ⚫ <b>RuntimeError</b> — crashes while running<br>
            🔴 <b>NullPointerException</b> — Java null object
          </div>
        </div>
        <div class="card">
          <div style="font-weight:700;color:var(--cyan);margin-bottom:8px">📌 Tips for Best Results</div>
          <ul style="font-size:.85rem;color:var(--txt2);padding-left:16px;line-height:2.2;margin:0">
            <li>Copy the <b>full</b> error message</li>
            <li>Include the line number if shown</li>
            <li>Paste the <b>complete</b> code, not just one line</li>
          </ul>
        </div>""", unsafe_allow_html=True)

    if run2:
        if need_key(): pass
        elif not code2.strip(): st.warning("Paste your code first!")
        else:
            with st.spinner("⚡ Diagnosing…"):
                try:
                    res2 = run(P_QUICKFIX, lang=language, code=code2,
                               err=errmsg or "No error message provided")
                    st.session_state.analysis_count += 1
                    st.session_state.total_errors   += 1
                    st.session_state.score          += 5
                    st.session_state.streak         += 1
                    etype = errmsg.split(":")[0].strip() if errmsg.strip() else "Unspecified"
                    log_error_type_manual(etype)
                    save_history(language, "Quick Fix", code2)
                    st.success("✅ Fix ready! +5 pts ⭐")
                    render_sections(res2)
                    blocks2 = extract_code_blocks(res2)
                    if blocks2:
                        st.markdown("**✅ Fixed Code:**")
                        for b in blocks2:
                            st.code(b.strip(), language=language.lower())
                except Exception as ex:
                    st.error(f"❌ {ex}")


# ════════════════════════════════════════════════════════════════════
# TAB 3 ── EXPLAIN CODE
# ════════════════════════════════════════════════════════════════════
with T[2]:
    st.markdown('<div class="lbl">📚 Understand Every Line</div>', unsafe_allow_html=True)
    e1, e2 = st.columns([3,2], gap="large")
    with e1:
        code3 = st.text_area("Code to Explain", height=280,
                             placeholder=f"Paste any {language} code — even if it's correct. I'll explain every single line!",
                             label_visibility="visible")
        run3  = st.button("📚 Explain Line By Line", key="b3")
    with e2:
        st.markdown("""
        <div class="card">
          <div style="font-weight:700;color:var(--purple);margin-bottom:10px">🎯 Great For:</div>
          <div style="font-size:.85rem;color:var(--txt2);line-height:2.3">
            🔹 Understanding lab code you copied<br>
            🔹 Studying before exams<br>
            🔹 Understanding teacher's solution<br>
            🔹 Reviewing someone else's code<br>
            🔹 Learning new concepts from examples<br>
            🔹 Checking if your logic is right
          </div>
        </div>""", unsafe_allow_html=True)

    if run3:
        if need_key(): pass
        elif not code3.strip(): st.warning("Paste code to explain!")
        else:
            with st.spinner("📚 Reading line by line…"):
                try:
                    res3 = run(P_EXPLAIN, lang=language, code=code3)
                    st.session_state.score  += 5
                    st.session_state.streak += 1
                    save_history(language, "Explain", code3)
                    st.success("✅ Explanation ready! +5 pts ⭐")
                    render_sections(res3)
                except Exception as ex:
                    st.error(f"❌ {ex}")


# ════════════════════════════════════════════════════════════════════
# TAB 4 ── QUIZ ME
# ════════════════════════════════════════════════════════════════════
with T[3]:
    st.markdown('<div class="lbl">🧠 Test Your Understanding</div>', unsafe_allow_html=True)
    qc1, qc2 = st.columns([2,1], gap="large")
    with qc1:
        code4 = st.text_area("Code for Quiz", height=200,
                             placeholder=f"Paste your {language} code → I'll generate 4 quiz questions!",
                             label_visibility="visible")
        run4  = st.button("🧠 Generate Quiz", key="b4")
    with qc2:
        st.markdown("""
        <div class="card">
          <div style="font-weight:700;color:var(--purple);margin-bottom:10px">🎯 Quiz Tests You On:</div>
          <div style="font-size:.85rem;color:var(--txt2);line-height:2.2">
            🔹 What the code outputs<br>🔹 Errors in the code<br>
            🔹 Variable values<br>🔹 Logic understanding<br>
            🔹 Bug identification
          </div>
        </div>
        <div class="card">
          <div style="font-weight:700;color:var(--orange);margin-bottom:6px">🏆 Points</div>
          <div style="font-size:.85rem;color:var(--txt2);line-height:2.2">
            4/4 → +20 ⭐ &nbsp; 3/4 → +12 ⭐<br>
            2/4 → +6 ⭐ &nbsp;&nbsp; 1/4 → +2 ⭐
          </div>
        </div>""", unsafe_allow_html=True)

    if run4:
        if need_key(): pass
        elif not code4.strip(): st.warning("Paste code first!")
        else:
            with st.spinner("🧠 Generating quiz…"):
                try:
                    raw4 = run(P_QUIZ, lang=language, code=code4)
                    clean = re.sub(r'^```(?:json)?\s*', '', raw4.strip())
                    clean = re.sub(r'\s*```$', '', clean).strip()
                    st.session_state.quiz_data      = json.loads(clean)
                    st.session_state.quiz_answers   = {}
                    st.session_state.quiz_submitted = False
                    st.success("✅ Quiz ready!")
                except Exception as ex:
                    st.error(f"❌ Quiz generation failed: {ex}")

    qd = st.session_state.quiz_data
    if qd:
        st.markdown("---")
        st.markdown("### 📝 Answer All 4 Questions:")
        for i, q in enumerate(qd):
            st.markdown(f"""
            <div class="qbox">
              <div class="qnum">Question {i+1} of {len(qd)}</div>
              <div class="qtxt">{q['q']}</div>
            </div>""", unsafe_allow_html=True)
            sel = st.radio(f"q{i}", q["options"], index=None,
                           key=f"qr_{i}", label_visibility="collapsed")
            if sel is not None:
                st.session_state.quiz_answers[i] = q["options"].index(sel)

        if not st.session_state.quiz_submitted:
            if st.button("✅ Submit Answers", key="qsub"):
                correct = sum(1 for i,q in enumerate(qd)
                              if st.session_state.quiz_answers.get(i)==q["answer"])
                pts = [0,2,6,12,20][min(correct,4)]
                st.session_state.score          += pts
                st.session_state.quiz_submitted  = True
                st.session_state.streak         += 1
                st.balloons()
                st.success(f"🎉 {correct}/{len(qd)} correct! +{pts} pts ⭐")

        if st.session_state.quiz_submitted:
            st.markdown("### 📊 Your Results:")
            correct_total = 0
            for i, q in enumerate(qd):
                chosen = st.session_state.quiz_answers.get(i)
                ok     = chosen == q["answer"]
                if ok: correct_total += 1
                st.markdown(f"""
                <div class="rb {'g' if ok else 'e'}">
                  <h4><span class="dot"></span>{'✅' if ok else '❌'} Q{i+1}: {q['q']}</h4>
                  <div>
                    <b>Your answer:</b> {q['options'][chosen] if chosen is not None else '—'}<br>
                    <b>Correct answer:</b> {q['options'][q['answer']]}<br>
                    <b>Explanation:</b> {q['explanation']}
                  </div>
                </div>""", unsafe_allow_html=True)
            pct = int(correct_total/len(qd)*100)
            wrong_total = len(qd) - correct_total
            qcol1, qcol2 = st.columns([1,1])
            with qcol1:
                st.markdown(f"""
                <div class="pbwrap" style="height:10px;margin:16px 0 6px">
                  <div class="pbfill" style="width:{pct}%;background:linear-gradient(90deg,var(--green),var(--cyan))"></div>
                </div>
                <p style="text-align:center;color:var(--txt2);font-size:.85rem">{pct}% Score</p>""",
                unsafe_allow_html=True)
            with qcol2:
                fig_q = px.pie(names=["Correct","Incorrect"], values=[correct_total, wrong_total],
                               color_discrete_sequence=["#10b981","#ef4444"], hole=.55)
                fig_q.update_traces(textinfo="value")
                st.plotly_chart(style_fig(fig_q, height=180), use_container_width=True)
            if st.button("🔄 New Quiz", key="qretry"):
                st.session_state.quiz_data = None
                st.session_state.quiz_submitted = False
                st.rerun()


# ════════════════════════════════════════════════════════════════════
# TAB 5 ── CHAT TUTOR
# ════════════════════════════════════════════════════════════════════
with T[4]:
    st.markdown('<div class="lbl">💬 Ask Your AI Tutor Anything</div>', unsafe_allow_html=True)
    cc1, cc2 = st.columns([2,1], gap="large")
    with cc1:
        code5 = st.text_area("Code Context (optional)", height=140,
                             placeholder=f"Paste your {language} code here so the tutor has context — or leave blank for general questions",
                             label_visibility="visible")
        # Render chat history
        for msg in st.session_state.chat_history:
            cls  = "u" if msg["role"]=="user" else "a"
            who  = "YOU" if msg["role"]=="user" else "🤖 AI TUTOR"
            body = msg["content"].replace("<","&lt;").replace(">","&gt;").replace("\n","<br>")
            st.markdown(f"""
            <div class="cb {cls}">
              <div class="who">{who}</div>
              <div>{body}</div>
            </div>""", unsafe_allow_html=True)

        q5   = st.text_input("Your question", placeholder="Why does this error happen? What is a pointer? How do I fix line 3?",
                             label_visibility="collapsed")
        rb5  = st.button("💬 Ask Tutor", key="b5")
        if st.button("🗑️ Clear Chat", key="clrchat"):
            st.session_state.chat_history = []
            st.rerun()

    with cc2:
        st.markdown("""
        <div class="card">
          <div style="font-weight:700;color:var(--cyan);margin-bottom:10px">💡 Try Asking:</div>
          <div style="font-size:.84rem;color:var(--txt2);line-height:2.4">
            "Why did I get NameError?"<br>
            "What does line 3 do?"<br>
            "Explain pointers simply"<br>
            "Difference between = and =="<br>
            "What is recursion?"<br>
            "Why use ArrayList in Java?"<br>
            "How do I loop through a list?"<br>
            "What is a null pointer exception?"
          </div>
        </div>""", unsafe_allow_html=True)

    if rb5 and q5.strip():
        if need_key(): pass
        else:
            st.session_state.chat_history.append({"role":"user","content":q5})
            hist_str = "\n".join(f"{m['role'].upper()}: {m['content']}"
                                 for m in st.session_state.chat_history[-8:])
            with st.spinner("💬 Tutor is thinking…"):
                try:
                    ans = run(P_CHAT, lang=language, code=code5 or "(no code provided)",
                              history=hist_str, question=q5)
                    st.session_state.chat_history.append({"role":"ai","content":ans})
                    st.session_state.score += 2
                    st.rerun()
                except Exception as ex:
                    st.error(f"❌ {ex}")


# ════════════════════════════════════════════════════════════════════
# TAB 6 ── ROADMAP
# ════════════════════════════════════════════════════════════════════
with T[5]:
    st.markdown('<div class="lbl">🗺️ Your Personalized Learning Roadmap</div>', unsafe_allow_html=True)
    rm1, rm2 = st.columns([2,1], gap="large")
    with rm1:
        code6 = st.text_area("Paste code for roadmap", height=230,
                             placeholder=f"Paste your {language} code → I'll analyze your skills and build a 5-step personalized learning path",
                             label_visibility="visible")
        run6  = st.button("🗺️ Build My Roadmap", key="b6")
    with rm2:
        st.markdown("""
        <div class="card">
          <div style="font-weight:700;color:var(--green);margin-bottom:10px">🎯 Roadmap Includes:</div>
          <div style="font-size:.85rem;color:var(--txt2);line-height:2.3">
            📊 Your current skill level + score gauge<br>
            ✅ Concepts you already know<br>
            ⚠️ Knowledge gaps identified<br>
            🗺️ 5-step custom learning path<br>
            📅 This week's specific goal<br>
            ⏰ Daily 15-min practice idea<br>
            📚 3 recommended resources<br>
            💬 Personalized motivation message
          </div>
        </div>""", unsafe_allow_html=True)

    if run6:
        if need_key(): pass
        elif not code6.strip(): st.warning("Paste code first!")
        else:
            with st.spinner("🗺️ Analyzing your skills…"):
                try:
                    raw6  = run(P_ROADMAP, lang=language, code=code6, level=level)
                    clean6 = re.sub(r'^```(?:json)?\s*','',raw6.strip())
                    clean6 = re.sub(r'\s*```$','',clean6).strip()
                    st.session_state.roadmap_data = json.loads(clean6)
                    st.session_state.score += 8
                    st.session_state.streak += 1
                    save_history(language, "Roadmap", code6)
                    st.success("✅ Roadmap built! +8 pts ⭐")
                except Exception as ex:
                    st.error(f"❌ {ex}")

    rd = st.session_state.roadmap_data
    if rd:
        lvl_str = rd.get("level","Beginner")
        sc_str  = rd.get("score",5)
        lc  = "lvl-b" if "Begin" in lvl_str else "lvl-i" if "Inter" in lvl_str else "lvl-a"

        hr1, hr2 = st.columns([2,1], gap="large")
        with hr1:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;flex-wrap:wrap">
              <span class="lvl {lc}">📊 {lvl_str}</span>
              <span style="color:var(--txt2);font-size:.9rem">Code Quality Score:</span>
              <span style="font-size:1.3rem;font-weight:900;color:var(--orange)">{sc_str}/10</span>
            </div>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="pbwrap" style="height:8px;margin-bottom:8px">
              <div class="pbfill" style="width:{sc_str*10}%;background:linear-gradient(90deg,var(--orange),var(--green))"></div>
            </div>""", unsafe_allow_html=True)
            # Known vs Gaps bar
            fig_kg = px.bar(x=["Known Concepts","Knowledge Gaps"],
                             y=[len(rd.get("known",[])), len(rd.get("gaps",[]))],
                             color=["Known Concepts","Knowledge Gaps"],
                             color_discrete_map={"Known Concepts":"#10b981","Knowledge Gaps":"#f59e0b"})
            fig_kg.update_layout(showlegend=False, xaxis_title="", yaxis_title="Count")
            st.plotly_chart(style_fig(fig_kg, height=220), use_container_width=True)
        with hr2:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=sc_str,
                title={"text":"Quality Gauge","font":{"size":13}},
                gauge={
                    "axis":{"range":[0,10]}, "bar":{"color":"#3b82f6"},
                    "bgcolor":"rgba(0,0,0,0)",
                    "steps":[
                        {"range":[0,4],"color":"rgba(239,68,68,.25)"},
                        {"range":[4,7],"color":"rgba(245,158,11,.25)"},
                        {"range":[7,10],"color":"rgba(16,185,129,.25)"},
                    ],
                }))
            st.plotly_chart(style_fig(fig_gauge, height=240), use_container_width=True)

        rd1, rd2 = st.columns([1,1], gap="large")
        with rd1:
            st.markdown('<div class="lbl">📍 Your 5-Step Path</div>', unsafe_allow_html=True)
            for step in rd.get("roadmap",[]):
                s  = step.get("status","next")
                nc = "rdone" if s=="done" else "rcurr" if s=="current" else "rnext"
                st.markdown(f"""
                <div class="rstep">
                  <div class="rnum {nc}">{step['step']}</div>
                  <div>
                    <div style="font-weight:700;font-size:.92rem">{step['topic']}</div>
                    <div style="font-size:.83rem;color:var(--txt2);margin-top:2px">{step['desc']}</div>
                    <div style="font-size:.68rem;color:var(--txt3);margin-top:3px;text-transform:uppercase;letter-spacing:1px">{s}</div>
                  </div>
                </div>""", unsafe_allow_html=True)

            mot = rd.get("motivational_message","")
            if mot:
                st.markdown(f"""
                <div class="rb p" style="margin-top:16px">
                  <h4><span class="dot"></span>💬 Message For You</h4>
                  <div>{mot}</div>
                </div>""", unsafe_allow_html=True)

        with rd2:
            st.markdown('<div class="lbl">✅ What You Know</div>', unsafe_allow_html=True)
            for c in rd.get("known",[]):
                st.markdown(f'<div style="background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);border-radius:8px;padding:7px 12px;margin-bottom:6px;font-size:.84rem;color:#34d399">✓ {c}</div>', unsafe_allow_html=True)

            st.markdown('<div class="lbl" style="margin-top:14px">⚠️ Knowledge Gaps</div>', unsafe_allow_html=True)
            for g in rd.get("gaps",[]):
                st.markdown(f'<div style="background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:8px;padding:7px 12px;margin-bottom:6px;font-size:.84rem;color:#fbbf24">○ {g}</div>', unsafe_allow_html=True)

            st.markdown('<div class="lbl" style="margin-top:14px">📅 Goals & Resources</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="rb g">
              <h4><span class="dot"></span>🎯 This Week</h4>
              <div>{rd.get('weekly_goal','Keep practicing!')}</div>
            </div>
            <div class="rb o">
              <h4><span class="dot"></span>⏰ Daily 15 Min</h4>
              <div>{rd.get('daily_practice','Write one small program every day.')}</div>
            </div>""", unsafe_allow_html=True)
            for r2 in rd.get("resources",[]):
                st.markdown(f'<div style="background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:8px 12px;margin-bottom:6px;font-size:.84rem;color:var(--txt2)">📖 {r2}</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 7 ── COMPARE
# ════════════════════════════════════════════════════════════════════
with T[6]:
    st.markdown('<div class="lbl">🔀 Compare Two Code Versions</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:var(--txt2);font-size:.88rem;margin-bottom:16px">Paste your original broken code AND the fixed version — AI explains every difference and what you learned.</p>', unsafe_allow_html=True)
    v1c, v2c = st.columns(2, gap="large")
    with v1c:
        st.markdown('<div class="lbl">📄 Version A (Original/Buggy)</div>', unsafe_allow_html=True)
        orig = st.text_area("v1", height=260, placeholder="Paste your original/broken code…", label_visibility="collapsed")
    with v2c:
        st.markdown('<div class="lbl">✅ Version B (Fixed/Improved)</div>', unsafe_allow_html=True)
        impr = st.text_area("v2", height=260, placeholder="Paste the corrected/improved code…", label_visibility="collapsed")
    run7 = st.button("🔀 Compare Versions", key="b7")

    if run7:
        if need_key(): pass
        elif not orig.strip() or not impr.strip(): st.warning("Paste both versions!")
        else:
            with st.spinner("🔀 Comparing…"):
                try:
                    res7 = run(P_COMPARE, lang=language, v1=orig, v2=impr)
                    st.session_state.score += 5
                    st.session_state.streak += 1
                    save_history(language, "Compare", orig)
                    st.success("✅ Comparison done! +5 pts ⭐")
                    # Quick visual: line-count comparison
                    fig_cmp = px.bar(x=["Original","Improved"],
                                      y=[len(orig.strip().splitlines()), len(impr.strip().splitlines())],
                                      color=["Original","Improved"],
                                      color_discrete_map={"Original":"#ef4444","Improved":"#10b981"})
                    fig_cmp.update_layout(showlegend=False, xaxis_title="", yaxis_title="Lines of Code")
                    st.plotly_chart(style_fig(fig_cmp, height=220), use_container_width=True)
                    sc1, sc2 = st.columns(2, gap="medium")
                    with sc1:
                        st.markdown("**📄 Original:**")
                        st.code(orig, language=language.lower())
                    with sc2:
                        st.markdown("**✅ Improved:**")
                        st.code(impr, language=language.lower())
                    render_sections(res7)
                except Exception as ex:
                    st.error(f"❌ {ex}")


# ════════════════════════════════════════════════════════════════════
# TAB 8 ── GENERATE CODE
# ════════════════════════════════════════════════════════════════════
with T[7]:
    st.markdown('<div class="lbl">✍️ Generate Practice Code</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:var(--txt2);font-size:.88rem;margin-bottom:16px">Describe what you want to build → get complete, well-commented code with explanations. Perfect for learning by example!</p>', unsafe_allow_html=True)

    g1, g2 = st.columns([2,1], gap="large")
    with g1:
        task = st.text_area("Describe what to build", height=120,
                            placeholder="Examples:\n• A program that finds the largest number in a list\n• Fibonacci series using recursion\n• Simple calculator with +, -, *, /\n• Check if a number is prime\n• Reverse a string without built-in functions",
                            label_visibility="visible")
        run8 = st.button("✍️ Generate Code", key="b8")
    with g2:
        st.markdown("""
        <div class="card">
          <div style="font-weight:700;color:var(--pink);margin-bottom:10px">💡 Great Ideas to Try:</div>
          <div style="font-size:.84rem;color:var(--txt2);line-height:2.3">
            📌 Factorial using recursion<br>
            📌 Bubble sort implementation<br>
            📌 Stack using array<br>
            📌 Palindrome checker<br>
            📌 Simple linked list<br>
            📌 Binary search<br>
            📌 Matrix multiplication
          </div>
        </div>""", unsafe_allow_html=True)

    if run8:
        if need_key(): pass
        elif not task.strip(): st.warning("Describe what to build!")
        else:
            with st.spinner("✍️ Writing code for you…"):
                try:
                    res8 = run(P_GENERATE, lang=language, task=task, level=level)
                    st.session_state.score += 8
                    st.session_state.streak += 1
                    save_history(language, "Generate", task)
                    st.success("✅ Code generated! +8 pts ⭐")
                    g_blocks = extract_code_blocks(res8)
                    if g_blocks:
                        st.markdown("**✅ Generated Code:**")
                        for b in g_blocks:
                            st.code(b.strip(), language=language.lower())
                    render_sections(res8)
                except Exception as ex:
                    st.error(f"❌ {ex}")


# ════════════════════════════════════════════════════════════════════
# TAB 9 ── ANALYTICS DASHBOARD  (NEW)
# ════════════════════════════════════════════════════════════════════
with T[8]:
    st.markdown('<div class="lbl">📊 Your Learning Analytics</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.info("🚀 Run a few analyses, fixes, or roadmaps first — your charts will appear here once you have data!")
    else:
        ns  = [h["n"] for h in st.session_state.score_log] or [0]
        scs = [h["score"] for h in st.session_state.score_log] or [0]

        a1, a2 = st.columns(2, gap="large")
        with a1:
            st.markdown("**📈 Score Progress**")
            fig_line = px.line(x=ns, y=scs, markers=True, color_discrete_sequence=["#3b82f6"])
            fig_line.update_traces(line=dict(width=3), marker=dict(size=8, color="#06b6d4"))
            fig_line.update_layout(xaxis_title="Analysis #", yaxis_title="Score")
            st.plotly_chart(style_fig(fig_line), use_container_width=True)

            st.markdown("**🌐 Language Usage**")
            lu = st.session_state.lang_usage
            if lu:
                fig_pie = px.pie(names=list(lu.keys()), values=list(lu.values()), hole=.5,
                                  color_discrete_sequence=PLOTLY_COLORS)
                st.plotly_chart(style_fig(fig_pie), use_container_width=True)
            else:
                st.caption("No language data yet.")

        with a2:
            st.markdown("**🛠️ Feature Usage**")
            mu = st.session_state.mode_usage
            if mu:
                fig_bar = px.bar(x=list(mu.values()), y=list(mu.keys()), orientation="h",
                                  color=list(mu.keys()), color_discrete_sequence=PLOTLY_COLORS)
                fig_bar.update_layout(showlegend=False, xaxis_title="Times Used", yaxis_title="")
                st.plotly_chart(style_fig(fig_bar), use_container_width=True)
            else:
                st.caption("No feature-usage data yet.")

            st.markdown("**🐛 Error Types Encountered**")
            et = st.session_state.error_types
            if et:
                fig_err = px.bar(x=list(et.keys()), y=list(et.values()),
                                  color=list(et.keys()), color_discrete_sequence=PLOTLY_COLORS)
                fig_err.update_layout(showlegend=False, xaxis_title="", yaxis_title="Count")
                st.plotly_chart(style_fig(fig_err), use_container_width=True)
            else:
                st.caption("No error data yet — run Full Analysis or Quick Fix on buggy code!")

        st.markdown("---")
        st.markdown(f"""
        <div class="stats-strip">
          <div class="stat-box"><div class="sv">{len(st.session_state.lang_usage)}</div><div class="sl">Languages Tried</div></div>
          <div class="stat-box"><div class="sv">{len(st.session_state.mode_usage)}</div><div class="sl">Features Used</div></div>
          <div class="stat-box"><div class="sv">{max(scs) if scs else 0}</div><div class="sl">Peak Score</div></div>
          <div class="stat-box"><div class="sv">{sum(st.session_state.error_types.values()) if st.session_state.error_types else 0}</div><div class="sl">Bugs Logged</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="lbl">🕒 Full Session Log</div>', unsafe_allow_html=True)
        for item in reversed(st.session_state.history):
            st.markdown(f"""
            <div class="card" style="padding:12px 16px;display:flex;justify-content:space-between;align-items:center">
              <div>
                <span style="font-weight:700;color:var(--blue)">#{item['n']}</span>
                &nbsp;·&nbsp; {item['lang']} &nbsp;·&nbsp; <span style="color:var(--cyan)">{item['mode']}</span>
              </div>
              <div style="color:var(--txt3);font-size:.78rem">{item.get('time','')}</div>
            </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 10 ── CONVERT LANGUAGE  (NEW)
# ════════════════════════════════════════════════════════════════════
with T[9]:
    st.markdown('<div class="lbl">🔄 Translate Your Code Between Languages</div>', unsafe_allow_html=True)
    ALL_LANGS = ["Python","Java","C","C++","JavaScript"]
    cv1, cv2 = st.columns([3,2], gap="large")
    with cv1:
        colA, colB = st.columns(2)
        with colA:
            from_lang = st.selectbox("From", ALL_LANGS,
                                      index=ALL_LANGS.index(language) if language in ALL_LANGS else 0,
                                      key="cv_from")
        with colB:
            to_opts = [l for l in ALL_LANGS if l != from_lang]
            to_lang = st.selectbox("To", to_opts, key="cv_to")
        code9 = st.text_area("Code to convert", height=260,
                             placeholder=f"Paste your {from_lang} code here…", label_visibility="visible")
        run9 = st.button("🔄 Convert Code", key="b9")
    with cv2:
        st.markdown("""
        <div class="card">
          <div style="font-weight:700;color:var(--cyan);margin-bottom:10px">🎯 Why Convert?</div>
          <div style="font-size:.85rem;color:var(--txt2);line-height:2.3">
            🔹 See how the same logic looks in another language<br>
            🔹 Great for comparing syntax across courses<br>
            🔹 Learn a new language faster using code you already understand<br>
            🔹 Spot language-specific gotchas before they bite you
          </div>
        </div>""", unsafe_allow_html=True)

    if run9:
        if need_key(): pass
        elif not code9.strip(): st.warning("Paste some code to convert!")
        else:
            with st.spinner(f"🔄 Translating {from_lang} → {to_lang}…"):
                try:
                    res9 = run(P_CONVERT, from_lang=from_lang, to_lang=to_lang, code=code9)
                    st.session_state.score += 5
                    st.session_state.streak += 1
                    save_history(to_lang, "Convert", code9)
                    st.success(f"✅ Converted to {to_lang}! +5 pts ⭐")
                    cc_left, cc_right = st.columns(2, gap="medium")
                    with cc_left:
                        st.markdown(f"**📄 Original ({from_lang}):**")
                        st.code(code9, language=from_lang.lower())
                    with cc_right:
                        blocks9 = extract_code_blocks(res9)
                        st.markdown(f"**✅ Converted ({to_lang}):**")
                        if blocks9:
                            st.code(blocks9[0].strip(), language=to_lang.lower())
                    render_sections(res9)
                except Exception as ex:
                    st.error(f"❌ {ex}")


# ════════════════════════════════════════════════════════════════════
# TAB 11 ── DAILY CHALLENGE  (NEW)
# ════════════════════════════════════════════════════════════════════
with T[10]:
    st.markdown('<div class="lbl">🎯 Sharpen Your Skills</div>', unsafe_allow_html=True)
    dc1, dc2 = st.columns([1,1], gap="large")
    with dc1:
        topic = st.selectbox("Pick a topic", ["Surprise Me","Loops","Functions","Arrays/Lists","Strings","Recursion","Conditionals"])
        run10 = st.button("🎲 Get a Challenge", key="b10")
    with dc2:
        st.markdown("""
        <div class="card">
          <div style="font-weight:700;color:var(--green);margin-bottom:8px">💪 How It Works</div>
          <div style="font-size:.84rem;color:var(--txt2);line-height:2.2">
            1️⃣ Get a bite-sized problem in your language<br>
            2️⃣ Try it yourself first using the starter code<br>
            3️⃣ Stuck? Reveal a hint<br>
            4️⃣ Check your work against the solution
          </div>
        </div>""", unsafe_allow_html=True)

    if run10:
        if need_key(): pass
        else:
            with st.spinner("🎯 Cooking up a challenge…"):
                try:
                    raw10 = run(P_CHALLENGE, lang=language, level=level, topic=topic)
                    clean10 = re.sub(r'^```(?:json)?\s*','',raw10.strip())
                    clean10 = re.sub(r'\s*```$','',clean10).strip()
                    st.session_state.challenge_data = json.loads(clean10)
                    st.session_state.challenge_revealed = False
                    st.session_state.mode_usage["Challenge"] = st.session_state.mode_usage.get("Challenge", 0) + 1
                    st.success("✅ Challenge ready!")
                except Exception as ex:
                    st.error(f"❌ {ex}")

    cd = st.session_state.challenge_data
    if cd:
        st.markdown(f"""
        <div class="qbox">
          <div class="qnum">{cd.get('difficulty','Medium').upper()} · {language}</div>
          <div class="qtxt" style="font-size:1.1rem">{cd.get('title','Challenge')}</div>
          <div style="font-size:.88rem;color:var(--txt2);line-height:1.7">{cd.get('problem','')}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("**📝 Starter Code:**")
        st.code(cd.get("starter_code",""), language=language.lower())

        with st.expander("💡 Need a hint?"):
            for i, h in enumerate(cd.get("hints",[])):
                st.markdown(f"**Hint {i+1}:** {h}")

        if not st.session_state.challenge_revealed:
            if st.button("👀 Reveal Solution", key="reveal_sol"):
                st.session_state.challenge_revealed = True
                st.session_state.score += 3
                st.rerun()
        else:
            st.markdown("**✅ Solution:**")
            st.code(cd.get("solution",""), language=language.lower())
            st.markdown(f"""
            <div class="rb g"><h4><span class="dot"></span>🔍 Approach</h4><div>{cd.get('explanation','')}</div></div>
            """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TAB 12 ── ACHIEVEMENTS  (NEW)
# ════════════════════════════════════════════════════════════════════
with T[11]:
    st.markdown('<div class="lbl">🏆 Your Badges</div>', unsafe_allow_html=True)

    s = st.session_state
    unlocked_ids = {b["id"] for b in BADGES if b["cond"](s)}
    n_unlocked   = len(unlocked_ids)
    n_total      = len(BADGES)

    bcol1, bcol2 = st.columns([2,1], gap="large")
    with bcol1:
        st.markdown(f"""
        <div class="stats-strip">
          <div class="stat-box"><div class="sv">{n_unlocked}/{n_total}</div><div class="sl">Badges Earned</div></div>
          <div class="stat-box"><div class="sv">{int(n_unlocked/n_total*100)}%</div><div class="sl">Collection Complete</div></div>
        </div>""", unsafe_allow_html=True)
    with bcol2:
        fig_b = px.pie(names=["Unlocked","Locked"], values=[n_unlocked, n_total - n_unlocked],
                       color_discrete_sequence=["#10b981","#1a2840"], hole=.6)
        fig_b.update_traces(textinfo="none")
        fig_b.update_layout(showlegend=False)
        st.plotly_chart(style_fig(fig_b, height=160), use_container_width=True)

    st.markdown("---")
    cols_b = st.columns(3)
    for i, b in enumerate(BADGES):
        is_un = b["id"] in unlocked_ids
        with cols_b[i % 3]:
            st.markdown(f"""
            <div class="card badge-card" style="text-align:center;opacity:{1 if is_un else .45};
                        border-color:{'rgba(16,185,129,.4)' if is_un else 'var(--border)'}">
              <div style="font-size:2.2rem;margin-bottom:6px">{b['icon']}</div>
              <div style="font-weight:800;font-size:.88rem">{b['name']}</div>
              <div style="font-size:.76rem;color:var(--txt2);margin-top:4px">{b['desc']}</div>
              <div style="font-size:.68rem;margin-top:8px;font-weight:700;color:{'#34d399' if is_un else 'var(--txt3)'}">
                {'✅ UNLOCKED' if is_un else '🔒 LOCKED'}
              </div>
            </div>""", unsafe_allow_html=True)


# ── SESSION HISTORY (recent 5, shown on every tab view) ───────────
if st.session_state.history:
    st.markdown("---")
    st.markdown('<div class="lbl">🕒 Session History</div>', unsafe_allow_html=True)
    cols_h = st.columns(min(len(st.session_state.history), 5))
    for i, item in enumerate(reversed(st.session_state.history[-5:])):
        with cols_h[i]:
            st.markdown(f"""
            <div class="card" style="padding:13px">
              <div style="font-size:.67rem;color:var(--txt3)">#{item['n']} · {item.get('time','')}</div>
              <div style="font-size:.78rem;font-weight:700;color:var(--blue);margin:3px 0">{item['lang']} · {item['mode'][:14]}</div>
              <div style="font-size:.72rem;color:var(--txt3);font-family:var(--mono);
                          overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{item['snippet']}</div>
            </div>""", unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:48px 0 24px;color:var(--txt3);font-size:.78rem;
            border-top:1px solid var(--border);margin-top:40px">
  <div style="font-size:1.1rem;font-weight:900;margin-bottom:6px;
              background:linear-gradient(90deg,#60a5fa,#06b6d4,#a78bfa);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
    AI Coding Buddy Pro · v4.0 — Analytics Edition
  </div>
  Built with ❤️ using <b>Streamlit</b> · <b>LangChain Core</b> · <b>Mistral AI</b> · <b>Plotly</b><br>
  <span style="opacity:.5;margin-top:4px;display:block">
    Helping engineering students debug, learn, and level up — one error at a time.
  </span>
</div>""", unsafe_allow_html=True)

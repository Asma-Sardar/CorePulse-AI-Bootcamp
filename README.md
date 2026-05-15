# Pulsera 🌿
### AI-Powered Recovery Intelligence System

> *"Don't just train hard. Train smart. Know when to stop."*

Built at **Al Yamamah University, Khobar** · AI Bootcamp Hackathon 2026

---

## The Problem

Athletes overtrain. They push through fatigue, ignore warning signs, and only feel the damage after it's too late. Generic fitness apps tell you to "rest when tired." That's not good enough.

**Pulsera tells you exactly when, why, and what to do — before breakdown happens.**

---

## What Makes Pulsera Different

| Feature | What It Does |
|---|---|
| 🤖 **ML Readiness Score** | XGBoost model trained on 973 real athletes predicts your readiness (0–100) |
| 🧠 **RAG Knowledge Base** | 25 peer-reviewed sports science protocols retrieved and matched to your state |
| 💬 **LLM Coaching** | Personalized advice grounded in YOUR metrics — not generic ChatGPT |
| 📊 **Explainability** | See exactly what drove your score: sleep, HR, load, intensity |
| 🕐 **Multi-Horizon Memory** | 7-day, 30-day, and long-term baselines — compares you to *you* |
| 📈 **Trend Graphs** | Track your recovery trajectory over time |
| 💧 **Hydration Intelligence** | Custom water targets based on your weight, session, and intensity |
| ⚡ **Auto-Calculations** | Max BPM, body fat, HR reserve, VO₂ max — calculated live as you type |

---

## Three-Layer AI Architecture

```
User Metrics (daily log)
        ↓
[ Layer 1 ] ML Model (XGBoost + Random Forest)
        → Readiness Score (0–100) + Contributing Factors
        ↓
[ Layer 2 ] RAG Retrieval (TF-IDF Cosine Similarity)
        → 25 Evidence-Based Recovery Protocols matched to your state
        ↓
[ Layer 3 ] LLM Personalization (Groq · Gemini · OpenRouter)
        → Coaching advice grounded in your data + sports science
```

---

## How to Use

** Open directly (no installation):**
1. Download `pulsera_realcoach.html`
2. Open in any browser
3. That's it — fully self-contained

---

## First Time Setup

1. **Create your profile** — age, weight, height, experience level (once only)
2. **Log your workout daily** — duration, intensity, heart rate, sleep
3. **Get your Readiness Score** — with full explanation of contributing factors
4. **Read your coaching advice** — personalized, evidence-based, actionable
5. **Track your trend** — 7-day and 30-day recovery graphs

---

## Tech Stack

```
Frontend    HTML5 · JavaScript · TF-IDF RAG · SVG Charts · IndexedDB
ML Model    XGBoost · Random Forest · Optuna · scikit-learn (973 athletes)
RAG         ChromaDB · Sentence Transformers · 25 sports science protocols
LLM         Groq (LLaMA 3.3) · Google Gemini · OpenRouter (fallback chain)
Backend     Python · Streamlit · SQLite · Pandas · NumPy
```

---

## Project Structure

```
CorePulse-AI-Bootcamp/
├── pulsera_realcoach.html   ← Full frontend app (self-contained)
├── app.py                   ← Streamlit backend
├── llm_coach.py             ← LLM integration (Groq)
├── PULSERA.ipynb            ← ML model training notebook
├── data/
│   └── knowledge_base.json  ← 25 RAG protocols (sports science)
├── rag/
│   ├── build_vectorstore.py ← ChromaDB vector store builder
│   └── retriever.py         ← RAG retrieval + contributing factors
├── corepulse.db             ← SQLite user database
└── requirements.txt
└──.DS_Store
```

---

## The Science Behind It

Recovery protocols sourced from:
- NSCA Training Guidelines 2025
- ISSN Nutrient Timing Position Stand 2017
- Walsh et al., British Journal of Sports Medicine 2021
- Carrard et al., Sports Health 2022 — Overtraining Syndrome
- Hatia et al., Cureus 2024 — Sleep and Athletic Recovery
- IOC 2023 Consensus Statement on Athlete Nutrition
- Frontiers in Physiology 2025 — Sleep Deprivation and Performance

---

## Team

Built with 💚 by Team Pulsera · Al Yamamah University, Khobar · 2026

## Team Members: 

Asma Sardar
Ayah Alqassab
Leena Albakawi
Rana Alshehri
Hala Alfardan

---

*Pulsera is a prototype built for educational purposes. Always consult a medical professional for health decisions.*

# 🚂 IRCTC Conversational IVR — Milestone 3
### Web Simulator with Speech-to-Text · NLU · Text-to-Speech

---

## 🌐 Live Demo

👉 **https://railspeak.netlify.app**

> Open in **Chrome or Edge** → Allow microphone → Start talking!

---

## 🎯 What's New in Milestone 3

| Feature | M2 | M3 |
|---------|----|----|
| Input Method | DTMF buttons only | Voice + Text + DTMF |
| Speech-to-Text | ❌ | ✅ Web Speech API |
| Intent Detection | ❌ | ✅ Keyword + Regex NLU |
| Entity Extraction | ❌ | ✅ Stations, PNR, Date, Class |
| Text-to-Speech | ❌ | ✅ SpeechSynthesis API |
| Multi-turn Session | ❌ | ✅ State machine |
| Debug Panel | ❌ | ✅ Live intent + confidence |

---

## 🗣️ Supported Intents

| Intent | Example |
|--------|---------|
| Book Ticket | "I want to book a ticket from Delhi to Mumbai" |
| PNR Status | "Check PNR 1234567890" |
| Train Schedule | "Schedule of train 12951" |
| Cancel Ticket | "I want to cancel my ticket" |
| Fare Enquiry | "What is the fare from Delhi to Bangalore?" |
| Running Status | "Is my train running late?" |
| Complaint | "I have a complaint" |

---

## 🧪 Test It Out

**One-shot booking:**
```
Book ticket from Delhi to Mumbai on 15 April sleeper class
```

**Step-by-step:**
```
1. "Book a ticket"
2. "Delhi"
3. "Mumbai"
4. "15 April"
5. "Sleeper"
```

**PNR Check** — Sample PNRs to try:
- `1234567890` → CONFIRMED
- `9876543210` → RAC
- `5555555555` → Waitlist

---

## 🏗️ Architecture

```
Browser (Chrome/Edge)
│
├── 🎤 Web Speech API       → Voice input (STT)
├── 🧠 Intent Detection     → NLU in JavaScript (no API needed)
├── 🔍 Entity Extraction    → Stations, PNR, Date, Class
├── 💬 Dialogue Manager     → State machine, multi-turn context
└── 🔊 SpeechSynthesis      → Voice output (TTS)
```

**Zero backend. Zero API keys. Zero cost. Runs entirely in browser.**

---

## 📁 Project Structure

```
repo/
├── irctc_simulator_m3.html   ← Milestone 3 (this milestone)
├── irctc_ui.html             ← Milestone 2 DTMF simulator
├── irctc_backend.py          ← Optional FastAPI backend
└── README_M3.md              ← This file
```

---

## 🚀 Run Locally


```
Open: `http://localhost:5500/irctc_simulator_m3.html`


---

## 📞 Note on Real Phone IVR

This simulator demonstrates the complete conversational AI layer.
In production (Milestone 4), the same NLU and dialogue logic would be
triggered via an incoming call to a **Twilio / Azure ACS** phone number.
The intent detection and state machine remain identical — only STT/TTS
would shift to cloud services (Azure Speech).

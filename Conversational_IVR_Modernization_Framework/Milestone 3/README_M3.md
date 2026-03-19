# 🚂 IRCTC Conversational IVR — Milestone 3
### Web Simulator with Speech-to-Text · NLU · Text-to-Speech

> **Project:** Conversational IVR Modernization Framework
> **Author:** M. Ramya Srivalli | Infosys Intern | Batch 13, Group-2
> **Organization:** Infosys Internship Project

---

## 🌐 Live Demo

👉 **[https://ticket-assistant--24b01a4278.replit.app](https://ticket-assistant--24b01a4278.replit.app)**

> Open in **Chrome or Edge** → Allow microphone → Start talking!

---

## 🖥️ Run Locally

```
https://glorious-trout-5g9xwv77j5pgcpvjj-8000.app.github.dev/irctc_m3.html
```

Or with VS Code Live Server → right-click `irctc_m3.html` → Open with Live Server → `http://localhost:5500/irctc_m3.html`

> ⚠️ **Voice input (STT) requires Chrome or Edge** — Firefox does not support Web Speech API.

---

## 📌 What is Milestone 3?

Milestone 3 upgrades the DTMF-only simulator from Milestone 2 into a **fully conversational AI IVR**. Users can now speak naturally — or type — instead of pressing number buttons.

**Milestone 2 (DTMF Only):**
```
System: "Press 1 for PNR status, Press 2 for ticket booking..."
User:   *Clicks button "1"*
```

**Milestone 3 (Conversational AI):**
```
System: "Namaste! How can I assist you today?"
User:   "I want to check my PNR status for 1234567890"
System: "✅ CONFIRMED | Coach B4 | Berth 32 (Lower) | Platform 3"
```

---

## 🎯 What's New in Milestone 3

| Feature | M2 | M3 |
|---------|----|----|
| Input Method | DTMF buttons only | ✅ Voice + Text + DTMF |
| Speech-to-Text | ❌ | ✅ Web Speech API |
| Intent Detection | ❌ | ✅ Keyword + Regex NLU |
| Entity Extraction | ❌ | ✅ Stations, PNR, Date, Class |
| Text-to-Speech | ❌ | ✅ SpeechSynthesis API |
| Multi-turn Session | ❌ | ✅ State machine dialogue |
| Debug Panel | ❌ | ✅ Live intent + confidence |
| Session Stats | ❌ | ✅ Messages, intents, avg confidence |
| Result Cards | ❌ | ✅ PNR / Booking / Tracking cards |

---

## 🏗️ Architecture

Milestone 3 runs **entirely in the browser**. Zero backend. Zero API keys. Zero cost.

```
Browser (Chrome / Edge)
│
├── 🎤 Web Speech API     → Voice input (STT) via Google's built-in model
├── 🧠 Intent Detection   → Regex + keyword NLU in JavaScript
├── 🔍 Entity Extraction  → Stations, PNR, dates, travel class
├── 💬 Dialogue Manager   → State machine, multi-turn context
├── 🖥️  UI Renderer       → Chat bubbles, quick replies, result cards
└── 🔊 SpeechSynthesis   → Voice output (TTS), browser-native
```

---

## 🗣️ Supported Intents

| Intent | Example Utterance |
|--------|---------|
| 🎫 Book Ticket | "Book a ticket from Delhi to Mumbai on 15 April sleeper" |
| 📋 PNR Status | "Check PNR 1234567890" |
| 📍 Live Train Tracking | "Live status of train 12951" |
| 🕐 Train Schedule | "Schedule of train 12301" |
| ❌ Cancel Ticket | "I want to cancel my ticket PNR 9876543210" |
| 💰 Fare Enquiry | "What is the fare from Delhi to Bangalore 3AC?" |
| ⚡ Tatkal Booking | "Tatkal ticket from Bangalore to Chennai tomorrow" |
| 📢 Complaint | "I have a complaint about food quality" |

---

## 🧪 Test It Out

**One-shot booking:**
```
Book ticket from Delhi to Mumbai on 15 April sleeper class
```

**Step-by-step (multi-turn):**
```
"Book a ticket" → "Delhi" → "Mumbai" → "15 April" → "Sleeper"
```

**Sample PNRs to try:**

| PNR | Expected Result |
|-----|----------------|
| `1234567890` | ✅ CONFIRMED — Train 12951, Coach B4, Berth 32, Platform 3 |
| `9876543210` | 🟡 RAC 12 — Train 12630, Coach A2, Platform 1 |
| `5555555555` | ❌ WL 89 — Train 12483 |
| `4444444444` | ✅ CONFIRMED — Train 22119, Coach H1, Berth 05, Platform 5 |

**Sample train numbers to track:** `12951`, `12301`, `12630`, `22119`, `12002`

---

## ⚙️ Three Input Modes

| Mode | How to Use |
|------|-----------|
| **Text Chat** | Type query and press Enter or ➤ |
| **Voice (STT)** | Click 🎤 → speak → auto-sends when done |
| **DTMF Keypad** | 1=PNR · 2=Book · 3=Track · 4=Schedule · 5=Fare · 6=Cancel · 9=Complaint · 0=Exit |

---

## 📁 Project Structure

```
Conversational_IVR_Modernization_Framework/
├── Milestone 2/
│   ├── README_M2.md
│   ├── irctc_backend.py       ← FastAPI integration layer
│   └── irctc_ui.html          ← M2 DTMF simulator
├── Milestone 3/
│   ├── README_M3.md           ← This file
│   └── irctc_m3.html          ← M3 Conversational simulator
├── LICENSE
├── README.md
├── milestone1.pdf
└── ramya_agile.xls
```

---

## 🛣️ Milestone Roadmap

| Milestone | Status | Description |
|-----------|--------|-------------|
| M1 | ✅ Complete | Legacy system analysis & requirements |
| M2 | ✅ Complete | FastAPI integration layer + DTMF simulator |
| M3 | ✅ Complete | Conversational AI — Voice + NLU + TTS |
| M4 | 🔄 Upcoming | Real phone IVR via Twilio / Azure ACS |

---

## 🧰 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Vanilla JavaScript (ES6+) |
| Speech-to-Text | Web Speech API (browser-native) |
| Text-to-Speech | SpeechSynthesis API (browser-native) |
| NLU Engine | Custom Regex + Keyword matching |
| Dialogue Manager | JavaScript state machine |
| Live Demo | Replit |
| Local Dev | GitHub Codespaces |
| Target Cloud (M4) | Azure Communication Services + BAP / Twilio |

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| Voice button does nothing | Use Chrome or Edge — Firefox not supported |
| Mic not working | Allow microphone access in browser settings |
| Voice recognised incorrectly | Speak clearly; try typing the same query to test |
| Bot says "I didn't understand" | Use keywords: "book", "PNR", "track", "fare", "cancel" — check NLU Debug panel |

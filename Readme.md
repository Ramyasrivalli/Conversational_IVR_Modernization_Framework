# 🚂 Conversational IVR Modernization Framework

> **AI-Enabled IRCTC IVR Modernization using Azure ACS · Twilio · Web Simulator**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal.svg)](https://fastapi.tiangolo.com)
[![M3 Live Demo](https://img.shields.io/badge/M3%20Demo-Replit-orange.svg)](https://ticket-assistant--24b01a4278.replit.app)
[![M2 Live Demo](https://img.shields.io/badge/M2%20Demo-Claude-blueviolet.svg)](https://claude.ai/public/artifacts/6f11325f-8531-487e-a886-fdbf6ae76559)

---

## 👤 Author

| Field | Details |
|-------|---------|
| **Name** | M. Ramya Srivalli |
| **Organization** | Infosys Internship |
| **Batch** | Batch 13, Group-2 |
| **Project** | AI-Enabled Conversational IVR Modernization Framework |
| **Year** | 2026 |

---

## 🌐 Live Demo & Links

| Resource | Link | Description |
|----------|------|-------------|
| 🚀 **M3 Live Demo** | [ticket-assistant--24b01a4278.replit.app](https://ticket-assistant--24b01a4278.replit.app) | Conversational IVR — voice + text + DTMF |
| 🖥️ **M2 Live Demo** | [DTMF IVR Simulator](https://claude.ai/public/artifacts/6f11325f-8531-487e-a886-fdbf6ae76559) | DTMF web simulator — keypad + JSON viewer |
| 📖 **M2 API Docs** | `http://localhost:8000/docs` | Swagger UI — run `python irctc_backend.py` first |
| 📁 **Repository** | [github.com/Ramyasrivalli/Conversational_IVR_Modernization_Framework](https://github.com/Ramyasrivalli/Conversational_IVR_Modernization_Framework) | Full source code |

> ⚠️ Open M3 demo in **Chrome or Edge** — Firefox does not support the Web Speech API (voice input).

---

## 📌 Project Overview

This project modernizes the traditional **IRCTC IVR (Interactive Voice Response)** system — the automated telephone service Indian railway passengers call to check PNR status, book tickets, track trains, and get travel information.

### Background

IRCTC (Indian Railway Catering and Tourism Corporation) operates one of the world's largest IVR systems, serving millions of passengers daily through the railway helpline **139**. Passengers across India — including those without smartphones or internet access — depend on this system for critical travel information.

### The Problem

The existing IRCTC IVR is built on **VoiceXML (VXML)** — a legacy technology from the early 2000s. It forces passengers to:

- Navigate through **deep numbered menus** — "Press 1 for PNR, Press 2 for booking, Press 3 for..."
- Press **multiple DTMF keys** on their phone keypad just to answer a simple question
- **Repeat their details** every call — the system has no memory of previous interactions
- Suffer through **long call durations** and high drop-off rates during peak hours
- Struggle with **poor peak-hour performance** — the Tatkal booking window (10 AM daily) generates massive call spikes that degrade the system
- Navigate in only **two languages** (Hindi and English) — adding a new language requires re-recording every prompt

### The Solution

A **hybrid modernization approach** — a conversational AI layer added on top of the existing legacy system without replacing or disrupting it.

```
User speaks naturally:   "Mujhe PNR 1234567890 ka status batao"
System understands:       Intent: pnr_status | Entity: PNR = 1234567890
System responds:          "PNR 1234567890 is CONFIRMED on train 12951, Coach B4, Berth 32 (Lower), Platform 3"
```

**Key benefits:**
- Passengers speak naturally — no menu navigation needed
- System remembers context across the entire call
- Cloud-native auto-scaling for Tatkal rush hours
- Legacy DTMF menus continue working as a fallback
- Zero disruption — the existing system stays live

---

## 🏗️ System Architecture

### High-Level Flow

```
📞 Passenger Calls IRCTC 139
              │
              ▼
┌─────────────────────────────────────┐
│     Cloud Telephony Layer           │
│     Azure ACS / Twilio /            │
│     Web Simulator (Browser)         │
│     ─ Receives PSTN/VoIP call       │
│     ─ Streams audio to STT          │
│     ─ Plays TTS response back       │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│     FastAPI Integration Layer       │  ← Milestone 2
│     irctc_backend.py                │
│     ─ Session management            │
│     ─ Menu routing                  │
│     ─ DTMF handling                 │
│     ─ ACS/BAP bridge stub           │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│     Conversational AI Layer         │  ← Milestone 3
│     irctc_m3.html                   │
│     ─ Speech-to-Text (STT)          │
│     ─ Intent Detection (NLU)        │
│     ─ Entity Extraction             │
│     ─ Dialogue State Machine        │
│     ─ Text-to-Speech (TTS)          │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│     IRCTC Backend Services          │
│     ─ PNR Database                  │
│     ─ Reservation System (PRS)      │
│     ─ Train Enquiry System (NTES)   │
│     ─ Payment Gateway               │
└─────────────────────────────────────┘
```

### Three Platform Tracks

The project is designed to work across three different telephony platforms:

| Track | Platform | How It Works |
|-------|----------|-------------|
| **A** | Azure Communication Services (ACS) | Cloud-native Microsoft telephony; SDK-based call control; Azure Neural TTS (`en-IN-NeerjaNeural`) |
| **B** | Twilio | XML-based TwiML instructions; `<Gather input="speech">` for voice input; webhook-driven architecture |
| **C** | Web Simulator | Browser-native; Web Speech API for STT; SpeechSynthesis API for TTS; zero cost, zero setup |

---

## 📂 Complete Repository Structure

```
Conversational_IVR_Modernization_Framework/
│
├── 📄 README.md                     ← This file — complete project documentation
├── 📄 LICENSE                       ← MIT License (Copyright 2026 M. Ramya Srivalli)
├── 📄 CONTRIBUTING.md               ← How to report issues and contribute
├── 📄 requirements.txt              ← All Python dependencies (FastAPI, uvicorn, pytest, etc.)
├── 📄 .gitignore                    ← Excludes secrets, __pycache__, .env files
├── 📊 ramya_agile.xls               ← Agile sprint tracker for the project
│
├── 📁 Milestone_1/
│   ├── 📄 README_M1.md              ← Full M1 documentation
│   │                                   (legacy architecture, limitations, ACS/BAP needs,
│   │                                    6-phase roadmap, compatibility gap analysis)
│   └── 📄 milestone1.pdf            ← Submitted legacy system analysis report
│
├── 📁 Milestone_2/
│   ├── 📄 README_M2.md              ← Full M2 documentation
│   │                                   (how to run, simulator walkthrough,
│   │                                    all 9 API endpoints with JSON examples,
│   │                                    ACS bridge explanation, debugging guide)
│   ├── 🐍 irctc_backend.py          ← FastAPI integration layer
│   │                                   • POST /ivr/start    — session + welcome prompt
│   │                                   • POST /ivr/input    — DTMF routing
│   │                                   • POST /ivr/pnr      — PNR status lookup
│   │                                   • POST /ivr/booking  — ticket booking
│   │                                   • POST /ivr/tatkal   — Tatkal emergency booking
│   │                                   • POST /ivr/tracking — live train tracking
│   │                                   • POST /acs/bridge   — ACS/BAP stub (M3 replaces)
│   │                                   • GET  /session/{id} — session retrieval
│   │                                   • GET  /health       — server health check
│   └── 🌐 irctc_ui.html             ← DTMF web IVR simulator
│                                       • 3-panel layout (controls / log / stats)
│                                       • DTMF keypad + service cards
│                                       • Live JSON response viewer
│                                       • Call flow step tracker
│                                       • API call history panel
│
├── 📁 Milestone_3/
│   ├── 📄 README_M3.md              ← Full M3 documentation
│   │                                   (live demo, intents, NLU engine explanation,
│   │                                    sample PNRs/trains, 3 input modes, TTS code,
│   │                                    troubleshooting guide)
│   └── 🌐 irctc_m3.html             ← Conversational AI IVR simulator
│                                       • Voice input (Web Speech API / Google STT)
│                                       • Text input (keyboard)
│                                       • DTMF keypad mode
│                                       • NLU engine — 9 intents, 130+ patterns
│                                       • Entity extraction — PNR, train, city, date, class
│                                       • State machine dialogue manager
│                                       • Text-to-Speech output (en-IN)
│                                       • Live NLU debug panel
│                                       • Session stats, intent history, result cards
│
└── 📁 Milestone_4/
    ├── 📄 README_M4.md              ← Full M4 documentation
    │                                   (5 testing layers, test descriptions,
    │                                    performance targets, 6 bug fixes table,
    │                                    deployment guide, 25-item checklist)
    └── 🐍 test_m4_ivr.py            ← Complete test suite
                                        • TestUnit          — 11 unit tests (<100ms each)
                                        • TestIntegration   — 7 integration tests
                                        • TestE2E           — 5 end-to-end journey tests
                                        • TestErrorHandling — 7 error handling tests
                                        • load_test()       — performance load test
```

---

## 🛣️ Milestone-by-Milestone Breakdown

### Milestone 1 — Legacy System Analysis & Requirements Gathering ✅

**Objective:** Understand the existing IRCTC IVR system deeply before proposing any changes.

**What was done:**
- Reviewed the complete existing IRCTC IVR architecture (VXML, DTMF, telephony gateway, ASR/TTS engine, backend APIs)
- Documented all 7 major limitations of the current system with their real-world impact
- Defined integration requirements for **Azure ACS** (telephony layer) and **BAP** (intelligence layer)
- Identified 6 key technical challenges: VXML incompatibility, context management, real-time data latency, peak load scaling, Indian language variability, and PII security
- Created a **six-phase integration roadmap** from assessment through scalability
- Produced a compatibility gap analysis table comparing traditional vs modern IVR

**Key deliverable:** `milestone1.pdf` — comprehensive legacy analysis report

---

### Milestone 2 — Integration Layer Development ✅

**Objective:** Build the FastAPI middleware that connects the IVR front-end to IRCTC backend services, and a web simulator to test it.

**What was built:**

`irctc_backend.py` — A FastAPI REST API server with:
- **IST time-aware greetings** — "Suprabhat! Good Morning!" / "Namaskar! Good Afternoon!" / "Shubh Sandhya! Good Evening!"
- **Session management** with UUID-based session IDs and full call history
- **PNR Status** — returns coach, berth number, platform, departure time, booking status
- **Smart Booking** — multi-step flow: 5 travel classes × 5 quotas × 6 berth preferences
- **Tatkal Booking** — time-gated (10 AM–11 PM IST), urgency scoring, queue position
- **Live Tracking** — current station, next station, delay reason, ETA, on-time reliability score
- **ACS/BAP Bridge Stub** — returns exact payload for M3 ACS SDK integration

`irctc_ui.html` — A browser-based DTMF phone simulator with:
- Clean professional light theme (matches M3 design)
- Three-panel layout: controls + DTMF keypad / call log / stats + API history
- Syntax-highlighted JSON response viewer
- Call flow step tracker (6 steps, done/active/pending states)
- Auto health-check on page load
- Direct PNR/train number input bar
- Clickable API endpoint tester in right panel

---

### Milestone 3 — Conversational AI Layer ✅

**Objective:** Add voice input, NLU, and natural language understanding so users can speak freely instead of pressing numbered menus.

**What was built:**

`irctc_m3.html` — A complete conversational IVR simulator running entirely in the browser:

| Component | Implementation |
|-----------|---------------|
| **Speech-to-Text** | Web Speech API → Google STT (built into Chrome/Edge) |
| **Intent Detection** | Regex + keyword NLU — 9 intents, 130+ patterns, special-case fast-paths |
| **Entity Extraction** | PNR (10-digit), train (5-digit), 15 cities, date, travel class, Tatkal flag |
| **Dialogue Manager** | JavaScript state machine — 12 states, multi-turn context preservation |
| **Text-to-Speech** | SpeechSynthesis API — en-IN voice, rate 0.94, pitch 1.05 |
| **UI** | 3-panel: sidebar (mode/queries/PNRs) / chat (bubbles/typing) / debug (NLU/stats/history) |

**Zero backend. Zero API keys. Zero cost. Runs entirely in the browser.**

---

### Milestone 4 — Testing & Deployment ✅

**Objective:** Validate the complete system through structured testing and prepare for production deployment.

**What was built:**

`test_m4_ivr.py` — A complete test suite with 30+ tests across 5 layers:

| Layer | Class | Tests | Speed |
|-------|-------|-------|-------|
| Unit | `TestUnit` | 11 tests | < 100ms each |
| Integration | `TestIntegration` | 7 tests | 1–5 seconds |
| End-to-End | `TestE2E` | 5 journey tests | 10–30 seconds |
| Load | `load_test()` | 50 requests | Standalone |
| Error Handling | `TestErrorHandling` | 7 tests | < 100ms each |

Also corrected **6 deliberate bugs** from the original sample code provided in the module.

---

## 🚀 Quick Start Guide

### Option A — Run M3 Conversational Simulator (No Setup Needed)

```bash
# Just open irctc_m3.html in Chrome or Edge
# Voice input, NLU, TTS — all works instantly with no server
```

Or use the live demo: **[ticket-assistant--24b01a4278.replit.app](https://ticket-assistant--24b01a4278.replit.app)**

---

### Option B — Run M2 Backend + DTMF Simulator

```bash
# Step 1 — Clone the repository
git clone https://github.com/Ramyasrivalli/Conversational_IVR_Modernization_Framework.git
cd Conversational_IVR_Modernization_Framework

# Step 2 — Install dependencies
pip install -r requirements.txt

# Step 3 — Start the FastAPI server
python Milestone_2/irctc_backend.py

# Step 4 — Open the simulator
# Browser → http://localhost:8000

# Step 5 — View interactive API docs
# Browser → http://localhost:8000/docs
```

---

### Option C — Run M4 Test Suite

```bash
# Terminal 1 — Start the backend
python Milestone_2/irctc_backend.py

# Terminal 2 — Run all tests
pytest Milestone_4/test_m4_ivr.py -v

# Run only one layer
pytest Milestone_4/test_m4_ivr.py -v -k "TestUnit"
pytest Milestone_4/test_m4_ivr.py -v -k "TestIntegration"
pytest Milestone_4/test_m4_ivr.py -v -k "TestE2E"
pytest Milestone_4/test_m4_ivr.py -v -k "TestErrorHandling"

# Run the load test (standalone)
python Milestone_4/test_m4_ivr.py
```

---

## 📋 IRCTC Services — What the System Handles

| # | Service | DTMF Key | Voice / Text Example | What You Get Back |
|---|---------|----------|----------------------|-------------------|
| 1 | 📋 PNR Status | `1` | "Check PNR 1234567890" | Coach, berth, platform, departure time, booking status |
| 2 | 🎫 Ticket Booking | `2` | "Book a ticket from Delhi to Mumbai on 15 April sleeper" | Available trains, fare, booking ID, payment link |
| 3 | ⚡ Tatkal Booking | `3` | "Tatkal ticket Bangalore to Chennai tomorrow" | Ref ID, surcharge, urgency score, queue position |
| 4 | 📍 Live Tracking | `4` | "Live status of train 12951" | Current station, next stop, delay, ETA |
| 5 | ❌ Cancel & Refund | `5` | "Cancel my ticket PNR 9876543210" | Cancellation preview, estimated refund |
| 6 | 💰 Fare Enquiry | — | "Fare from Delhi to Bangalore 3AC" | Base fare, Tatkal surcharge |
| 7 | 🕐 Train Schedule | — | "Schedule of train 12301" | Origin, destination, departure, arrival, distance |
| 8 | 📢 Complaint | `9` | "I have a complaint about food quality" | Complaint ref ID, response timeline |
| 9 | 👨‍💼 Talk to Agent | `9` | — | Transfer to live IRCTC support agent |

---

## 🧠 How the NLU Engine Works (M3)

The Natural Language Understanding engine is built entirely in JavaScript — no cloud API required.

### Step 1 — Intent Detection

The engine tests every input against pattern lists for 9 intents. Each match increases the confidence score.

```
User says: "Schedule of train 12301"
                │
                ▼
Special-case fast-path: /schedule\s+of\s+train/i → MATCH
                │
                ▼
Intent: train_schedule | Confidence: 100% ✅
```

```
User says: "Book a ticket from Delhi to Mumbai sleeper"
                │
                ▼
book_ticket patterns matched: book ✓ ticket ✓ from ✓
Confidence: 3/17 = 18% base → boosted by multiple matches → ~65%
                │
                ▼
Intent: book_ticket | Confidence: 65% ✅
```

### Step 2 — Entity Extraction

| What User Says | Entity Extracted |
|----------------|-----------------|
| "1234567890" (10 digits) | `pnr = 1234567890` |
| "train 12951" (5 digits) | `train = 12951` |
| "from Delhi to Mumbai" | `from = delhi`, `to = mumbai` |
| "15 April" | `date = 15 april` |
| "sleeper" / "3AC" | `cls = SL` / `3A` |
| "tatkal" | `tatkal = true` |

### Step 3 — Multi-Turn State Machine

The system remembers context so users don't have to repeat themselves:

```
Turn 1: "Book a ticket"
        → State: book_from → Ask: "Where to travel from?"

Turn 2: "Delhi"
        → State: book_to → Ask: "From Delhi — where to travel to?"

Turn 3: "Mumbai"
        → State: book_dt → Ask: "Which date?"

Turn 4: "15 April"
        → State: book_cl → Ask: "Which travel class?"

Turn 5: "Sleeper"
        → Show available trains + fare → State: idle ✅
```

---

## 🧪 Sample Test Data

### PNR Numbers

| PNR | Status | Train | Coach | Berth | Platform |
|-----|--------|-------|-------|-------|----------|
| `1234567890` | ✅ CONFIRMED | 12951 Mumbai Rajdhani | B4 | 32 (Lower) | 3 |
| `9876543210` | 🟡 RAC 12 | 12630 Yeshwantpur Exp | A2 | 15 (Side Lower) | 1 |
| `5555555555` | ❌ WL 89 | 12483 Amritsar Express | — | — | — |
| `4444444444` | ✅ CONFIRMED | 22119 Mumbai AC Express | H1 | 05 (Upper) | 5 |

### Train Numbers

| Train | Name | Route | Status |
|-------|------|-------|--------|
| `12951` | Mumbai Rajdhani Express | New Delhi → Mumbai Central | On Time |
| `12301` | Howrah Rajdhani Express | Howrah → New Delhi | On Time |
| `12630` | Yeshwantpur Express | Yeshwantpur → Howrah | 12 min late |
| `22119` | Mumbai CSMT AC Express | Lucknow → Mumbai CSMT | 5 min late |
| `12002` | Bhopal Shatabdi Express | New Delhi → Habibganj | On Time |

### Fare Reference (Sample)

| Route | Sleeper | 3rd AC | 2nd AC | 1st AC |
|-------|---------|--------|--------|--------|
| Delhi → Mumbai | ₹735 | ₹1,985 | ₹2,865 | ₹4,785 |
| Delhi → Bangalore | ₹1,205 | ₹2,785 | ₹4,025 | ₹6,675 |
| Delhi → Chennai | ₹1,265 | ₹3,005 | ₹4,345 | ₹7,225 |
| Mumbai → Bangalore | ₹580 | ₹1,430 | ₹2,050 | — |
| Bangalore → Chennai | ₹300 | ₹880 | ₹1,295 | ₹2,145 |

---

## 🔌 API Endpoints Quick Reference (M2)

| Method | Endpoint | Description | Key Request Fields |
|--------|----------|-------------|-------------------|
| `POST` | `/ivr/start` | Start session + welcome | `caller_id`, `language` |
| `POST` | `/ivr/input` | DTMF key handler | `session_id`, `digit`, `current_flow` |
| `POST` | `/ivr/pnr` | PNR status check | `session_id`, `pnr_number` |
| `POST` | `/ivr/booking` | Ticket booking | `session_id`, `train_number`, `from_station`, `to_station`, `travel_class`, `quota`, `berth_preference` |
| `POST` | `/ivr/tatkal` | Tatkal booking | `session_id`, `train_number`, `from_station`, `to_station`, `travel_class` |
| `POST` | `/ivr/tracking` | Live train tracking | `session_id`, `train_number` |
| `POST` | `/acs/bridge` | ACS/BAP stub | `session_id`, `acs_call_connection_id`, `vxml_event`, `tts_text` |
| `GET` | `/session/{id}` | Get session state | — |
| `GET` | `/health` | Server health check | — |

Full request/response examples with JSON: see **[Milestone_2/README_M2.md](Milestone_2/README_M2.md)**

---

## 🧰 Full Tech Stack

### Backend (Milestone 2)

| Component | Technology | Version |
|-----------|-----------|---------|
| REST Framework | FastAPI | 0.100+ |
| ASGI Server | Uvicorn | 0.23+ |
| Data Validation | Pydantic | v2 |
| Language | Python | 3.10+ |
| Session Storage | In-memory dict (M4: Redis) | — |
| API Documentation | Swagger UI (auto-generated) | — |

### Frontend (Milestone 3)

| Component | Technology |
|-----------|-----------|
| Language | Vanilla JavaScript ES6+ |
| UI | HTML5 + CSS3 (no framework) |
| Fonts | Plus Jakarta Sans + IBM Plex Mono |
| Speech-to-Text | Web Speech API (Google STT via browser) |
| Text-to-Speech | SpeechSynthesis API (browser-native, en-IN) |
| NLU | Custom Regex + Keyword matching |
| Dialogue | JavaScript state machine |

### Testing (Milestone 4)

| Component | Technology |
|-----------|-----------|
| Test Framework | pytest 7.4+ |
| API Testing | FastAPI TestClient (httpx) |
| Mocking | unittest.mock.patch + MagicMock |
| Load Testing | requests + time |
| Logging | Python logging (JSON format) |

### Cloud / Deployment

| Platform | Role |
|----------|------|
| Azure Communication Services (ACS) | Production telephony, STT, TTS (en-IN-NeerjaNeural) |
| BAP (Bot Application Platform) | Intent recognition, dialogue management |
| Twilio | Alternative telephony (TwiML-based) |
| Replit | Live demo hosting (M3 simulator) |
| GitHub Codespaces | Local development environment |
| Render / Railway / Heroku | Backend hosting options |

---

## 🚀 Deployment Guide

### M3 Simulator — Static Deployment (Zero Cost)

| Platform | Steps |
|----------|-------|
| **Replit** | Create project → Upload `irctc_m3.html` → Rename to `index.html` → Run |
| **Netlify Drop** | Go to `app.netlify.com/drop` → Create folder → Rename file to `index.html` → Drag folder → Get URL |
| **GitHub Pages** | Push to repo → Settings → Pages → Deploy from `main` branch |
| **Vercel** | `vercel deploy` from project folder |

### M2 Backend — Server Deployment

```bash
# Render / Railway / Heroku
# 1. Push to GitHub
# 2. Connect repo to platform
# 3. Set start command: uvicorn irctc_backend:app --host 0.0.0.0 --port $PORT

# For production — replace in-memory sessions with Redis:
# pip install redis
# import redis; r = redis.Redis(host=REDIS_URL)
```

> **Never hardcode secrets.** Use environment variables for `ACS_CONN_STR`, `TWILIO_AUTH_TOKEN`, etc.

---

## 📊 Project Roadmap

| Milestone | Status | Demo | Description |
|-----------|--------|------|-------------|
| **M1** — Legacy Analysis | ✅ Complete | — | IRCTC IVR architecture review, integration requirements, 6-phase plan |
| **M2** — Integration Layer | ✅ Complete | [▶ Live Demo](https://claude.ai/public/artifacts/6f11325f-8531-487e-a886-fdbf6ae76559) | FastAPI backend (8 endpoints) + DTMF web simulator |
| **M3** — Conversational AI | ✅ Complete | [▶ Live Demo](https://ticket-assistant--24b01a4278.replit.app) | Voice + NLU + TTS browser simulator — zero cost, zero backend |
| **M4** — Testing & Deployment | ✅ Complete | — | 30+ tests (unit/integration/E2E/load/error) + deployment guide |



*For milestone-specific documentation, see the README inside each milestone folder.*

# 🚂 IRCTC Smart IVR — Integration Layer
## Milestone 2: FastAPI Backend + Web IVR Simulator

> **Project:** Conversational IVR Modernization Framework
> **Author:** M. Ramya Srivalli | Infosys Intern | Batch 13, Group-2
> **Organization:** Infosys Internship Project

---

## 📌 What is Milestone 2?

Milestone 2 builds the **integration layer** — the middleware that connects the legacy IRCTC IVR system with modern conversational platforms (ACS/BAP). It delivers two things:

1. **`irctc_backend.py`** — A fully functional FastAPI REST API server that handles all IVR call logic, session management, and IRCTC service simulation
2. **`irctc_ui.html`** — A web-based IVR simulator that runs in any browser, letting you interact with the backend as if you were calling from a real phone

**Why both?** Real phone testing requires paid Twilio/ACS accounts and phone numbers. The web simulator gives you a zero-cost, zero-setup way to test and demo the exact same IVR logic that would run in production.

---

## 🏗️ System Architecture

```
[Web Browser — irctc_ui.html]
         |
         |  HTTP POST (fetch API)
         |
         v
[FastAPI Server — irctc_backend.py]   ← THIS IS MILESTONE 2
         |
         |── POST /ivr/start      → Creates session, returns welcome prompt
         |── POST /ivr/input      → Handles DTMF key press, routes menus
         |── POST /ivr/pnr        → PNR Status lookup
         |── POST /ivr/booking    → Smart Ticket Booking flow
         |── POST /ivr/tatkal     → Tatkal Emergency Booking
         |── POST /ivr/tracking   → Live Train Tracking
         |── POST /acs/bridge     → ACS/BAP connector stub (Milestone 3 replaces)
         |── GET  /health         → Server health check
         |
         v
[ACS / BAP Conversational AI]  ← Milestone 3 will connect here
         |
         v
[Voice Response to Caller]
```

---

## 📂 Project Files

```
Milestone 2/
├── irctc_backend.py    → FastAPI server — the complete IVR integration layer
└── irctc_ui.html       → Web IVR Simulator UI — browser-based phone interface
```

---

## ⚙️ How the Web Simulator Works

### The Core Concept

A **web-based IVR simulator** replicates a real phone call entirely inside the browser. No phone, no phone number, no cloud account required.

| Real IVR (Phone) | Web Simulator (Browser) |
|---|---|
| You dial the IRCTC number | You click **"START CALL"** |
| Robot voice speaks the menu | Text prompts appear on screen |
| You press 1, 2, 3 on keypad | You click number buttons on screen |
| DTMF tones are sent | JavaScript captures your click |
| IVR routes your call | FastAPI routes your request |
| Call ends | Session is terminated |

**Same logic. Same backend. Different interface.** Think of it like a flight simulator — the controls are different from a real plane, but the underlying system behaviour is identical.

### Architecture: Frontend ↔ Backend Communication

```
┌─────────────────────────────────────────────┐
│         FRONTEND (irctc_ui.html)            │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Phone Interface (HTML/CSS)           │  │
│  │  - DTMF Dialpad (1-9, *, 0, #)      │  │
│  │  - Display screen (shows prompts)    │  │
│  │  - Start Call / End Call buttons     │  │
│  │  - Service cards (PNR, Booking, etc) │  │
│  │  - JSON response viewer              │  │
│  └──────────────────────────────────────┘  │
│               ↕ JavaScript fetch()          │
│  ┌──────────────────────────────────────┐  │
│  │  Session State Manager               │  │
│  │  - sessionId (unique call ID)        │  │
│  │  - currentMenu (which menu open)     │  │
│  │  - call history log                  │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                 ↕ HTTP POST/GET
┌─────────────────────────────────────────────┐
│         BACKEND (irctc_backend.py)          │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  FastAPI Endpoints                   │  │
│  │  - /ivr/start  /ivr/input           │  │
│  │  - /ivr/pnr    /ivr/booking         │  │
│  │  - /ivr/tatkal /ivr/tracking        │  │
│  │  - /acs/bridge (M3 stub)            │  │
│  └──────────────────────────────────────┘  │
│               ↕                             │
│  ┌──────────────────────────────────────┐  │
│  │  In-Memory Session Store             │  │
│  │  - Active call sessions              │  │
│  │  - Booking slot tracking             │  │
│  │  - Call history per session          │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 📋 PNR Status Check | Real-time PNR lookup with coach, berth, platform, and booking status |
| 🎫 Smart Ticket Booking | Multi-level flow — class selection → quota → berth preference |
| ⚡ Tatkal Emergency Booking | Priority booking with urgency scoring and queue position |
| 📍 Live Train Tracking | Current station, delay status, next station, and ETA |
| 🔌 ACS/BAP Bridge Stub | VXML event translator endpoint — stub ready for Milestone 3 |
| 🖥️ Web IVR Simulator | Interactive UI with DTMF dialpad, JSON viewer, and call log |
| 📋 Session Management | Full call history and booking slot tracking per session |
| 🏥 Health Check | `/health` endpoint for server status monitoring |

---

## 🚀 How to Run

### Prerequisites

```
Python 3.10 or above
```

### Step 1 — Install Dependencies

```bash
pip install fastapi uvicorn requests
```

### Step 2 — Start the FastAPI Server

```bash
python irctc_backend.py
```

You will see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Step 3 — Open the Simulator

Open your browser and go to:
```
http://localhost:8000
```

The server automatically serves `irctc_ui.html` as the frontend.

### Step 4 — Access API Documentation

Swagger UI (interactive API docs — auto-generated by FastAPI):
```
http://localhost:8000/docs
```

---

## 🎮 How to Use the Web Simulator

Follow this step-by-step walkthrough to test every feature:

```
Step 1 → Click "START CALL"
         A unique Session ID is created
         Welcome prompt appears on screen

Step 2 → Press "1" on the dialpad
         Routes to PNR Status flow

Step 3 → Click the "PNR STATUS" card
         Returns: Train number, Coach B4, Berth 32, Platform 1, Status: CONFIRMED

Step 4 → Press "2" on the dialpad
         Routes to Smart Ticket Booking
         → Select class: 1=Sleeper / 2=3AC / 3=2AC / 4=1AC / 5=Chair Car
         → Select quota: 1=General / 2=Ladies / 3=Senior Citizen
         → Select berth preference: 1=Lower / 2=Middle / 3=Upper
         Click "SMART BOOKING" card
         Returns: Booking ID, Estimated Fare, Payment Link

Step 5 → Press "3" on the dialpad
         Click "TATKAL EMERGENCY" card
         Returns: Ref ID, Tatkal Surcharge, Urgency Score, Queue Position

Step 6 → Press "4" on the dialpad
         Click "LIVE TRACKING" card
         Returns: Current Station, Next Station, Delay Minutes, ETA

Step 7 → Click "END CALL"
         Session is terminated and logged
```

---

## 🐛 Debugging Guide

### Issue 1: CORS Error in Browser

**Error:**
```
Access to fetch at 'http://localhost:8000' blocked by CORS policy
```

**Fix:** The backend already has CORS middleware. Ensure you are opening the simulator at `http://localhost:8000` (served by FastAPI), not by double-clicking the HTML file directly.

---

### Issue 2: Backend Not Responding

**Symptoms:** Clicking "START CALL" does nothing. Console shows network error.

**Fix:**
1. Confirm the server is running — terminal shows `Uvicorn running on http://127.0.0.1:8000`
2. Open `http://localhost:8000/health` in your browser — should return JSON
3. Check that port 8000 is not occupied by another process

---

### Issue 3: Session Not Found

**Error:** `{"error": "Session not found"}`

**Fix:** Sessions are stored in memory and reset when the server restarts. Click "END CALL" then "START CALL" to create a fresh session.

---

## 🛣️ Milestone Roadmap

| Milestone | Status | Description |
|---|---|---|
| M1 | ✅ Complete | Legacy system analysis & requirements — `milestone1.pdf` |
| M2 | ✅ Complete | Integration layer — this project |
| M3 | 🔄 Upcoming | Conversational AI — Voice + NLU + TTS |
| M4 | 🔄 Upcoming | Real phone IVR via Twilio / Azure ACS |

---

## 🧰 Tech Stack

| Component | Technology |
|---|---|
| REST API Framework | FastAPI |
| ASGI Server | Uvicorn |
| Data Validation | Pydantic |
| Frontend | HTML + CSS + JavaScript |
| Session Storage | In-memory Python dict |
| API Docs | Swagger UI (auto-generated by FastAPI) |
| Target Cloud (M3+) | Azure Communication Services + BAP |

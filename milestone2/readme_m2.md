# ⚙️ Milestone 2 — Integration Layer Development

> **Project:** Conversational IVR Modernization Framework
> **Author:** M. Ramya Srivalli | Infosys Intern | Batch 13, Group-2
> **Organization:** Infosys Internship Project

---

## 🌐 Live Demo

👉 **[https://claude.ai/public/artifacts/6f11325f-8531-487e-a886-fdbf6ae76559](https://claude.ai/public/artifacts/6f11325f-8531-487e-a886-fdbf6ae76559)**

> Click **START CALL** → use the DTMF keypad or service cards → see live JSON responses.
> Note: API calls to the FastAPI backend will not respond in the static demo — the UI layout and simulator interface are fully visible.

---

## 📌 What is Milestone 2?

Milestone 2 builds the **integration layer** — the FastAPI middleware that sits between the browser/telephone front-end and the IRCTC backend services. It also delivers a fully functional web-based IVR simulator so the entire system can be tested and demonstrated without a real phone or paid cloud account.

**Two deliverables:**

| File | What It Is |
|------|-----------|
| `irctc_backend.py` | FastAPI REST API — 8 endpoints covering all IRCTC IVR services |
| `irctc_ui.html` | Web IVR simulator — browser-based DTMF phone interface |

---

## 📂 Files

```
Milestone_2/
├── README_M2.md        ← This file
├── irctc_backend.py    ← FastAPI integration layer (main backend)
└── irctc_ui.html       ← DTMF web simulator (frontend)
```

---

## 🏗️ System Architecture

```
[Web Browser — irctc_ui.html]
         │  JavaScript fetch() HTTP POST
         ▼
┌─────────────────────────────────────────────────┐
│         FastAPI Server — irctc_backend.py        │  ← MILESTONE 2
│                                                  │
│  POST /ivr/start     → Session creation + welcome prompt       │
│  POST /ivr/input     → Universal DTMF key handler + routing    │
│  POST /ivr/pnr       → PNR Status lookup                       │
│  POST /ivr/booking   → Smart Ticket Booking (class/quota/berth)│
│  POST /ivr/tatkal    → Tatkal Emergency Booking                 │
│  POST /ivr/tracking  → Live Train Location & Delay             │
│  GET  /session/{id}  → Session state retrieval                 │
│  POST /acs/bridge    → ACS/BAP event translator stub           │
│  GET  /health        → Server health + active session count    │
│                                                  │
│  In-Memory Session Store (SESSIONS dict)         │
│  - session_id, caller_id, language               │
│  - current_flow, booking_slots                   │
│  - call history log                              │
└──────────────────────────────────────────────────┘
         │  (M3 connects here)
         ▼
[ACS / BAP Conversational AI]  ← Milestone 3
         │
         ▼
[IRCTC Backend Services — PNR DB, PRS, NTES, Payment]
```

---

## 🌐 How the Web Simulator Works

A **web-based IVR simulator** replicates a real phone call entirely inside the browser. No phone, no phone number, no cloud account is required.

| Real Phone Call | Web Simulator |
|----------------|--------------|
| You dial 139 | You click **START CALL** |
| Robot voice speaks the menu | Text prompts appear on screen |
| You press 1, 2, 3 on phone keypad | You click number buttons on screen |
| DTMF tones sent to server | JavaScript sends `POST /ivr/input` |
| IVR processes and responds | FastAPI processes and responds |
| You hear the response | JSON response shown in log panel |
| Call ends | Session is terminated |

**Analogy:** A flight simulator teaches the same skills as a real plane — different controls, same logic underneath.

### Frontend ↔ Backend Communication

```
┌──────────────────────────────────────────────┐
│        FRONTEND (irctc_ui.html)              │
│                                              │
│  Three-Panel Layout:                         │
│  LEFT: Call controls + DTMF keypad           │
│        + Service cards + Flow steps          │
│                                              │
│  CENTRE: Call log with chat bubbles          │
│          + JSON response viewer              │
│          + Text input + Send button          │
│                                              │
│  RIGHT: Session stats + API call history     │
│         + Last response card + Endpoints     │
└──────────────────────────────────────────────┘
              ↕  HTTP POST/GET  ↕
┌──────────────────────────────────────────────┐
│        BACKEND (irctc_backend.py)            │
│                                              │
│  FastAPI with 9 endpoints                    │
│  Pydantic request/response models            │
│  In-memory session dictionary                │
│  CORS middleware enabled (allow all origins) │
│  Auto-generated Swagger UI at /docs          │
└──────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📋 PNR Status Check | Returns coach, berth number, platform, journey date, and booking status |
| 🎫 Smart Ticket Booking | Multi-step flow — class selection (5 options) → quota (5 options) → berth preference (6 options) |
| ⚡ Tatkal Emergency Booking | Priority booking with time-gated window, urgency scoring, and queue position |
| 📍 Live Train Tracking | Current station, next station, delay minutes, delay reason, and ETA |
| 🔌 ACS/BAP Bridge Stub | VXML event translator — returns exact payload for M3 ACS SDK integration |
| 📋 Session Management | UUID-based sessions with full call history, booking slots, and IST time-aware greetings |
| 🏥 Health Check | `/health` returns version, active session count, endpoint list |
| 📖 Swagger UI | Auto-generated interactive API docs at `/docs` |

---

## 🚀 How to Run

### Step 1 — Install dependencies

```bash
pip install fastapi uvicorn requests
```

### Step 2 — Start the FastAPI server

```bash
python irctc_backend.py
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Step 3 — Open the simulator

```
http://localhost:8000
```

The server automatically serves `irctc_ui.html` as the frontend.

### Step 4 — Access interactive API docs

```
http://localhost:8000/docs
```

---

## 🎮 Complete Simulator Walkthrough

```
Step 1 → Click "START CALL"
         → Session ID created (e.g., 3a7f92bc-...)
         → IST time-aware greeting plays:
           "Suprabhat! Welcome to IRCTC Smart Railway Services..."
         → Main menu announced: Press 1-5, 9 for agent, 0 to repeat

Step 2 → Press "1" on DTMF keypad
         → Routes to PNR Status flow
         → Prompt: "Please enter your 10-digit PNR number followed by hash"

Step 3 → Type "1234567890" in input box OR click PNR Status service card
         → POST /ivr/pnr called
         → Returns: Train 12951, Coach B4, Berth 32 (Lower),
                    Platform 1, Departure 16:55, Status CONFIRMED

Step 4 → Press "2" on DTMF keypad
         → Routes to Smart Ticket Booking
         → Press 1 = Sleeper / 2 = Third AC / 3 = Second AC / 4 = First AC / 5 = Chair Car
         → Press 1 = General / 2 = Ladies / 3 = Senior Citizen / 4 = Defence / 5 = Tourist
         → Press 1 = Lower / 2 = Middle / 3 = Upper / 4 = Side Lower / 5 = Side Upper / 6 = No Pref
         → Click "Smart Booking" service card to confirm
         → Returns: Booking ID (BK + UUID), Fare ₹450–₹3200, Payment link

Step 5 → Press "3" on DTMF keypad
         → Routes to Tatkal Emergency Booking
         → Click "Tatkal" card (only works 10 AM–11 PM IST)
         → Returns: Ref ID (TK + UUID), Surcharge ₹200–₹700,
                    Urgency Score (0–100), Queue Position

Step 6 → Press "4" on DTMF keypad
         → Routes to Live Train Tracking
         → Type any 5-digit train number OR click "Live Tracking" card
         → Returns: Current station (Mathura Junction),
                    Next station (Agra Cantt), ETA 14:32,
                    Delay 12 min (Signal clearance), On-time score 87%

Step 7 → Press "9" on DTMF keypad
         → Agent transfer triggered
         → Prompt: "Connecting you to an IRCTC support agent. Please hold."

Step 8 → Click "END CALL"
         → Session terminated and logged
```

---

## 📡 API Endpoints Reference

### `POST /ivr/start`
Creates a session and returns an IST time-aware greeting with the full main menu.

**Request:**
```json
{ "caller_id": "WebSimulator", "language": "EN" }
```

**Response:**
```json
{
  "status": "success",
  "prompt": "Suprabhat! Good Morning! Welcome to IRCTC Smart Railway Services...",
  "data": {
    "session_id": "3a7f92bc-1234-5678-abcd-ef1234567890",
    "menu": { "1": "PNR Status Check", "2": "Smart Ticket Booking", ... },
    "next_action": "collect_dtmf"
  }
}
```

---

### `POST /ivr/input`
Processes a DTMF key press and routes to the correct service flow.

**Request:**
```json
{ "session_id": "3a7f92bc...", "digit": "2", "current_flow": "main_menu" }
```

**Response:**
```json
{
  "status": "success",
  "prompt": "Smart Ticket Booking. Select class: 1 Sleeper, 2 Third AC...",
  "data": { "selected": "Smart Ticket Booking", "next_collect": "journey_details" }
}
```

---

### `POST /ivr/pnr`
Looks up PNR details and returns full booking information.

**Request:**
```json
{ "session_id": "3a7f92bc...", "pnr_number": "1234567890" }
```

**Response:**
```json
{
  "status": "success",
  "prompt": "PNR 1234567890: CONFIRMED. Train 12951 Mumbai Rajdhani...",
  "data": {
    "pnr_details": {
      "pnr": "1234567890", "train": "12951 — Mumbai Rajdhani Express",
      "from": "NDLS (New Delhi)", "to": "MMCT (Mumbai Central)",
      "date": "15-Mar-2026", "class": "Third AC (3A)",
      "status": "CONFIRMED", "coach": "B4", "berth": "32 — Lower",
      "platform": "Platform 1", "departure": "16:55", "arrival": "08:35 +1"
    }
  }
}
```

---

### `POST /ivr/booking`
Processes a full ticket booking with class, quota, and berth.

**Request:**
```json
{
  "session_id": "3a7f92bc...",
  "train_number": "12951", "journey_date": "15-Apr-2026",
  "from_station": "NDLS", "to_station": "MMCT",
  "travel_class": "1", "quota": "1", "berth_preference": "1",
  "passenger_count": 1
}
```

**Response:**
```json
{
  "status": "success",
  "prompt": "Booking ID BK3A7F92BC created. Train 12951, Sleeper, General. Estimated fare ₹450...",
  "data": {
    "booking": {
      "booking_id": "BK3A7F92BC", "train": "12951", "class": "Sleeper (SL)",
      "quota": "General", "berth": "Lower", "fare": "₹450",
      "status": "PENDING_PAYMENT", "pay_link": "https://irctc.co.in/pay/BK3A7F92BC"
    }
  }
}
```

---

### `POST /ivr/tatkal`
Initiates Tatkal emergency booking (time-gated: 10 AM–11 PM IST).

**Response (success):**
```json
{
  "status": "success",
  "data": {
    "tatkal": {
      "ref": "TK3F9B2A", "surcharge": "₹200", "urgency_score": 72,
      "queue_position": 3, "status": "TATKAL_QUEUED"
    }
  }
}
```

**Response (outside window):**
```json
{ "status": "unavailable", "prompt": "Tatkal window closed. Opens at 10 AM IST for AC, 11 AM for Sleeper." }
```

---

### `POST /ivr/tracking`
Returns live train location, delay status, and ETA for next station.

**Response:**
```json
{
  "status": "success",
  "data": {
    "tracking": {
      "train_number": "12951", "current_station": "Mathura Junction (MTJ)",
      "next_station": "Agra Cantt (AGC)", "eta_next_station": "14:32",
      "delay_minutes": 12, "delay_reason": "Signal clearance at Mathura",
      "distance_covered_km": 148, "total_distance_km": 1384,
      "on_time_score": "87%"
    }
  }
}
```

---

### `POST /acs/bridge`
VXML-to-ACS event translator stub. Returns the exact payload that will go to Azure ACS in Milestone 3.

**Request:**
```json
{
  "session_id": "3a7f92bc...",
  "acs_call_connection_id": "ACS_CALL_001",
  "vxml_event": "filled",
  "tts_text": "Welcome to IRCTC",
  "collect_digits": true,
  "max_digits": 1
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "bridge_payload": {
      "platform": "ACS", "directive": "USER_INPUT_RECEIVED",
      "voice": "en-IN-NeerjaNeural", "collect_digits": true, "max_digits": 1
    },
    "m3_todo": "Replace stub: conn.start_recognizing_media(...) with bridge_payload above"
  }
}
```

---

### `GET /health`
Server health check with active session count.

**Response:**
```json
{
  "status": "success",
  "data": { "version": "2.0.0", "milestone": "M2", "active_sessions": 3 }
}
```

---

## 🔌 ACS/BAP Bridge — What the M3 Stub Does

The `/acs/bridge` endpoint currently returns a **stub** showing the exact payload that would be sent to Azure ACS. In Milestone 3, the stub body is replaced with the real ACS SDK call:

```python
# Milestone 3 — real ACS SDK replaces the stub
from azure.communication.callautomation import (
    CallAutomationClient, TextSource, RecognizeInputType
)

client = CallAutomationClient.from_connection_string(ACS_CONN_STR)
conn = client.get_call_connection(payload.acs_call_connection_id)

conn.start_recognizing_media(
    input_type=RecognizeInputType.DTMF,
    play_prompt=TextSource(
        text=payload.tts_text,
        voice_name="en-IN-NeerjaNeural"
    ),
    max_tones_to_collect=payload.max_digits,
    operation_context="irctc_main_menu"
)
```

---

## 🐛 Debugging Guide

### Issue 1 — CORS error in browser console

```
Access to fetch at 'http://localhost:8000' blocked by CORS policy
```

**Fix:** Open the simulator at `http://localhost:8000` (served by FastAPI), not by double-clicking `irctc_ui.html`. The backend already has CORS middleware enabled for all origins.

---

### Issue 2 — Backend not responding when you click START CALL

**Checklist:**
1. Confirm terminal shows `Uvicorn running on http://127.0.0.1:8000`
2. Visit `http://localhost:8000/health` directly — should return JSON
3. Check port 8000 is not in use by another process: `lsof -i :8000` (Linux/Mac) or check Task Manager (Windows)

---

### Issue 3 — Session not found error

```json
{"detail": "Session not found or expired."}
```

**Fix:** Sessions live in memory and are lost when the server restarts. Click **END CALL** then **START CALL** to create a fresh session after any restart.

---

### Issue 4 — Tatkal returns "unavailable"

This is intentional — Tatkal booking is time-gated to **10 AM–11 PM IST**. Outside this window the endpoint correctly returns `status: unavailable`. Test it during the correct hours or temporarily modify the time check in `irctc_backend.py` for testing.

---

## 🛣️ Milestone Roadmap

| Milestone | Status | Demo | Description |
|-----------|--------|------|-------------|
| **M1** | ✅ Complete | — | Legacy analysis & requirements gathering |
| **M2** | ✅ Complete | [▶ Live Demo](https://claude.ai/public/artifacts/6f11325f-8531-487e-a886-fdbf6ae76559) | Integration layer — **this milestone** |
| **M3** | 🔜 Upcoming | [▶ Live Demo](https://ticket-assistant--24b01a4278.replit.app) | Conversational AI — Voice + NLU + TTS |
| **M4** | 🔜 Upcoming | — | Testing & deployment |

---

## 🧰 Tech Stack

| Component | Technology |
|-----------|-----------|
| REST API Framework | FastAPI 0.100+ |
| ASGI Server | Uvicorn |
| Data Validation | Pydantic v2 |
| Session Storage | In-memory Python dict (M4: Redis for production) |
| Frontend | HTML5 + CSS3 + Vanilla JavaScript |
| Fonts | Plus Jakarta Sans + IBM Plex Mono |
| API Documentation | Swagger UI (auto-generated at `/docs`) |
| Target Cloud — M3+ | Azure Communication Services + BAP |

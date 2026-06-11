# Milestone 2 — FastAPI Integration Layer & DTMF Simulator

> **Objective:** Build the FastAPI middleware that connects the IVR front-end to IRCTC backend services, and a web simulator to test it.

[![M2 Live Demo](https://img.shields.io/badge/M2%20Demo-Claude-blueviolet.svg)](https://claude.ai/public/artifacts/6f11325f-8531-487e-a886-fdbf6ae76559)

---

## 📄 Files in This Milestone

| File | Description |
|---|---|
| `irctc_backend.py` | FastAPI REST API server — 8 endpoints, session management, IST greetings |
| `irctc_ui.html` | Browser-based DTMF phone simulator — 3-panel UI, JSON viewer, call flow tracker |
| `README_M2.md` | This file |

---

## 🚀 How to Run

```bash
# Step 1 — Install dependencies (from repo root)
pip install -r requirements.txt

# Step 2 — Start the server
python Milestone_2/irctc_backend.py

# Step 3 — Open the DTMF simulator
# Browser → http://localhost:8000

# Step 4 — Interactive API docs (Swagger UI)
# Browser → http://localhost:8000/docs
```

The server prints: `✅ IRCTC IVR Backend running on http://localhost:8000`

---

## 🔌 All 9 Endpoints

### 1. `POST /ivr/start` — Start a New IVR Session

**Request:**
```json
{
  "caller_id": "+91-9876543210",
  "language": "en"
}
```

**Response:**
```json
{
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Namaskar! Good Afternoon! Welcome to IRCTC 139. Press 1 for PNR Status, Press 2 for Ticket Booking, Press 3 for Tatkal, Press 4 for Train Tracking, Press 5 for Cancellation, Press 9 for Agent.",
  "options": ["1", "2", "3", "4", "5", "9"],
  "language": "en",
  "timestamp": "2026-06-11T14:30:00+05:30",
  "greeting_type": "afternoon"
}
```

**IST Greeting Logic:**
| IST Time | Greeting |
|---|---|
| 5:00 AM – 11:59 AM | "Suprabhat! Good Morning!" |
| 12:00 PM – 4:59 PM | "Namaskar! Good Afternoon!" |
| 5:00 PM – 8:59 PM | "Shubh Sandhya! Good Evening!" |
| 9:00 PM – 4:59 AM | "Shubh Ratri! Good Night!" |

---

### 2. `POST /ivr/input` — Handle DTMF Key Press

**Request:**
```json
{
  "session_id": "a1b2c3d4-...",
  "digit": "1",
  "current_flow": "main_menu"
}
```

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "flow": "pnr_status",
  "message": "Please enter your 10-digit PNR number followed by hash.",
  "next_action": "collect_pnr",
  "valid": true
}
```

---

### 3. `POST /ivr/pnr` — Check PNR Status

**Request:**
```json
{
  "session_id": "a1b2c3d4-...",
  "pnr_number": "1234567890"
}
```

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "pnr": "1234567890",
  "status": "CONFIRMED",
  "train_number": "12951",
  "train_name": "Mumbai Rajdhani Express",
  "from_station": "NDLS",
  "to_station": "BCT",
  "departure": "16:55",
  "arrival": "08:35+1",
  "coach": "B4",
  "berth_number": "32",
  "berth_type": "Lower",
  "platform": "3",
  "message": "PNR 1234567890 — Status: CONFIRMED. Train 12951 Mumbai Rajdhani Express. Coach B4, Berth 32 Lower. Departs Platform 3 at 16:55.",
  "tts_text": "Your PNR is confirmed. Train number 12951, Mumbai Rajdhani Express. Coach B4, Berth 32 Lower. Platform 3. Departure at 16:55."
}
```

**Sample PNR numbers for testing:**
| PNR | Status |
|---|---|
| `1234567890` | CONFIRMED — 12951, B4/32 Lower |
| `9876543210` | RAC 12 — 12630, A2/15 Side Lower |
| `5555555555` | WL 89 — 12483 |
| `4444444444` | CONFIRMED — 22119, H1/05 Upper |

---

### 4. `POST /ivr/booking` — Book a Ticket

**Request:**
```json
{
  "session_id": "a1b2c3d4-...",
  "train_number": "12951",
  "from_station": "NDLS",
  "to_station": "BCT",
  "travel_class": "SL",
  "quota": "GN",
  "berth_preference": "lower"
}
```

**Travel Classes:** `SL` (Sleeper), `3A` (3rd AC), `2A` (2nd AC), `1A` (1st AC), `CC` (Chair Car)
**Quotas:** `GN` (General), `TQ` (Tatkal), `LD` (Ladies), `HP` (Handicapped), `FT` (Foreign Tourist)
**Berth Preferences:** `lower`, `middle`, `upper`, `side_lower`, `side_upper`, `no_preference`

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "booking_id": "BK-2026-NDLS-BCT-7823",
  "train": "12951 Mumbai Rajdhani Express",
  "from": "NDLS — New Delhi",
  "to": "BCT — Mumbai Central",
  "class": "SL — Sleeper",
  "quota": "GN — General",
  "berth_preference": "lower",
  "fare": 735,
  "availability": "AVAILABLE — 43 seats",
  "payment_link": "https://pay.irctc.co.in/BK-2026-NDLS-BCT-7823",
  "valid_until": "2026-06-11T15:15:00+05:30",
  "message": "Booking initiated. Train 12951 from NDLS to BCT. Sleeper class, ₹735. Pay within 15 minutes.",
  "tts_text": "Booking ready. Train 12951 Mumbai Rajdhani Express. Sleeper class. Fare 735 rupees. Please complete payment within 15 minutes."
}
```

---

### 5. `POST /ivr/tatkal` — Tatkal Emergency Booking

**Request:**
```json
{
  "session_id": "a1b2c3d4-...",
  "train_number": "12951",
  "from_station": "NDLS",
  "to_station": "BCT",
  "travel_class": "3A"
}
```

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "tatkal_ref": "TK-2026-7823-NDLS",
  "status": "QUEUE_POSITION_12",
  "fare": 1985,
  "tatkal_surcharge": 400,
  "total_fare": 2385,
  "urgency_score": 87,
  "window_open": true,
  "window_closes": "2026-06-11T23:00:00+05:30",
  "message": "Tatkal booking queued. Position 12. 3rd AC. Fare ₹2385 (including ₹400 surcharge). Window closes at 11 PM.",
  "tts_text": "Tatkal booking initiated. Queue position 12. Total fare 2385 rupees including Tatkal surcharge. Complete payment to confirm."
}
```

> Tatkal is only available **10:00 AM – 11:00 PM IST**. Outside these hours the endpoint returns a `window_open: false` response with the next opening time.

---

### 6. `POST /ivr/tracking` — Live Train Tracking

**Request:**
```json
{
  "session_id": "a1b2c3d4-...",
  "train_number": "12951"
}
```

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "train_number": "12951",
  "train_name": "Mumbai Rajdhani Express",
  "current_station": "Kota Junction",
  "current_station_code": "KOTA",
  "next_station": "Ratlam Junction",
  "next_station_code": "RTM",
  "scheduled_departure": "20:15",
  "actual_departure": "20:27",
  "delay_minutes": 12,
  "delay_reason": "Signal hold at Sawai Madhopur",
  "eta_destination": "08:47+1",
  "on_time_reliability": 94,
  "message": "Train 12951 is at Kota Junction. Delayed by 12 minutes. Next station: Ratlam Junction. ETA Mumbai: 08:47.",
  "tts_text": "Train 12951 Mumbai Rajdhani Express is currently at Kota Junction. Running 12 minutes late. Expected arrival Mumbai Central at 08 47."
}
```

---

### 7. `POST /acs/bridge` — ACS/BAP Integration Stub

This endpoint simulates the bridge between Azure ACS call automation events and the IRCTC backend. In Milestone 3, the real ACS SDK replaces this stub.

**Request:**
```json
{
  "session_id": "a1b2c3d4-...",
  "acs_call_connection_id": "acs-call-xyz-789",
  "vxml_event": "speech_recognized",
  "tts_text": "Please enter your PNR",
  "speech_transcript": "check pnr one two three four five six seven eight nine zero"
}
```

**Response:**
```json
{
  "acs_action": "play_tts",
  "tts_text": "Please enter your PNR",
  "voice": "en-IN-NeerjaNeural",
  "next_event": "collect_dtmf",
  "session_id": "a1b2c3d4-...",
  "bap_payload": {
    "intent": "pnr_status",
    "entities": { "pnr": "1234567890" },
    "confidence": 0.94,
    "dialogue_state": "pnr_lookup"
  }
}
```

---

### 8. `GET /session/{session_id}` — Get Session State

**Response:**
```json
{
  "session_id": "a1b2c3d4-...",
  "caller_id": "+91-9876543210",
  "language": "en",
  "current_flow": "pnr_status",
  "history": [
    { "timestamp": "14:30:00", "action": "session_start", "input": null },
    { "timestamp": "14:30:05", "action": "dtmf_input", "input": "1" },
    { "timestamp": "14:30:12", "action": "pnr_lookup", "input": "1234567890" }
  ],
  "created_at": "2026-06-11T14:30:00+05:30",
  "last_activity": "2026-06-11T14:30:12+05:30"
}
```

---

### 9. `GET /health` — Server Health Check

**Response:**
```json
{
  "status": "healthy",
  "service": "IRCTC IVR Backend",
  "version": "2.0.0",
  "timestamp": "2026-06-11T14:30:00+05:30",
  "endpoints_active": 8,
  "sessions_active": 3
}
```

---

## 🖥️ DTMF Simulator — `irctc_ui.html`

Open `irctc_ui.html` in any browser while the backend is running at `localhost:8000`.

### Three-Panel Layout

```
┌──────────────────┬──────────────────────┬─────────────────────┐
│   CONTROLS       │   CALL LOG           │   STATS & HISTORY   │
│                  │                      │                      │
│  [Start Call]    │  14:30 — Session     │  Active Sessions: 3  │
│  [End Call]      │  started             │  Total Calls Today:  │
│                  │                      │  127                 │
│  PNR: [_______]  │  14:30 — Welcome     │                      │
│  Train: [_____]  │  message played      │  API Call History:   │
│  [Check PNR]     │                      │  POST /ivr/start ✅  │
│  [Track Train]   │  14:30 — User        │  POST /ivr/input ✅  │
│                  │  pressed: 1          │  POST /ivr/pnr  ✅  │
│  DTMF Keypad:    │                      │                      │
│  [1][2][3]       │  14:30 — PNR flow    │  Response JSON:      │
│  [4][5][6]       │  initiated           │  { "status":         │
│  [7][8][9]       │                      │    "CONFIRMED",      │
│  [*][0][#]       │  14:30 — Result:     │    "coach": "B4" ... │
│                  │  CONFIRMED ✅        │  }                   │
└──────────────────┴──────────────────────┴─────────────────────┘
```

### Features
- **Auto health-check** on page load — turns green if backend is running
- **Direct PNR/train input** bar — type and press Enter or click the button
- **DTMF keypad** — click keys to send digits to the `/ivr/input` endpoint
- **Syntax-highlighted JSON** response viewer in right panel
- **Call flow step tracker** — 6 steps with done/active/pending states
- **Service cards** — one-click shortcuts to each IVR service

---

## 🐛 Debugging Guide

**"Server not found" / health check fails:**
```bash
# Check that the server is running
python Milestone_2/irctc_backend.py
# Should print: ✅ IRCTC IVR Backend running on http://localhost:8000
```

**"CORS error" in browser console:**
The backend has CORS fully open for development. If you see CORS errors, ensure you're running `irctc_ui.html` via HTTP (not `file://`):
```bash
# Use Python's built-in server to serve the HTML
python -m http.server 3000
# Then open http://localhost:3000/Milestone_2/irctc_ui.html
```

**PNR returns "not found":**
Only the 4 sample PNRs are implemented. Use: `1234567890`, `9876543210`, `5555555555`, `4444444444`.

**Tatkal returns "window closed":**
Tatkal is time-gated. The endpoint is only active 10:00 AM – 11:00 PM IST.

# 🚂 IRCTC Smart IVR — Integration Layer (Milestone 2)

> **Project:** Conversational IVR Modernization Framework
> **Module:** Module 2 — Integration Layer Development
> **Organization:** Infosys Internship Project

---

## 📌 About This Project

This project modernizes the traditional IRCTC IVR (Interactive Voice Response) system by building a **FastAPI-based middleware integration layer** that connects legacy VXML-based IVR systems with modern Conversational AI platforms (ACS/BAP).

Milestone 2 delivers a **fully functional REST API integration layer** with a web-based IVR simulator that demonstrates real-time call flows, DTMF handling, and JSON-based communication.

---

## 🏗️ System Architecture

```
[Caller / Web Browser]
        |
        v
[FastAPI Integration Layer]   ← Milestone 2 (This Project)
        |
        |── POST /ivr/start     → Welcome prompt + session creation
        |── POST /ivr/input     → DTMF key press handler
        |── POST /ivr/pnr       → PNR Status Check
        |── POST /ivr/booking   → Smart Ticket Booking
        |── POST /ivr/tatkal    → Tatkal Emergency Booking
        |── POST /ivr/tracking  → Live Train Tracking
        |── POST /acs/bridge    → ACS/BAP connector (stub → M3)
        |── GET  /health        → Server health check
        v
[ACS / BAP Conversational AI]  ← Milestone 3 will connect here
        |
        v
[Voice Response to Caller]
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎫 PNR Status Check | Real-time PNR status with coach, berth & platform info |
| 🚂 Smart Ticket Booking | Multi-level booking — class + quota + berth selection |
| ⚡ Tatkal Emergency Booking | Priority booking with urgency scoring & queue position |
| 📍 Live Train Tracking | Real-time train location, delay & next station ETA |
| 🔌 ACS/BAP Bridge | VXML event translator — stub ready for M3 integration |
| 🖥️ Web IVR Simulator | Interactive dark-themed UI with dialpad & JSON viewer |
| 📋 Session Management | Full call history & booking slot tracking per session |

---

## 🚀 How to Run

### Prerequisites
```
Python 3.10 or above
```

### Install Dependencies
```bash
pip install fastapi uvicorn requests
```

### Start the Server
```bash
python irctc_backend.py
```

### Open in Browser
```
http://localhost:8000
```

### API Documentation (Swagger UI)
```
http://localhost:8000/docs
```

---

## 🎮 How to Use the Web Simulator

```
Step 1 → Click "START CALL"
         Welcome prompt plays, Session ID is created

Step 2 → Press "1" on dialpad
         Routes to PNR Status flow

Step 3 → Click "PNR STATUS" card
         Returns: Train, Coach B4, Berth 32, Platform 1

Step 4 → Press "2" on dialpad → select class → quota → berth
         Click "SMART BOOKING" card
         Returns: Booking ID, Estimated Fare, Payment Link

Step 5 → Press "3" on dialpad
         Click "TATKAL EMERGENCY" card
         Returns: Ref ID, Surcharge, Urgency Score, Queue Position

Step 6 → Press "4" on dialpad
         Click "LIVE TRACKING" card
         Returns: Current Station, Next Station, Delay, ETA

Step 7 → Click "END CALL"
```

---

## 📁 Project Structure

```
IRCTC_IVR/
├── irctc_backend.py    → FastAPI server (Integration Layer)
└── irctc_ui.html       → Web IVR Simulator UI
```

---

## 🔌 ACS/BAP Integration (Milestone 3 Roadmap)

The `/acs/bridge` endpoint is currently a **stub** that shows exactly what payload would be sent to ACS/BAP. In Milestone 3, this will be replaced with:

```python
from azure.communication.callautomation import (
    CallAutomationClient, TextSource, RecognizeInputType
)
client = CallAutomationClient.from_connection_string(ACS_CONN_STR)
conn = client.get_call_connection(acs_call_connection_id)
conn.start_recognizing_media(
    input_type=RecognizeInputType.DTMF,
    play_prompt=TextSource(text=tts_text, voice_name="en-IN-NeerjaNeural"),
    max_tones_to_collect=1,
    operation_context="irctc_main_menu"
)
```

---

## 🛣️ Milestone Roadmap

| Milestone | Status | Description |
|---|---|---|
| M1 | ✅ Done | Legacy system analysis & requirements |
| M2 | ✅ Done | Integration layer (this project) |
| M3 | 🔄 Upcoming | Conversational AI flows via ACS/BAP |
| M4 | 🔄 Upcoming | Testing, deployment & monitoring |

---

## 🧰 Tech Stack

- **FastAPI** — REST API framework
- **Uvicorn** — ASGI server
- **Pydantic** — Request/response validation
- **HTML + CSS + JS** — Web IVR Simulator UI
- **Azure ACS** — (Milestone 3 integration target)
- **BAP** — Bot Activity Protocol (Milestone 3)

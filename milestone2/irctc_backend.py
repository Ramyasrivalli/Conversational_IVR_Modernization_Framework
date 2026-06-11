"""
IRCTC Conversational IVR Modernization Framework
Milestone 2 — FastAPI Integration Layer

Author  : M. Ramya Srivalli
Batch   : Infosys Internship, Batch 13, Group-2
Year    : 2026

Run:
    python irctc_backend.py
    → Server starts at http://localhost:8000
    → Swagger docs at http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone, timedelta
import uuid
import uvicorn
import os

# ── App Setup ─────────────────────────────────────────────────────────────────

app = FastAPI(
    title="IRCTC IVR Integration Layer",
    description="AI-Enabled Conversational IVR — Milestone 2",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve irctc_ui.html at root
@app.get("/", response_class=HTMLResponse)
def root():
    html_path = os.path.join(os.path.dirname(__file__), "irctc_ui.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h2>IRCTC IVR Backend running. Open irctc_ui.html in your browser.</h2>")

# ── IST Timezone Helper ────────────────────────────────────────────────────────

IST = timezone(timedelta(hours=5, minutes=30))

def ist_now() -> datetime:
    return datetime.now(IST)

def ist_greeting() -> tuple[str, str]:
    """Return (greeting_text, greeting_type) based on IST hour."""
    hour = ist_now().hour
    if 5 <= hour < 12:
        return "Suprabhat! Good Morning!", "morning"
    elif 12 <= hour < 17:
        return "Namaskar! Good Afternoon!", "afternoon"
    elif 17 <= hour < 21:
        return "Shubh Sandhya! Good Evening!", "evening"
    else:
        return "Shubh Ratri! Good Night!", "night"

def ist_str() -> str:
    return ist_now().isoformat()

# ── In-Memory Session Store ────────────────────────────────────────────────────

sessions: dict = {}

# ── Mock Data ─────────────────────────────────────────────────────────────────

PNR_DATABASE = {
    "1234567890": {
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
    },
    "9876543210": {
        "status": "RAC 12",
        "train_number": "12630",
        "train_name": "Yeshwantpur Express",
        "from_station": "YPR",
        "to_station": "HWH",
        "departure": "21:30",
        "arrival": "06:15+2",
        "coach": "A2",
        "berth_number": "15",
        "berth_type": "Side Lower",
        "platform": "1",
    },
    "5555555555": {
        "status": "WL 89",
        "train_number": "12483",
        "train_name": "Amritsar Express",
        "from_station": "NDLS",
        "to_station": "ASR",
        "departure": "09:30",
        "arrival": "19:20",
        "coach": "—",
        "berth_number": "—",
        "berth_type": "—",
        "platform": "TBD",
    },
    "4444444444": {
        "status": "CONFIRMED",
        "train_number": "22119",
        "train_name": "Mumbai CSMT AC Express",
        "from_station": "LKO",
        "to_station": "CSMT",
        "departure": "14:05",
        "arrival": "09:30+1",
        "coach": "H1",
        "berth_number": "05",
        "berth_type": "Upper",
        "platform": "5",
    },
}

TRAIN_DATABASE = {
    "12951": {
        "name": "Mumbai Rajdhani Express",
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
    },
    "12301": {
        "name": "Howrah Rajdhani Express",
        "current_station": "Mughal Sarai Junction",
        "current_station_code": "MGS",
        "next_station": "Allahabad Junction",
        "next_station_code": "ALD",
        "scheduled_departure": "13:45",
        "actual_departure": "13:45",
        "delay_minutes": 0,
        "delay_reason": None,
        "eta_destination": "07:55+1",
        "on_time_reliability": 91,
    },
    "12630": {
        "name": "Yeshwantpur Express",
        "current_station": "Wadi Junction",
        "current_station_code": "WADI",
        "next_station": "Gulbarga",
        "next_station_code": "GR",
        "scheduled_departure": "08:30",
        "actual_departure": "08:42",
        "delay_minutes": 12,
        "delay_reason": "Late engine attachment at Yelahanka",
        "eta_destination": "06:15+2",
        "on_time_reliability": 78,
    },
    "22119": {
        "name": "Mumbai CSMT AC Express",
        "current_station": "Bhopal Junction",
        "current_station_code": "BPL",
        "next_station": "Itarsi Junction",
        "next_station_code": "ET",
        "scheduled_departure": "00:15",
        "actual_departure": "00:20",
        "delay_minutes": 5,
        "delay_reason": "Crew change delay",
        "eta_destination": "09:35+1",
        "on_time_reliability": 88,
    },
    "12002": {
        "name": "Bhopal Shatabdi Express",
        "current_station": "Gwalior Junction",
        "current_station_code": "GWL",
        "next_station": "Jhansi Junction",
        "next_station_code": "JHS",
        "scheduled_departure": "11:55",
        "actual_departure": "11:55",
        "delay_minutes": 0,
        "delay_reason": None,
        "eta_destination": "14:05",
        "on_time_reliability": 97,
    },
}

FARE_TABLE = {
    ("NDLS", "BCT"): {"SL": 735, "3A": 1985, "2A": 2865, "1A": 4785, "CC": None},
    ("NDLS", "SBC"): {"SL": 1205, "3A": 2785, "2A": 4025, "1A": 6675, "CC": None},
    ("NDLS", "MAS"): {"SL": 1265, "3A": 3005, "2A": 4345, "1A": 7225, "CC": None},
    ("BCT", "SBC"): {"SL": 580, "3A": 1430, "2A": 2050, "1A": None, "CC": None},
    ("SBC", "MAS"): {"SL": 300, "3A": 880, "2A": 1295, "1A": 2145, "CC": 660},
}

TATKAL_SURCHARGE = {"SL": 150, "3A": 400, "2A": 600, "1A": 900, "CC": 125}

# ── Request / Response Models ──────────────────────────────────────────────────

class StartRequest(BaseModel):
    caller_id: str = "+91-9999999999"
    language: str = "en"

class InputRequest(BaseModel):
    session_id: str
    digit: str
    current_flow: str = "main_menu"

class PNRRequest(BaseModel):
    session_id: str
    pnr_number: str

class BookingRequest(BaseModel):
    session_id: str
    train_number: str
    from_station: str
    to_station: str
    travel_class: str = "SL"
    quota: str = "GN"
    berth_preference: str = "no_preference"

class TatkalRequest(BaseModel):
    session_id: str
    train_number: str
    from_station: str
    to_station: str
    travel_class: str = "SL"

class TrackingRequest(BaseModel):
    session_id: str
    train_number: str

class ACSBridgeRequest(BaseModel):
    session_id: str
    acs_call_connection_id: str = ""
    vxml_event: str = "speech_recognized"
    tts_text: Optional[str] = None
    speech_transcript: Optional[str] = None

# ── Helper ─────────────────────────────────────────────────────────────────────

def get_session(session_id: str) -> dict:
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found. Call POST /ivr/start first.")
    return sessions[session_id]

def log_action(session_id: str, action: str, inp=None):
    if session_id in sessions:
        sessions[session_id]["history"].append({
            "timestamp": ist_now().strftime("%H:%M:%S"),
            "action": action,
            "input": inp,
        })
        sessions[session_id]["last_activity"] = ist_str()

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.post("/ivr/start", summary="Start IVR Session")
def ivr_start(req: StartRequest):
    session_id = str(uuid.uuid4())
    greeting, greeting_type = ist_greeting()
    welcome = (
        f"{greeting} Welcome to IRCTC 139. "
        "Press 1 for PNR Status, Press 2 for Ticket Booking, "
        "Press 3 for Tatkal, Press 4 for Train Tracking, "
        "Press 5 for Cancellation, Press 9 for Agent."
    )
    sessions[session_id] = {
        "session_id": session_id,
        "caller_id": req.caller_id,
        "language": req.language,
        "current_flow": "main_menu",
        "history": [{"timestamp": ist_now().strftime("%H:%M:%S"), "action": "session_start", "input": None}],
        "created_at": ist_str(),
        "last_activity": ist_str(),
    }
    return {
        "session_id": session_id,
        "message": welcome,
        "options": ["1", "2", "3", "4", "5", "9"],
        "language": req.language,
        "timestamp": ist_str(),
        "greeting_type": greeting_type,
    }


@app.post("/ivr/input", summary="Handle DTMF Key Press")
def ivr_input(req: InputRequest):
    session = get_session(req.session_id)
    log_action(req.session_id, "dtmf_input", req.digit)

    routing = {
        "1": ("pnr_status",   "Please enter your 10-digit PNR number followed by hash.", "collect_pnr"),
        "2": ("booking",      "Please say or enter: train number, from station, to station, travel class.", "collect_booking_details"),
        "3": ("tatkal",       "Tatkal booking. Please provide train number, from and to station.", "collect_tatkal_details"),
        "4": ("tracking",     "Please enter the 5-digit train number to track.", "collect_train_number"),
        "5": ("cancellation", "Please enter the PNR number you wish to cancel.", "collect_cancel_pnr"),
        "9": ("agent",        "Transferring you to an IRCTC support agent. Please hold.", "transfer"),
        "0": ("main_menu",    "Returning to main menu. Press 1 for PNR, 2 for Booking, 3 for Tatkal, 4 for Tracking, 5 for Cancellation, 9 for Agent.", "main_menu"),
        "*": ("main_menu",    "Returning to main menu.", "main_menu"),
    }

    if req.digit in routing:
        flow, message, next_action = routing[req.digit]
        sessions[req.session_id]["current_flow"] = flow
        return {
            "session_id": req.session_id,
            "flow": flow,
            "message": message,
            "next_action": next_action,
            "valid": True,
        }
    else:
        return {
            "session_id": req.session_id,
            "flow": session["current_flow"],
            "message": f"Invalid input '{req.digit}'. Press 1 for PNR, 2 for Booking, 3 for Tatkal, 4 for Tracking, 9 for Agent.",
            "next_action": "re_prompt",
            "valid": False,
        }


@app.post("/ivr/pnr", summary="PNR Status Check")
def ivr_pnr(req: PNRRequest):
    session = get_session(req.session_id)
    log_action(req.session_id, "pnr_lookup", req.pnr_number)

    pnr = req.pnr_number.strip()
    if not pnr.isdigit() or len(pnr) != 10:
        raise HTTPException(status_code=400, detail="PNR must be exactly 10 digits.")

    if pnr not in PNR_DATABASE:
        return {
            "session_id": req.session_id,
            "pnr": pnr,
            "status": "NOT_FOUND",
            "message": f"PNR {pnr} not found in the system. Please verify the number and try again.",
            "tts_text": f"PNR {' '.join(pnr)} was not found. Please check the number and try again.",
        }

    d = PNR_DATABASE[pnr]
    status = d["status"]
    is_confirmed = status == "CONFIRMED"

    message = (
        f"PNR {pnr} — Status: {status}. "
        f"Train {d['train_number']} {d['train_name']}. "
    )
    tts = f"Your PNR status is {status}. Train {d['train_name']}. "

    if is_confirmed or status.startswith("RAC"):
        message += f"Coach {d['coach']}, Berth {d['berth_number']} {d['berth_type']}. Platform {d['platform']}. Departs at {d['departure']}."
        tts += f"Coach {d['coach']}, Berth {d['berth_number']} {d['berth_type']}. Platform {d['platform']}. Departure at {d['departure']}."
    else:
        message += f"Waitlisted. Please check closer to departure for confirmation."
        tts += "You are on the waiting list. Please check closer to the travel date."

    return {
        "session_id": req.session_id,
        "pnr": pnr,
        **d,
        "message": message,
        "tts_text": tts,
    }


@app.post("/ivr/booking", summary="Ticket Booking")
def ivr_booking(req: BookingRequest):
    session = get_session(req.session_id)
    log_action(req.session_id, "booking", f"{req.from_station}→{req.to_station} {req.travel_class}")

    booking_id = f"BK-2026-{req.from_station}-{req.to_station}-{abs(hash(req.session_id)) % 9000 + 1000}"

    key = (req.from_station.upper(), req.to_station.upper())
    fare = FARE_TABLE.get(key, {}).get(req.travel_class.upper(), 999)
    if fare is None:
        fare = 999

    class_names = {"SL": "Sleeper", "3A": "3rd AC", "2A": "2nd AC", "1A": "1st AC", "CC": "Chair Car"}
    quota_names = {"GN": "General", "TQ": "Tatkal", "LD": "Ladies", "HP": "Handicapped", "FT": "Foreign Tourist"}
    cls_name = class_names.get(req.travel_class.upper(), req.travel_class)
    quota_name = quota_names.get(req.quota.upper(), req.quota)

    train = TRAIN_DATABASE.get(req.train_number, {})
    train_name = train.get("name", f"Train {req.train_number}")

    valid_until = ist_now() + timedelta(minutes=15)

    return {
        "session_id": req.session_id,
        "booking_id": booking_id,
        "train": f"{req.train_number} {train_name}",
        "from": req.from_station,
        "to": req.to_station,
        "class": f"{req.travel_class} — {cls_name}",
        "quota": f"{req.quota} — {quota_name}",
        "berth_preference": req.berth_preference,
        "fare": fare,
        "availability": "AVAILABLE — 43 seats",
        "payment_link": f"https://pay.irctc.co.in/{booking_id}",
        "valid_until": valid_until.isoformat(),
        "message": f"Booking initiated. Train {req.train_number} from {req.from_station} to {req.to_station}. {cls_name} class, ₹{fare}. Pay within 15 minutes.",
        "tts_text": f"Booking ready. Train {req.train_number} {train_name}. {cls_name} class. Fare {fare} rupees. Complete payment within 15 minutes.",
    }


@app.post("/ivr/tatkal", summary="Tatkal Booking")
def ivr_tatkal(req: TatkalRequest):
    session = get_session(req.session_id)
    log_action(req.session_id, "tatkal_booking", f"{req.from_station}→{req.to_station}")

    now = ist_now()
    window_open = (10 <= now.hour < 23)

    if not window_open:
        next_open = now.replace(hour=10, minute=0, second=0, microsecond=0)
        if now.hour >= 23:
            next_open += timedelta(days=1)
        return {
            "session_id": req.session_id,
            "window_open": False,
            "message": f"Tatkal booking is not available right now. Window opens at 10:00 AM IST. Next opening: {next_open.strftime('%d %b %Y at 10:00 AM IST')}.",
            "tts_text": "Tatkal booking window is currently closed. It opens at 10 AM every day.",
        }

    tatkal_ref = f"TK-2026-{abs(hash(req.session_id)) % 9000 + 1000}-{req.from_station}"
    base_fare_map = {"SL": 735, "3A": 1985, "2A": 2865, "1A": 4785, "CC": 500}
    base_fare = base_fare_map.get(req.travel_class.upper(), 999)
    surcharge = TATKAL_SURCHARGE.get(req.travel_class.upper(), 200)
    total = base_fare + surcharge
    urgency = min(99, 60 + (now.hour - 10) * 4)
    queue_pos = max(1, 15 - (now.hour - 10) * 2)

    window_close = now.replace(hour=23, minute=0, second=0, microsecond=0)

    return {
        "session_id": req.session_id,
        "tatkal_ref": tatkal_ref,
        "status": f"QUEUE_POSITION_{queue_pos}",
        "fare": base_fare,
        "tatkal_surcharge": surcharge,
        "total_fare": total,
        "urgency_score": urgency,
        "window_open": True,
        "window_closes": window_close.isoformat(),
        "message": f"Tatkal booking queued. Position {queue_pos}. {req.travel_class} class. Fare ₹{total} (including ₹{surcharge} surcharge). Window closes at 11 PM.",
        "tts_text": f"Tatkal booking initiated. Queue position {queue_pos}. Total fare {total} rupees including Tatkal surcharge. Complete payment to confirm.",
    }


@app.post("/ivr/tracking", summary="Live Train Tracking")
def ivr_tracking(req: TrackingRequest):
    session = get_session(req.session_id)
    log_action(req.session_id, "train_tracking", req.train_number)

    train_num = req.train_number.strip()
    if train_num not in TRAIN_DATABASE:
        return {
            "session_id": req.session_id,
            "train_number": train_num,
            "status": "NOT_FOUND",
            "message": f"Train {train_num} not found. Please check the number and try again.",
            "tts_text": f"Train number {' '.join(train_num)} was not found.",
        }

    t = TRAIN_DATABASE[train_num]
    delay_msg = f" Delayed by {t['delay_minutes']} minutes" if t["delay_minutes"] > 0 else " Running on time"
    delay_reason_msg = f" due to {t['delay_reason']}" if t.get("delay_reason") else ""

    return {
        "session_id": req.session_id,
        "train_number": train_num,
        **t,
        "message": f"Train {train_num} is at {t['current_station']}.{delay_msg}{delay_reason_msg}. Next station: {t['next_station']}. ETA destination: {t['eta_destination']}.",
        "tts_text": f"Train {train_num} {t['name']} is currently at {t['current_station']}.{delay_msg}. Expected arrival at {t['eta_destination']}.",
    }


@app.post("/acs/bridge", summary="ACS/BAP Integration Stub")
def acs_bridge(req: ACSBridgeRequest):
    session = get_session(req.session_id)
    log_action(req.session_id, "acs_bridge", req.vxml_event)

    intent = "unknown"
    entities = {}
    confidence = 0.5
    dialogue_state = "idle"

    transcript = (req.speech_transcript or "").lower()
    if any(w in transcript for w in ["pnr", "status", "ticket", "confirm"]):
        intent = "pnr_status"
        confidence = 0.92
        dialogue_state = "pnr_lookup"
        digits = "".join(filter(str.isdigit, transcript))
        if len(digits) == 10:
            entities["pnr"] = digits
    elif any(w in transcript for w in ["book", "ticket", "reserve"]):
        intent = "book_ticket"
        confidence = 0.88
        dialogue_state = "collect_booking_details"
    elif any(w in transcript for w in ["track", "where", "location", "running"]):
        intent = "train_tracking"
        confidence = 0.91
        dialogue_state = "tracking"
    elif any(w in transcript for w in ["tatkal", "urgent", "emergency"]):
        intent = "tatkal_booking"
        confidence = 0.94
        dialogue_state = "tatkal_flow"

    return {
        "acs_action": "play_tts",
        "tts_text": req.tts_text or "How can I help you?",
        "voice": "en-IN-NeerjaNeural",
        "next_event": "collect_input",
        "session_id": req.session_id,
        "bap_payload": {
            "intent": intent,
            "entities": entities,
            "confidence": confidence,
            "dialogue_state": dialogue_state,
        },
    }


@app.get("/session/{session_id}", summary="Get Session State")
def get_session_state(session_id: str):
    session = get_session(session_id)
    return session


@app.get("/health", summary="Health Check")
def health():
    return {
        "status": "healthy",
        "service": "IRCTC IVR Backend",
        "version": "2.0.0",
        "timestamp": ist_str(),
        "endpoints_active": 8,
        "sessions_active": len(sessions),
    }


# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("✅ IRCTC IVR Backend running on http://localhost:8000")
    print("📖 Swagger API docs at  http://localhost:8000/docs")
    print("🖥️  DTMF Simulator at   http://localhost:8000")
    uvicorn.run("irctc_backend:app", host="0.0.0.0", port=8000, reload=True)

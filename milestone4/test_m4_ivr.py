"""
=============================================================================
PROJECT   : Conversational IVR Modernization Framework
MODULE    : Module 4 — Testing & Deployment
MILESTONE : Milestone 4 | IRCTC Smart IVR System
AUTHOR    : M. Ramya Srivalli | Infosys Intern | Batch 13, Group-2
=============================================================================

WHAT THIS FILE COVERS
---------------------
  1. Unit Tests           → Test individual endpoints in isolation (<100ms)
  2. Integration Tests    → Test API + session memory together (~1–5s)
  3. End-to-End Tests     → Simulate full IVR call flow (~10–30s)
  4. Performance Tests    → Load test with concurrent requests
  5. Error Handling Tests → Verify graceful failure responses

HOW TO RUN
----------
  Install dependencies:
      pip install fastapi uvicorn pytest httpx requests

  Run all tests:
      pytest test_m4_ivr.py -v

  Run one section only:
      pytest test_m4_ivr.py::TestUnitTests -v
      pytest test_m4_ivr.py::TestIntegrationTests -v
      pytest test_m4_ivr.py::TestE2ETests -v
      pytest test_m4_ivr.py::TestErrorHandling -v

  Run load test directly (needs server running):
      python test_m4_ivr.py

NOTES
-----
  - Unit tests mock all external calls → stay under 100ms
  - Integration tests use real in-memory session store
  - E2E tests simulate a real user call journey step by step
  - Load test needs your actual deployed URL in IVR_URL variable
=============================================================================
"""

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

import time
import requests
import pytest
from unittest.mock import patch, MagicMock

# ✅ FIXED: correct import path — was 'fastapi.testclients' (wrong)
from fastapi.testclient import TestClient

# Import your FastAPI app from irctc_backend.py
# Make sure irctc_backend.py is in the same folder
from irctc_backend import app

# ─────────────────────────────────────────────────────────────────────────────
# SHARED TEST CLIENT
# ─────────────────────────────────────────────────────────────────────────────

# ✅ FIXED: TestClient must always receive the app instance
# Original code had: client = TestClient()  ← raises TypeError
client = TestClient(app)


# =============================================================================
# SECTION 1 — UNIT TESTS
# =============================================================================
# What  : Test each endpoint individually, in complete isolation
# Speed : Each test must complete in under 100ms
# Rule  : No real HTTP calls, no real DB calls — mock everything external
#
# Key concept: Ask yourself — what is the CONTRACT of this endpoint?
# For /ivr/pnr: give me a 10-digit PNR → return train, coach, berth, status
# Your test should verify exactly that contract, and nothing more.
# =============================================================================

class TestUnitTests:

    def test_health_check(self):
        """
        GET /health should return 200 and confirm the server is running.
        This is the first test — if this fails, nothing else will work.
        """
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data

    def test_root_serves_frontend(self):
        """
        GET / should serve the irctc_ui.html simulator frontend.
        The response must be HTML, not JSON.
        """
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_ivr_start_creates_session(self):
        """
        POST /ivr/start should:
          - Return HTTP 200
          - Create a session with a unique session_id
          - Return a welcome prompt mentioning IRCTC
          - Return the main menu options (keys 1–5, 9, 0)
        """
        payload = {"caller_id": "TestCaller_001", "language": "EN"}
        response = client.post("/ivr/start", json=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert "prompt" in data
        assert "session_id" in data["data"]
        assert "menu" in data["data"]
        assert "IRCTC" in data["prompt"] or "Welcome" in data["prompt"]
        # Main menu must have at least PNR (1) and Booking (2)
        assert "1" in data["data"]["menu"]
        assert "2" in data["data"]["menu"]

    def test_ivr_start_optional_language_defaults_to_en(self):
        """
        POST /ivr/start without language field should work fine.
        language: Optional[str] = "EN" in the Pydantic model.
        """
        response = client.post("/ivr/start", json={"caller_id": "TestCaller_002"})
        assert response.status_code == 200

    def test_pnr_check_valid_10_digit(self):
        """
        POST /ivr/pnr with a valid 10-digit PNR must return:
          - status: success
          - pnr_details with pnr, status, coach, berth fields
        """
        start = client.post("/ivr/start", json={"caller_id": "PNR_Valid"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/ivr/pnr", json={
            "session_id": sid, "pnr_number": "1234567890"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        pnr = data["data"]["pnr_details"]
        assert pnr["pnr"] == "1234567890"
        assert "status" in pnr
        assert "coach" in pnr
        assert "berth" in pnr

    def test_pnr_check_too_short_is_invalid(self):
        """
        POST /ivr/pnr with fewer than 10 digits must return status "invalid".
        The system must NOT crash or return 500.
        """
        start = client.post("/ivr/start", json={"caller_id": "PNR_Short"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/ivr/pnr", json={
            "session_id": sid, "pnr_number": "12345"  # Only 5 digits
        })
        assert response.status_code == 200
        assert response.json()["status"] == "invalid"

    def test_pnr_check_letters_is_invalid(self):
        """
        POST /ivr/pnr with non-numeric characters must return status "invalid".
        """
        start = client.post("/ivr/start", json={"caller_id": "PNR_Letters"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/ivr/pnr", json={
            "session_id": sid, "pnr_number": "ABCDE12345"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "invalid"

    def test_booking_returns_booking_id_and_fare(self):
        """
        POST /ivr/booking with all required fields must return:
          - a booking_id
          - an estimated fare
          - a payment link
          - status: PENDING_PAYMENT
        """
        start = client.post("/ivr/start", json={"caller_id": "Booking_Test"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/ivr/booking", json={
            "session_id": sid,
            "train_number": "12951",
            "journey_date": "15-Apr-2026",
            "from_station": "NDLS",
            "to_station": "MMCT",
            "travel_class": "1",       # 1 = Sleeper
            "quota": "1",              # 1 = General
            "berth_preference": "1",   # 1 = Lower
            "passenger_count": 1
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        booking = data["data"]["booking"]
        assert "booking_id" in booking
        assert "fare" in booking
        assert "pay_link" in booking
        assert booking["status"] == "PENDING_PAYMENT"

    def test_tatkal_returns_ref_and_surcharge(self):
        """
        POST /ivr/tatkal must return either:
          - success (with ref, surcharge, urgency_score, queue_position)
          - OR unavailable (if outside the 10AM–11PM IST window)
        Both outcomes are valid — test accepts either.
        """
        start = client.post("/ivr/start", json={"caller_id": "Tatkal_Test"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/ivr/tatkal", json={
            "session_id": sid,
            "train_number": "12951",
            "journey_date": "15-Apr-2026",
            "from_station": "NDLS",
            "to_station": "MMCT",
            "travel_class": "1",
            "passenger_count": 1
        })
        assert response.status_code == 200
        assert response.json()["status"] in ["success", "unavailable"]

    def test_tracking_returns_station_and_delay(self):
        """
        POST /ivr/tracking with a valid 5-digit train number must return:
          - current_station, next_station, delay_minutes, eta_next_station
        """
        start = client.post("/ivr/start", json={"caller_id": "Track_Test"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/ivr/tracking", json={
            "session_id": sid, "train_number": "12951"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        track = data["data"]["tracking"]
        assert "current_station" in track
        assert "next_station" in track
        assert "delay_minutes" in track
        assert "eta_next_station" in track

    def test_tracking_invalid_train_number(self):
        """
        POST /ivr/tracking with a train number that is NOT 5 digits
        must return status "invalid", not a crash.
        """
        start = client.post("/ivr/start", json={"caller_id": "Track_Invalid"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/ivr/tracking", json={
            "session_id": sid, "train_number": "123"  # Only 3 digits
        })
        assert response.status_code == 200
        assert response.json()["status"] == "invalid"

    @patch("requests.get")
    def test_mock_external_api_call(self, mock_get):
        """
        Demonstrates mocking an external API so the unit test never
        hits the real internet and stays under 100ms.

        unittest.mock.patch replaces requests.get with a fake object
        that returns a predictable, controlled result.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "pnr": "1234567890", "status": "CONFIRMED"
        }
        mock_get.return_value = mock_response

        result = requests.get("https://api.irctc.co.in/pnr/1234567890")
        assert result.status_code == 200
        assert result.json()["status"] == "CONFIRMED"
        mock_get.assert_called_once()


# =============================================================================
# SECTION 2 — INTEGRATION TESTS
# =============================================================================
# What  : Test that API endpoints correctly interact with session memory
# Speed : ~1–5 seconds (allows real session read/write)
# Rule  : Do NOT mock the session store — let it run for real
#
# Key concept: Integration tests catch problems that unit tests cannot.
# If session memory is broken, multi-step flows fail here.
# Example: User says "Book a flight" in step 2 — but in step 3 when they
# say "Delhi", the system needs context from step 2. Without session, it fails.
# =============================================================================

class TestIntegrationTests:

    def test_session_created_and_readable(self):
        """
        After POST /ivr/start, the session must be readable
        via GET /session/{session_id}.
        This verifies the session store is actually storing data.
        """
        start = client.post("/ivr/start", json={"caller_id": "Integ_001"})
        sid = start.json()["data"]["session_id"]

        session_resp = client.get(f"/session/{sid}")
        assert session_resp.status_code == 200
        session_data = session_resp.json()["data"]
        assert session_data["session_id"] == sid
        assert session_data["caller_id"] == "Integ_001"

    def test_dtmf_1_routes_to_pnr_flow(self):
        """
        Pressing DTMF "1" on the main menu should route to PNR flow.
        The prompt must ask for a PNR number.
        This verifies /ivr/input reads AND updates session correctly.
        """
        start = client.post("/ivr/start", json={"caller_id": "Integ_002"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "main_menu"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert "PNR" in response.json()["prompt"]

    def test_dtmf_2_then_class_selection(self):
        """
        Multi-step DTMF test:
          Step 1: Press "2" → booking flow
          Step 2: Press "1" → select Sleeper class → ask for quota

        Each step depends on the previous session state being preserved.
        If session write fails after step 1, step 2 will not route correctly.
        """
        start = client.post("/ivr/start", json={"caller_id": "Integ_003"})
        sid = start.json()["data"]["session_id"]

        step1 = client.post("/ivr/input", json={
            "session_id": sid, "digit": "2", "current_flow": "main_menu"
        })
        assert step1.status_code == 200
        assert step1.json()["status"] == "success"

        step2 = client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "select_class"
        })
        assert step2.status_code == 200
        prompt = step2.json()["prompt"].lower()
        # After class selection, must ask for quota
        assert "quota" in prompt or "sleeper" in prompt

    def test_invalid_dtmf_reprompts_user(self):
        """
        Pressing an invalid DTMF key on the main menu should:
          - NOT crash the server
          - Return status "invalid"
          - Re-list valid options so the caller knows what to do
        """
        start = client.post("/ivr/start", json={"caller_id": "Integ_004"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/ivr/input", json={
            "session_id": sid, "digit": "8",  # Not in main menu
            "current_flow": "main_menu"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "invalid"
        # Must include valid options in the reprompt
        assert "1" in response.json()["prompt"]

    def test_session_history_logs_each_step(self):
        """
        After multiple interactions, the session history should
        record each event. This verifies that logging is working.
        """
        start = client.post("/ivr/start", json={"caller_id": "Integ_005"})
        sid = start.json()["data"]["session_id"]

        # Do two interactions
        client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "main_menu"
        })
        client.post("/ivr/pnr", json={
            "session_id": sid, "pnr_number": "1234567890"
        })

        session_resp = client.get(f"/session/{sid}")
        history = session_resp.json()["data"]["history"]
        # Must have at least: call_started, dtmf input, pnr_check
        assert len(history) >= 2

    def test_acs_bridge_returns_correct_payload_structure(self):
        """
        POST /acs/bridge (stub) must return the correct ACS SDK payload
        structure that will be used in production to control the call.
        Verifies the bridge knows: platform, voice, call_connection_id.
        """
        start = client.post("/ivr/start", json={"caller_id": "ACS_Integ"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/acs/bridge", json={
            "session_id": sid,
            "acs_call_connection_id": "ACS_CONN_INTEG_001",
            "vxml_event": "filled",
            "tts_text": "Welcome to IRCTC. Press 1 for PNR.",
            "collect_digits": True,
            "max_digits": 1
        })
        assert response.status_code == 200
        bridge = response.json()["data"]["bridge_payload"]
        assert bridge["platform"] == "ACS"
        assert bridge["voice"] == "en-IN-NeerjaNeural"
        assert bridge["acs_call_connection_id"] == "ACS_CONN_INTEG_001"
        assert bridge["collect_digits"] is True

    def test_invalid_session_returns_404(self):
        """
        Any endpoint receiving a session_id that does not exist must
        return HTTP 404 — not 200, not 500.
        """
        fake_sid = "00000000-0000-0000-0000-000000000000"
        response = client.post("/ivr/pnr", json={
            "session_id": fake_sid, "pnr_number": "1234567890"
        })
        assert response.status_code == 404


# =============================================================================
# SECTION 3 — END-TO-END (E2E) TESTS
# =============================================================================
# What  : Simulate complete real-user IVR call journeys
# Speed : ~10–30 seconds (full flow, no shortcuts)
# Rule  : Test USER STORIES, not functions
#
# Story: "As a caller, I press 1, enter my PNR,
#         and expect to hear my booking status."
#
# Key difference from integration tests:
#   Integration test → are two components talking correctly?
#   E2E test         → does the ENTIRE call flow work end to end?
# =============================================================================

class TestE2ETests:

    def test_complete_pnr_check_journey(self):
        """
        Full user story: Check PNR status
          Start call → Press 1 → Submit PNR → Receive status
        """
        # Step 1: Start the call
        start = client.post("/ivr/start", json={"caller_id": "E2E_PNR_001"})
        assert start.status_code == 200
        sid = start.json()["data"]["session_id"]
        assert "IRCTC" in start.json()["prompt"] or "Welcome" in start.json()["prompt"]

        # Step 2: Press "1" — route to PNR flow
        key1 = client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "main_menu"
        })
        assert key1.status_code == 200
        assert "PNR" in key1.json()["prompt"]

        # Step 3: Submit PNR number
        pnr = client.post("/ivr/pnr", json={
            "session_id": sid, "pnr_number": "1234567890"
        })
        assert pnr.status_code == 200
        assert pnr.json()["status"] == "success"
        # Result must mention CONFIRMED status or coach details
        assert "CONFIRMED" in pnr.json()["prompt"] or "B4" in pnr.json()["prompt"]

        print("✅ E2E PNR Check journey: PASSED")

    def test_complete_booking_journey(self):
        """
        Full user story: Book a ticket
          Start → Press 2 → Class=1 (Sleeper) → Quota=1 (General) →
          Berth=1 (Lower) → Submit booking → Get booking_id
        """
        start = client.post("/ivr/start", json={"caller_id": "E2E_Book_001"})
        sid = start.json()["data"]["session_id"]

        # Press 2 → booking flow
        r = client.post("/ivr/input", json={
            "session_id": sid, "digit": "2", "current_flow": "main_menu"
        })
        assert r.status_code == 200

        # Class = 1 (Sleeper)
        r = client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "select_class"
        })
        assert r.status_code == 200
        assert "Sleeper" in r.json()["prompt"] or "quota" in r.json()["prompt"].lower()

        # Quota = 1 (General)
        r = client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "select_quota"
        })
        assert r.status_code == 200
        assert "General" in r.json()["prompt"] or "berth" in r.json()["prompt"].lower()

        # Berth = 1 (Lower)
        r = client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "select_berth"
        })
        assert r.status_code == 200

        # Confirm booking
        booking = client.post("/ivr/booking", json={
            "session_id": sid,
            "train_number": "12951",
            "journey_date": "15-Apr-2026",
            "from_station": "NDLS",
            "to_station": "MMCT",
            "travel_class": "1",
            "quota": "1",
            "berth_preference": "1",
            "passenger_count": 1
        })
        assert booking.status_code == 200
        assert booking.json()["status"] == "success"
        assert "booking_id" in booking.json()["data"]["booking"]
        assert "fare" in booking.json()["data"]["booking"]

        print("✅ E2E Booking journey: PASSED")

    def test_complete_tracking_journey(self):
        """
        Full user story: Track a train
          Start → Press 4 → Submit train number → Get live status
        """
        start = client.post("/ivr/start", json={"caller_id": "E2E_Track_001"})
        sid = start.json()["data"]["session_id"]

        # Press 4 → tracking flow
        client.post("/ivr/input", json={
            "session_id": sid, "digit": "4", "current_flow": "main_menu"
        })

        # Submit train number
        tracking = client.post("/ivr/tracking", json={
            "session_id": sid, "train_number": "12951"
        })
        assert tracking.status_code == 200
        assert tracking.json()["status"] == "success"
        track = tracking.json()["data"]["tracking"]
        assert "current_station" in track
        assert "next_station" in track

        print("✅ E2E Tracking journey: PASSED")

    def test_invalid_key_then_valid_key_still_works(self):
        """
        Edge case: Caller presses wrong key, then correct key.
        The session must remain active — the call should NOT drop.
        """
        start = client.post("/ivr/start", json={"caller_id": "E2E_Edge_001"})
        sid = start.json()["data"]["session_id"]

        # Press invalid key "8"
        invalid = client.post("/ivr/input", json={
            "session_id": sid, "digit": "8", "current_flow": "main_menu"
        })
        assert invalid.status_code == 200
        assert invalid.json()["status"] == "invalid"

        # Session still alive — press valid key "1"
        valid = client.post("/ivr/input", json={
            "session_id": sid, "digit": "1", "current_flow": "main_menu"
        })
        assert valid.status_code == 200
        assert valid.json()["status"] == "success"

        print("✅ E2E Edge case (invalid then valid key): PASSED")

    def test_agent_transfer_journey(self):
        """
        Full user story: Caller needs human agent
          Start → Press 9 → Get transfer confirmation
        """
        start = client.post("/ivr/start", json={"caller_id": "E2E_Agent_001"})
        sid = start.json()["data"]["session_id"]

        transfer = client.post("/ivr/input", json={
            "session_id": sid, "digit": "9", "current_flow": "main_menu"
        })
        assert transfer.status_code == 200
        assert transfer.json()["status"] == "transfer"
        assert "agent" in transfer.json()["prompt"].lower() or \
               "connecting" in transfer.json()["prompt"].lower()

        print("✅ E2E Agent transfer journey: PASSED")

    def test_repeat_menu_journey(self):
        """
        Full user story: Caller didn't hear the menu clearly
          Start → Press 0 → Menu repeats
        """
        start = client.post("/ivr/start", json={"caller_id": "E2E_Repeat_001"})
        sid = start.json()["data"]["session_id"]

        repeat = client.post("/ivr/input", json={
            "session_id": sid, "digit": "0", "current_flow": "main_menu"
        })
        assert repeat.status_code == 200
        # Must repeat the main menu options
        assert "1" in repeat.json()["prompt"]
        assert "2" in repeat.json()["prompt"]

        print("✅ E2E Repeat menu journey: PASSED")


# =============================================================================
# SECTION 4 — PERFORMANCE / LOAD TESTS
# =============================================================================
# What   : Verify the system handles concurrent requests without degrading
# Target : Average response < 200ms | P95 < 500ms | Error rate < 1%
# Note   : Update IVR_URL below before running against your deployed server
# =============================================================================

# ── UPDATE THIS BEFORE RUNNING LOAD TESTS ───────────────────────────────────
IVR_URL = "http://localhost:8000"   # Replace with your deployed URL
# ────────────────────────────────────────────────────────────────────────────

def load_test(num_requests: int = 50, endpoint: str = "/health") -> dict:
    """
    Sends num_requests sequential HTTP GET requests to the IVR endpoint.
    Measures success rate, average response time, and P95 response time.

    Args:
        num_requests : Number of requests to send
        endpoint     : API path to test (default: /health)

    Returns:
        dict with keys: total, success, failed, avg_ms, p95_ms, error_rate_pct
    """
    url = f"{IVR_URL}{endpoint}"
    success = 0
    failed = 0
    response_times = []

    print(f"\n🔄 Load Test: {num_requests} requests → {url}")
    print("-" * 50)

    for i in range(num_requests):
        try:
            t0 = time.time()
            res = requests.get(url, timeout=5)
            elapsed_ms = (time.time() - t0) * 1000
            response_times.append(elapsed_ms)
            if res.status_code == 200:
                success += 1
            else:
                failed += 1
                print(f"  ⚠️  Request {i+1}: Status {res.status_code}")
        except requests.exceptions.RequestException as e:
            failed += 1
            print(f"  ❌ Request {i+1} failed: {e}")

    # Statistics
    avg_ms = sum(response_times) / len(response_times) if response_times else 0
    sorted_times = sorted(response_times)
    p95_index = int(len(sorted_times) * 0.95)
    p95_ms = sorted_times[p95_index] if sorted_times else 0
    error_rate = (failed / num_requests) * 100

    # ✅ FIXED: original code was missing f-string prefix on print statements
    print(f"\n📊 Results:")
    print(f"   Total Requests : {num_requests}")
    print(f"   Successful     : {success} ({success/num_requests*100:.1f}%)")
    print(f"   Failed         : {failed}")
    print(f"   Avg Response   : {avg_ms:.2f}ms")
    print(f"   P95 Response   : {p95_ms:.2f}ms")

    # Check against targets
    print("   ✅ Avg < 200ms : PASS" if avg_ms < 200
          else f"   ⚠️  Avg {avg_ms:.0f}ms > 200ms : SLOW")
    print("   ✅ P95 < 500ms : PASS" if p95_ms < 500
          else f"   ❌ P95 {p95_ms:.0f}ms > 500ms : FAIL")
    print("   ✅ Error < 1%  : PASS" if error_rate < 1
          else f"   ❌ Error rate {error_rate:.1f}% > 1% : FAIL")

    return {
        "total": num_requests,
        "success": success,
        "failed": failed,
        "avg_ms": round(avg_ms, 2),
        "p95_ms": round(p95_ms, 2),
        "error_rate_pct": round(error_rate, 2)
    }


def load_test_session_creation(num_requests: int = 20) -> None:
    """
    More realistic load test: hits POST /ivr/start with a JSON body.
    Stresses the session creation logic, not just a static endpoint.
    """
    url = f"{IVR_URL}/ivr/start"
    success = 0
    response_times = []

    print(f"\n🔄 Session Load Test: {num_requests} sessions → {url}")
    print("-" * 50)

    for i in range(num_requests):
        try:
            t0 = time.time()
            res = requests.post(
                url,
                json={"caller_id": f"LoadUser_{i:03d}", "language": "EN"},
                timeout=5
            )
            elapsed_ms = (time.time() - t0) * 1000
            response_times.append(elapsed_ms)
            if res.status_code == 200:
                success += 1
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Request {i+1} failed: {e}")

    avg_ms = sum(response_times) / len(response_times) if response_times else 0
    # ✅ FIXED: f-string prefix was missing in original code
    print(f"\n   {success}/{num_requests} sessions created | Avg: {avg_ms:.2f}ms")


# =============================================================================
# SECTION 5 — ERROR HANDLING & LOGGING TESTS
# =============================================================================
# What  : Verify the system fails gracefully — NEVER return a raw 500
# Rule  : Every error must produce a human-readable message for the caller
#
# Good error responses:
#   404 → "Session not found or expired."
#   422 → field-level validation errors from Pydantic
#   200 with status="invalid" → caller gave bad input (wrong PNR length etc.)
# =============================================================================

class TestErrorHandling:

    def test_missing_caller_id_returns_422(self):
        """
        POST /ivr/start without the required caller_id must return
        HTTP 422 (Unprocessable Entity) — FastAPI + Pydantic validation.
        The response must include field-level error details.
        """
        response = client.post("/ivr/start", json={})  # Empty body
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("caller_id" in str(err) for err in errors)

    def test_unknown_session_returns_404(self):
        """
        Sending a session_id that does not exist must return HTTP 404.
        The detail message must mention "not found".
        """
        fake_sid = "99999999-9999-9999-9999-999999999999"
        response = client.post("/ivr/pnr", json={
            "session_id": fake_sid, "pnr_number": "1234567890"
        })
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_invalid_pnr_does_not_return_500(self):
        """
        A bad PNR must return status "invalid" with a clear prompt.
        It must NOT return 500 Internal Server Error — ever.
        """
        start = client.post("/ivr/start", json={"caller_id": "Err_PNR"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/ivr/pnr", json={
            "session_id": sid, "pnr_number": "999"  # Too short
        })
        assert response.status_code == 200   # Not a 500
        assert response.json()["status"] == "invalid"
        assert "PNR" in response.json()["prompt"]  # Must explain the problem

    def test_invalid_train_does_not_return_500(self):
        """
        A bad train number must return status "invalid", never 500.
        """
        start = client.post("/ivr/start", json={"caller_id": "Err_Train"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/ivr/tracking", json={
            "session_id": sid, "train_number": "99"  # Too short
        })
        assert response.status_code == 200   # Not a 500
        assert response.json()["status"] == "invalid"

    def test_unknown_vxml_event_handled_gracefully(self):
        """
        POST /acs/bridge with an unknown vxml_event must NOT crash.
        Must return directive = "UNKNOWN" and continue operating.
        """
        start = client.post("/ivr/start", json={"caller_id": "Err_ACS"})
        sid = start.json()["data"]["session_id"]

        response = client.post("/acs/bridge", json={
            "session_id": sid,
            "acs_call_connection_id": "ACS_ERR_001",
            "vxml_event": "completely_unknown_event",
            "tts_text": "Test"
        })
        assert response.status_code == 200   # Not a crash
        assert response.json()["data"]["bridge_payload"]["directive"] == "UNKNOWN"

    def test_health_always_returns_200(self):
        """
        GET /health must always return 200. It is polled by load balancers.
        If it returns anything else, the server gets taken offline automatically.
        Run it 5 times to confirm it is consistently healthy.
        """
        for _ in range(5):
            response = client.get("/health")
            assert response.status_code == 200


# =============================================================================
# ENTRY POINT — run load tests directly
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  IRCTC Smart IVR — M4 Load Tests")
    print("  Make sure irctc_backend.py is running first:")
    print("  → python irctc_backend.py")
    print("=" * 60)

    load_test(num_requests=50, endpoint="/health")
    load_test_session_creation(num_requests=20)

    print("\n✅ Load tests done.")
    print("   To run unit/integration/E2E tests:")
    print("   → pytest test_m4_ivr.py -v")
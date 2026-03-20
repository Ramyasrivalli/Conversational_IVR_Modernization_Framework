# 🧪 Milestone 4 — Testing & Deployment

> **Project:** Conversational IVR Modernization Framework
> **Author:** M. Ramya Srivalli | Infosys Intern | Batch 13, Group-2
> **Organization:** Infosys Internship Project

---

## 📌 What is Milestone 4?

Milestone 4 is the **validation and deployment phase** — the final stage of the IVR modernization project. The goal is to prove the system works correctly, handles edge cases and errors gracefully, and performs well under realistic load before going live.

**Two deliverables:**

| File | What It Is |
|------|-----------|
| `test_m4_ivr.py` | Complete test suite — 30+ tests across 5 layers |
| `README_M4.md` | This file — testing guide and deployment reference |

> **Requires:** `irctc_backend.py` from Milestone 2 running on `localhost:8000`

---

## 📂 Files

```
Milestone_4/
├── README_M4.md      ← This file
└── test_m4_ivr.py    ← Complete test suite (all 5 layers, 30+ tests)
```

---

## 🚀 How to Run Tests

### Step 1 — Install dependencies

```bash
pip install fastapi uvicorn pytest httpx requests
```

### Step 2 — Start the backend (Terminal 1)

```bash
cd Milestone_2
python irctc_backend.py
# Confirm: Uvicorn running on http://127.0.0.1:8000
```

### Step 3 — Run the full test suite (Terminal 2)

```bash
cd Milestone_4
pytest test_m4_ivr.py -v
```

### Step 4 — Run one specific layer

```bash
pytest test_m4_ivr.py -v -k "TestUnit"          # Unit tests only
pytest test_m4_ivr.py -v -k "TestIntegration"   # Integration tests only
pytest test_m4_ivr.py -v -k "TestE2E"           # End-to-end tests only
pytest test_m4_ivr.py -v -k "TestErrorHandling" # Error handling tests only
```

### Step 5 — Run the load test (standalone)

```bash
# Backend must be running first (Step 2 above)
python test_m4_ivr.py
```

---

## 🧪 The Five Testing Layers

Testing follows a pyramid structure — each layer serves a different purpose:

```
                    ▲
                   /E2E\
                  / Full \          Simulate complete user journeys
                 /──────────\
                / Integration \     Multi-step flows, session state
               /──────────────\
              /   Unit Tests    \   Single endpoints in isolation
             /──────────────────\
            /  Error Handling    \  Graceful failure at every boundary
           /──────────────────────\
          /  Performance / Load    \ Response time under concurrent requests
         /────────────────────────\
```

---

## Layer 1 — Unit Tests (`TestUnit`)

**Purpose:** Validate each individual endpoint contract in complete isolation. No real external calls — all dependencies are mocked.

**Speed target:** Each test must complete in under 100ms.

**Rule:** Use `unittest.mock.patch` for any external HTTP call or database operation so tests remain fast and deterministic.

| Test Name | What It Validates |
|-----------|-------------------|
| `test_root_returns_200` | Root `/` endpoint returns HTTP 200 |
| `test_health_endpoint` | `/health` returns status `success` and includes version field |
| `test_start_ivr_creates_session` | `/ivr/start` creates and returns a non-empty session_id |
| `test_start_ivr_prompt_contains_menu_options` | Welcome prompt contains menu guidance text |
| `test_pnr_check_valid_pnr` | Valid 10-digit PNR returns `CONFIRMED` status and coach/berth details |
| `test_pnr_check_invalid_pnr_rejected` | PNR shorter than 10 digits returns `status: invalid` |
| `test_booking_returns_booking_id` | Full booking payload returns a `booking_id` in response |
| `test_tatkal_booking_returns_ref_id` | Tatkal request returns either `queued` or `unavailable` gracefully |
| `test_tracking_returns_station_info` | Valid 5-digit train number returns `current_station` field |
| `test_tracking_invalid_train_rejected` | 3-digit train number returns `status: invalid` |
| `test_booking_with_mocked_external_api` | External `requests.post` is mocked — test stays under 100ms |

---

## Layer 2 — Integration Tests (`TestIntegration`)

**Purpose:** Verify that multiple API calls work together correctly — especially session state persisting across sequential requests.

**Speed target:** 1–5 seconds per test.

**Key insight:** Integration tests fail for different reasons than unit tests. A unit test fails when a function has a bug. An integration test fails when two components cannot share state correctly — for example, the session created in `/ivr/start` not being retrievable by `/ivr/input`.

| Test Name | What It Validates |
|-----------|-------------------|
| `test_session_persists_across_requests` | Session created in `/ivr/start` is retrievable via `GET /session/{id}` |
| `test_dtmf_menu_navigation_pnr` | Pressing key `1` routes to PNR flow with PNR-related prompt |
| `test_dtmf_menu_navigation_booking` | Pressing key `2` routes to booking with class selection prompt |
| `test_booking_class_then_quota_then_berth_flow` | Full 3-step sequential flow: class → quota → berth each advancing correctly |
| `test_invalid_dtmf_key_handled_gracefully` | Pressing key `7` in main menu returns `status: invalid`, not a 500 crash |
| `test_agent_transfer_key_9` | Pressing key `9` returns `status: transfer` with agent mention in prompt |
| `test_acs_bridge_stub_returns_payload` | ACS bridge returns valid `bridge_payload` with `platform: ACS` and `voice: en-IN-NeerjaNeural` |

---

## Layer 3 — End-to-End Tests (`TestE2E`)

**Purpose:** Simulate complete user call journeys from `POST /ivr/start` all the way to a final service response. Each step's output becomes the input for the next step.

**Speed target:** 10–30 seconds per full journey.

**Key difference from integration tests:** E2E tests simulate a user story, not a function. The story is: *"As a passenger, I want to check my PNR status by calling IRCTC, pressing 1, and entering my PNR."*

| Test Name | Journey Simulated |
|-----------|-------------------|
| `test_full_pnr_check_journey` | Start call → Press key 1 → Submit PNR → Receive CONFIRMED status |
| `test_full_booking_journey` | Start → Press 2 → Select class → Select quota → Select berth → Confirm booking with booking_id |
| `test_full_tatkal_journey` | Start → Press 3 → Submit Tatkal details → Receive ref ID or graceful unavailable |
| `test_full_live_tracking_journey` | Start → Press 4 → Submit train number → Receive current station and delay info |
| `test_invalid_key_does_not_crash_session` | Press invalid key → Session survives → Press valid key 1 → Recovery succeeds |

---

## Layer 4 — Performance / Load Test (`load_test`)

**Purpose:** Ensure the IVR backend handles concurrent requests within acceptable time limits. Callers notice even a 200ms delay — so response time targets are strict.

**Run:** `python test_m4_ivr.py` (standalone, not via pytest)

### Performance Targets

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Average response time | < 200ms | Callers perceive delays above 200ms as "lag" |
| 95th percentile (P95) | < 500ms | Even the slowest 5% of requests must be fast |
| Error rate | 0% | Zero tolerance for errors under normal load |
| Throughput | Scales with cloud | Must not degrade during Tatkal rush |

### What the Load Test Does

```python
def load_test(num_requests=50, url="http://127.0.0.1:8000/health"):
    # Sends num_requests sequential HTTP GET requests
    # Records response time for each
    # Calculates: avg, min, max, P95, error rate
    # Prints full stats summary
    # Asserts avg < 500ms and error_rate == 0%
```

**Sample output:**
```
═══════════════════════════════════════════════════════
  IRCTC IVR — Load Test
  Target : http://127.0.0.1:8000/health
  Requests: 50
═══════════════════════════════════════════════════════
  ✅ Request  1: 12.4ms
  ✅ Request  2: 8.9ms
  ...
───────────────────────────────────────────────────────
  Results Summary
───────────────────────────────────────────────────────
  Total requests  : 50
  Successful      : 50
  Errors          : 0 (0.0%)
  Avg response    : 11.2ms  ✅
  Min response    : 7.1ms
  Max response    : 24.6ms
  P95 response    : 18.3ms  ✅
  Error rate      : 0.0%    ✅
═══════════════════════════════════════════════════════
```

---

## Layer 5 — Error Handling Tests (`TestErrorHandling`)

**Purpose:** Verify the system fails **gracefully** at every boundary. In a phone IVR, callers cannot see error messages — the system must always return a human-readable, helpful response instead of a raw stack trace or silent failure.

| Test Name | What It Validates |
|-----------|-------------------|
| `test_session_not_found_returns_404` | Fake session ID → HTTP 404 (not 500) |
| `test_pnr_with_invalid_session_returns_404` | PNR check with bad session → 404 |
| `test_missing_required_fields_returns_422` | Empty body to `/ivr/start` → HTTP 422 (Pydantic validation) |
| `test_pnr_wrong_length_returns_invalid_status` | PNR with 3, 11, or alphabetic digits → `status: invalid` |
| `test_train_number_wrong_length_returns_invalid` | 3-digit train number → `status: invalid` |
| `test_dtmf_invalid_key_in_main_menu` | Keys 6, 7, 8 in main menu → `status: invalid`, no crash |
| `test_health_endpoint_always_available` | `/health` returns 200 regardless of session state |

---

## 🐛 Bugs Fixed from Original Sample Code

The `m4_ivr.py` sample provided in the module contained **6 deliberate bugs** as a learning exercise. All are corrected in `test_m4_ivr.py`:

| # | Location | Original (Wrong) | Fixed (Correct) | Why It Fails |
|---|----------|------------------|-----------------|--------------|
| 1 | Import | `from fastapi.testclients import TestClient` | `from fastapi.testclient import TestClient` | No module named `testclients` (extra 's') |
| 2 | Import | `import myapp.main import app` | `from irctc_backend import app` | Invalid import syntax + wrong module name |
| 3 | Client init | `client = TestClient()` | `client = TestClient(app)` | `TestClient` requires the app instance as argument |
| 4 | E2E test | `paramas={"Digits": "1"}` | `params={"Digits": "1"}` | Typo — `paramas` is not a valid keyword |
| 5 | Load test | `print("Sent {num_requests}...")` | `print(f"Sent {num_requests}...")` | Missing `f` prefix — variables not interpolated |
| 6 | Load test | `url = " "` | `url = "http://127.0.0.1:8000/health"` | Blank URL causes immediate connection error |

---

## 🚀 Deployment Guide

### Web Simulator (M3) — Static Deployment

The M3 simulator is a single HTML file with zero backend dependencies. Deploy to any static host:

| Platform | Steps |
|----------|-------|
| **Replit** | Upload `irctc_m3.html` → rename to `index.html` → Run |
| **Netlify Drop** | Go to `app.netlify.com/drop` → Drag folder → Get URL instantly |
| **GitHub Pages** | Settings → Pages → Deploy from branch → Select `main` |
| **Vercel** | `vercel deploy` from project folder |

### Backend (M2) — Server Deployment

| Platform | Command |
|----------|---------|
| **Local** | `python irctc_backend.py` → `http://localhost:8000` |
| **Render** | Connect GitHub repo → Auto-deploy on push |
| **Railway** | `railway up` from project folder |
| **Heroku** | `heroku create` + `git push heroku main` |

**Required for production:**
- Replace in-memory `SESSIONS` dict with Redis (`redis-py` + Azure Cache for Redis)
- Set `ACS_CONN_STR` as environment variable (never hardcode)
- Enable HTTPS (required for Twilio webhooks)
- Configure ACS phone number webhook to point to `/ivr/start`

---

## ✅ Testing Checklist

Complete all items before submitting Milestone 4:

**Unit Tests**
- [ ] Root endpoint returns HTTP 200
- [ ] `/health` returns status + version
- [ ] `/ivr/start` returns a valid session_id
- [ ] Valid PNR returns CONFIRMED status
- [ ] Invalid PNR returns `status: invalid`
- [ ] Valid booking payload returns booking_id
- [ ] Valid train number returns current_station

**Integration Tests**
- [ ] Session persists across requests
- [ ] DTMF key `1` routes to PNR flow
- [ ] DTMF key `2` routes to booking class selection
- [ ] Full class → quota → berth 3-step flow works
- [ ] Invalid DTMF key returns graceful error
- [ ] Key `9` triggers agent transfer
- [ ] ACS bridge returns correct payload structure

**E2E Tests**
- [ ] Full PNR check journey completes end-to-end
- [ ] Full ticket booking journey completes end-to-end
- [ ] Full Tatkal journey completes end-to-end
- [ ] Full live tracking journey completes end-to-end
- [ ] Session survives an invalid key and recovers

**Performance**
- [ ] 50 requests: avg response time < 200ms
- [ ] 50 requests: P95 < 500ms
- [ ] 50 requests: error rate = 0%

**Error Handling**
- [ ] Fake session → HTTP 404
- [ ] Missing fields → HTTP 422
- [ ] Wrong-length PNR → `status: invalid`
- [ ] Keys 6, 7, 8 in main menu → `status: invalid`

**Run all tests:**
```bash
pytest test_m4_ivr.py -v
# Expected: 30+ tests PASSED, 0 FAILED
```

---

## 🛣️ Milestone Roadmap

| Milestone | Status | Description |
|-----------|--------|-------------|
| **M1** | ✅ Complete | Legacy analysis & requirements gathering |
| **M2** | ✅ Complete | FastAPI integration layer + DTMF web simulator |
| **M3** | ✅ Complete | Conversational AI — Voice + NLU + TTS |
| **M4** | ✅ Complete | Testing & deployment — **this milestone** |

---

## 🧰 Tech Stack

| Component | Technology |
|-----------|-----------|
| Test Framework | pytest 7.4+ |
| API Test Client | FastAPI TestClient (uses httpx internally) |
| Mocking | `unittest.mock.patch` + `MagicMock` |
| Load Testing | `requests` library + `time` module |
| Structured Logging | Python `logging` module with JSON format |
| Backend Under Test | FastAPI + Uvicorn (`irctc_backend.py`) |
| Production Session Store | Redis (Azure Cache for Redis) |
| Production Hosting | Azure App Service / Render / Railway |
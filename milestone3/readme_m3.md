# Milestone 3 — Conversational AI Layer

> **Objective:** Add voice input, NLU, and natural language understanding so passengers can speak freely instead of pressing numbered menus.


---

## 📄 Files in This Milestone

| File | Description |
|---|---|
| `irctc_m3.html` | Complete conversational IVR — voice + text + DTMF, NLU engine, TTS. Zero backend. |
| `README_M3.md` | This file |

---

## 🚀 How to Run

**Option 1 — Open locally:**
```bash
# Just open irctc_m3.html in Chrome or Edge
# No server needed — everything runs in the browser
```

> ⚠️ **Must use Chrome or Edge.** Firefox does not support the Web Speech API.


---

## 🎤 Three Input Modes

| Mode | How to Use |
|---|---|
| **🎙️ Voice** | Click the microphone button → speak naturally → system understands intent |
| **⌨️ Text** | Type in the text box at the bottom → press Enter |
| **🔢 DTMF** | Click the keypad icon → press numbered keys (legacy compatibility) |

---

## 🧠 NLU Engine — How It Works

The NLU engine is built entirely in JavaScript — no cloud API required.

### 9 Supported Intents

| Intent | Example Inputs | Entities Extracted |
|---|---|---|
| `pnr_status` | "Check PNR 1234567890", "mera ticket confirm hua?" | `pnr` (10-digit) |
| `book_ticket` | "Book a ticket from Delhi to Mumbai sleeper" | `from`, `to`, `cls`, `date` |
| `tatkal_booking` | "Tatkal ticket Bangalore to Chennai tomorrow" | `from`, `to`, `cls`, `tatkal=true` |
| `train_tracking` | "Where is train 12951?", "Live status of Rajdhani" | `train` (5-digit) |
| `cancel_ticket` | "Cancel my ticket PNR 9876543210" | `pnr` |
| `fare_enquiry` | "Fare from Delhi to Bangalore 3AC" | `from`, `to`, `cls` |
| `train_schedule` | "Schedule of train 12301" | `train` |
| `complaint` | "I want to complain about food quality" | — |
| `greeting` | "Hello", "Hi", "Namaskar" | — |

### Multi-Turn State Machine (12 States)

The system remembers context so passengers don't repeat themselves:

```
User: "Book a ticket"
  → State: book_from   → "Where are you travelling from?"
User: "Delhi"
  → State: book_to     → "From Delhi — where to?"
User: "Mumbai"
  → State: book_dt     → "Which date?"
User: "15 April"
  → State: book_cl     → "Which travel class?"
User: "Sleeper"
  → Show trains, fare  → State: idle ✅
```

### Entity Extraction

| Entity | Pattern | Example |
|---|---|---|
| PNR | 10 consecutive digits | `1234567890` |
| Train | 5 consecutive digits | `12951` |
| From/To city | 15 city names + aliases | `delhi`, `New Delhi`, `NDLS`, `dilli` |
| Date | Natural language dates | `15 April`, `tomorrow`, `next Monday` |
| Travel class | Class keywords | `sleeper` → `SL`, `3ac` → `3A` |
| Tatkal flag | `tatkal`, `urgent`, `emergency` | → `tatkal: true` |

---

## 🗣️ Text-to-Speech

- **Voice:** `en-IN` (Indian English, auto-selected from available browser voices)
- **Rate:** 0.94 (slightly slower than default for clarity)
- **Pitch:** 1.05

The system speaks every response out loud. To mute, click the speaker icon.

---

## 🧪 Try These Examples

### Voice / Text Input

```
"Check PNR 1234567890"
"Where is train 12951 right now?"
"I want to book a ticket from Delhi to Mumbai"
"Tatkal ticket from Bangalore to Chennai for tomorrow"
"What is the fare from Delhi to Bangalore in 3AC?"
"Schedule of train 12301"
"Cancel my ticket 9876543210"
"I want to complain about the food quality in my train"
"Hello"
"Talk to an agent"
```

### DTMF Keys
```
1 → PNR Status flow
2 → Ticket Booking flow
3 → Tatkal Booking flow
4 → Live Train Tracking
5 → Cancellation
9 → Talk to Agent
```

---

## 🖥️ UI Layout

```
┌──────────────────┬─────────────────────────────────┬────────────────────────┐
│   SIDEBAR        │   CHAT                          │   DEBUG / STATS        │
│                  │                                 │                        │
│  Input Mode      │  [System bubble]                │  NLU Debug:            │
│  ○ Voice         │  "Welcome to IRCTC 139..."      │  Intent: pnr_status    │
│  ● Text          │                                 │  Confidence: 94%       │
│  ○ DTMF          │  [User bubble]                  │  Entities: pnr=12345   │
│                  │  "Check PNR 1234567890"          │                        │
│  Quick Queries:  │                                 │  Session Stats:        │
│  [PNR Status]    │  [Typing indicator...]          │  Intents: 3            │
│  [Train Track]   │                                 │  Turns: 7              │
│  [Book Ticket]   │  [System bubble]                │  Uptime: 4m 23s        │
│  [Fare Enquiry]  │  "PNR is CONFIRMED. Train..."   │                        │
│                  │                                 │  Intent History:       │
│  Sample PNRs:    │  [User bubble]                  │  pnr_status ✅         │
│  1234567890 ✅   │  "Where is train 12951?"        │  train_tracking ✅     │
│  9876543210 🟡   │                                 │  book_ticket 🔄        │
│  5555555555 ❌   │  [🎙️ / ⌨️ input bar]           │                        │
└──────────────────┴─────────────────────────────────┴────────────────────────┘
```

---


## 🐛 Troubleshooting

**Voice input not working:**
- Must use Chrome or Edge (not Firefox)
- Allow microphone permission when browser prompts
- Check that your microphone is not muted in system settings

**System speaks but text is garbled:**
- `en-IN` voice may not be installed. On Windows: Settings → Time & Language → Speech → Add voices → English (India)

**Intent showing as "unknown":**
- Try rephrasing. The NLU has 130+ patterns but may miss unusual phrasing.
- Use the quick query buttons in the sidebar as starting points.

**TTS not playing:**
- Some browsers block autoplay audio. Click anywhere in the page first.

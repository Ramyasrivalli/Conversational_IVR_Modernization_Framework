# 🧠 Milestone 3 — Conversational AI Layer

> **Project:** Conversational IVR Modernization Framework
> **Author:** M. Ramya Srivalli | Infosys Intern | Batch 13, Group-2
> **Organization:** Infosys Internship Project

---

## 🌐 Live Demo

👉 **[https://ticket-assistant--24b01a4278.replit.app](https://ticket-assistant--24b01a4278.replit.app)**

> Open in **Chrome or Edge** → Allow microphone → Start talking!

---

## 🖥️ Run Locally

**GitHub Codespaces:**
```
https://glorious-trout-5g9xwv77j5pgcpvjj-8000.app.github.dev/irctc_m3.html
```

**VS Code Live Server:**
```bash
# Right-click irctc_m3.html → Open with Live Server
# Then open: http://localhost:5500/irctc_m3.html
```

> ⚠️ **Voice (STT) requires Chrome or Edge** — Firefox does not support Web Speech API.

---

## 📌 What is Milestone 3?

Milestone 3 upgrades the DTMF-only simulator from Milestone 2 into a **fully conversational AI IVR**. Users can now speak naturally or type in plain English instead of pressing numbered menus.

### The Transformation

**Milestone 2 — DTMF Only:**
```
System: "Press 1 for PNR status, Press 2 for ticket booking..."
User:   *Clicks button "1"*
System: "Please enter your 10-digit PNR number followed by hash."
User:   *Clicks 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, #*
```

**Milestone 3 — Conversational AI:**
```
System: "Namaste! How can I assist you today?"
User:   "I want to check my PNR status for 1234567890"
System: "📋 PNR 1234567890 — Train 12951 Mumbai Rajdhani Express
         Status: ✅ CONFIRMED | Coach B4 | Berth 32 (Lower) | Platform 3
         Departs New Delhi at 16:55"
```

The same backend logic runs underneath — but users interact in **natural language** instead of navigating numbered menus.

---

## 📂 Files

```
Milestone_3/
├── README_M3.md      ← This file
└── irctc_m3.html     ← Complete conversational IVR simulator
```

---

## 🎯 What's New in Milestone 3

| Feature | M2 | M3 |
|---------|----|----|
| Input Method | DTMF buttons only | ✅ Voice + Text + DTMF (all three) |
| Speech-to-Text | ❌ | ✅ Web Speech API (browser-native) |
| Intent Detection | ❌ | ✅ Keyword + Regex NLU engine |
| Entity Extraction | ❌ | ✅ Stations, PNR, Date, Travel Class |
| Text-to-Speech | ❌ | ✅ SpeechSynthesis API (browser-native) |
| Multi-turn Session | ❌ | ✅ State machine dialogue manager |
| NLU Debug Panel | ❌ | ✅ Live intent name + confidence % |
| UI Theme | Dark DTMF simulator | ✅ Clean professional light theme |
| Session Stats | ❌ | ✅ Message count, intents, avg confidence |
| Intent History | ❌ | ✅ Timestamped conversation log |
| Result Cards | ❌ | ✅ PNR / Booking / Tracking info cards |
| Quick Reply Buttons | ❌ | ✅ Clickable suggested responses |
| Backend Required | Yes (FastAPI) | ❌ Zero backend needed |
| API Cost | None | ❌ Zero — fully browser-native |

---

## 🏗️ Architecture

Milestone 3 runs **entirely in the browser** — zero backend, zero API keys, zero cost.

```
Browser (Chrome / Edge)
│
├── 🎤 Web Speech API
│      → Records microphone audio
│      → Sends to Google STT (built into Chrome/Edge)
│      → Returns transcribed text
│
├── 🧠 Intent Detection Engine (JavaScript)
│      → Tests text against 9 intent pattern sets
│      → Calculates confidence score per intent
│      → Returns best-match intent + confidence %
│
├── 🔍 Entity Extraction (JavaScript)
│      → 10-digit number  → PNR
│      → 5-digit number   → Train Number
│      → City names       → Origin / Destination
│      → Date patterns    → Journey Date
│      → Class keywords   → Travel Class
│      → "tatkal/urgent"  → Tatkal Flag
│
├── 💬 Dialogue State Machine (JavaScript)
│      → Tracks current state (welcome / idle / pnr_wait / book_from / etc.)
│      → Preserves entities across turns
│      → Handles fallback when confidence < 35%
│
├── 🖥️  UI Renderer
│      → Three-panel layout (sidebar / chat / debug)
│      → Chat bubbles with sender avatars
│      → Quick reply buttons
│      → Result cards in right panel
│      → Typing indicator animation
│
└── 🔊 SpeechSynthesis API
       → Reads every bot response aloud
       → en-IN voice (Indian English)
       → Rate 0.94, Pitch 1.05
       → Toggle on/off with Voice button
```

---

## 🗣️ Supported Intents

| Intent | Trigger Keywords | Example Utterance |
|--------|-----------------|-------------------|
| 🎫 Book Ticket | book, booking, reserve, ticket, seat, journey | "Book a ticket from Delhi to Mumbai on 15 April sleeper" |
| 📋 PNR Status | pnr, status, confirm, rac, waitlist, wl | "Check PNR 1234567890" |
| 📍 Live Train Tracking | live, track, running, where, late, delay, location | "Live status of train 12951" |
| 🕐 Train Schedule | schedule, timetable, departure, arrival, route | "Schedule of train 12301" |
| ❌ Cancel Ticket | cancel, cancellation, refund | "I want to cancel my ticket PNR 9876543210" |
| 💰 Fare Enquiry | fare, price, cost, how much, tariff | "What is the fare from Delhi to Bangalore 3AC?" |
| ⚡ Tatkal Booking | tatkal, urgent, emergency | "Tatkal ticket from Bangalore to Chennai tomorrow" |
| 📢 Complaint | complaint, grievance, issue, problem, feedback | "I have a complaint about food quality" |
| 👋 Greeting | hi, hello, hey, namaste, good morning/evening | "Hello" / "Namaste" |

---

## 🔍 How the NLU Engine Works

### Step 1 — Intent Scoring

Each intent has a list of regex patterns. The engine tests the user's sentence against every pattern and counts how many match.

```javascript
const INTENTS = {
  pnr_status: [
    /\bpnr\b/,        // exact word "pnr"
    /\bstatus\b/,     // exact word "status"
    /\bconfirm/,      // "confirm" or "confirmed"
    /\brac\b/,        // "rac"
    /\bwaitlist\b/    // "waitlist"
  ],
  book_ticket: [
    /\bbook\b/,
    /\bticket\b/,
    /\btatkal\b/,
    /\bwant.*ticket/,
    /\bneed.*ticket/
    // ... 10 patterns
  ]
  // 9 intents total
}
```

**Score = matched patterns ÷ total patterns for that intent**

The intent with the highest score wins. If confidence is below **35%**, the system falls back to the current dialogue state (assumes the user is answering the last question asked).

### Step 2 — Entity Extraction

| Entity | Detection Pattern | Example |
|--------|------------------|---------|
| PNR Number | 10-digit number regex | `1234567890` |
| Train Number | 5-digit number regex (not PNR) | `12951` |
| Origin City | City list scan + "from/leaving/departing" prefix | `delhi`, `mumbai` |
| Destination City | City list scan + "to/towards/destination" prefix | `chennai`, `kolkata` |
| Journey Date | `DD Mon` pattern or today/tomorrow keyword | `15 April`, `tomorrow` |
| Travel Class | class keyword map | `sleeper` → `SL`, `3AC` → `3A` |
| Tatkal Flag | tatkal/urgent/emergency in sentence | `tatkal`, `urgent` |

**15 Indian cities supported:** Delhi, Mumbai, Bangalore, Chennai, Kolkata, Hyderabad, Jaipur, Pune, Ahmedabad, Lucknow, Surat, Agra, Bhopal, Nagpur, Kanpur

### Step 3 — Dialogue State Machine

The state machine remembers what was said across multiple turns:

```
State: welcome
  → Any input → State: idle

State: idle
  → Intent: pnr_status + has PNR   → Lookup and respond
  → Intent: pnr_status + no PNR    → State: pnr_wait ("Please share your 10-digit PNR")
  → Intent: book_ticket              → State: book_from ("Where to travel from?")
  → Intent: train_running_status     → State: track_wait ("Please provide train number")

State: pnr_wait
  → User says "1234567890"           → PNR lookup and respond → State: idle

State: book_from → State: book_to → State: book_dt → State: book_cl
  → Collects origin, destination, date, class one step at a time
  → When all 4 collected → Show trains + fare → State: idle
```

**Context is preserved** — if the user is mid-booking and says something ambiguous, the engine assumes they are answering the last question asked, not starting a new flow.

---

## 🧪 Test It Out

### One-shot booking (all info in one sentence)
```
Book ticket from Delhi to Mumbai on 15 April sleeper class
```

### Step-by-step booking (multi-turn)
```
Turn 1: "Book a ticket"      → System asks: "Where to travel from?"
Turn 2: "Delhi"              → System asks: "Where to travel to?"
Turn 3: "Mumbai"             → System asks: "Which date?"
Turn 4: "15 April"           → System asks: "Which class?"
Turn 5: "Sleeper"            → System shows available trains + fare
```

### Sample PNRs

| PNR | Expected Result |
|-----|----------------|
| `1234567890` | ✅ CONFIRMED — Train 12951, Coach B4, Berth 32 (Lower), Platform 3 |
| `9876543210` | 🟡 RAC 12 — Train 12630, Coach A2, Platform 1 |
| `5555555555` | ❌ WL 89 — Train 12483 (no berth assigned) |
| `4444444444` | ✅ CONFIRMED — Train 22119, Coach H1, Berth 05 (Upper), Platform 5 |

### Sample Train Numbers to Track

| Train | Name | Status |
|-------|------|--------|
| `12951` | Mumbai Rajdhani Express | On Time — at Surat, next: Vadodara |
| `12301` | Howrah Rajdhani Express | On Time — at Allahabad, next: Kanpur |
| `12630` | Yeshwantpur Express | 12 min late — at Nagpur, next: Raipur |
| `22119` | Mumbai CSMT AC Express | 5 min late — at Manmad, next: Nashik Road |
| `12002` | Bhopal Shatabdi Express | On Time — at Agra, next: Gwalior |

---

## ⚙️ Three Input Modes

### Mode 1 — Text Chat (Default)
Type your query in the input box and press **Enter** or click **➤**. Best for testing and debugging — you can craft exact queries to verify NLU accuracy.

### Mode 2 — Voice (STT)
1. Click the **🎤 microphone button** in the input bar
2. Allow microphone access when the browser prompts
3. Speak your query clearly in English
4. Text appears in the input box as you speak (interim results)
5. When you stop speaking, the query auto-sends

**Technical implementation:**
```javascript
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
const recog = new SR();
recog.lang = 'en-IN';        // Indian English accent
recog.continuous = false;    // Stop after one sentence
recog.interimResults = true; // Show partial text while speaking

recog.onresult = (event) => {
    let final = '', interim = '';
    for (const r of event.results) {
        if (r.isFinal) final += r[0].transcript;
        else interim += r[0].transcript;
    }
    document.getElementById('inp').value = final || interim;
};
```

The browser sends audio to Google's STT API (built into Chrome/Edge). No API key or cost is required.

### Mode 3 — DTMF Keypad
Click **DTMF Keypad** in the left panel to show the number pad. Keys map to predefined queries:

| Key | Action |
|-----|--------|
| `1` | Check PNR status |
| `2` | Book a ticket |
| `3` | Track my train |
| `4` | Train schedule |
| `5` | Fare enquiry |
| `6` | Cancel ticket |
| `9` | File complaint |
| `0` | Exit |

You can also type a full 10-digit PNR directly on the keypad — after 10 digits it auto-sends a PNR query.

---

## 🔊 Text-to-Speech (TTS)

Every bot response is read aloud using the browser's built-in SpeechSynthesis API:

```javascript
function speak(text) {
    const utterance = new SpeechSynthesisUtterance(
        text.replace(/<[^>]+>/g, '')  // strip HTML tags
    );
    utterance.lang = 'en-IN';   // Indian English
    utterance.rate = 0.94;      // slightly slower for clarity
    utterance.pitch = 1.05;     // slightly higher

    const voices = window.speechSynthesis.getVoices();
    const preferred = voices.find(v => v.lang === 'en-IN')
                   || voices.find(v => v.lang.startsWith('en'));
    if (preferred) utterance.voice = preferred;

    window.speechSynthesis.speak(utterance);
}
```

Toggle voice on/off using the **🔊 Voice On / 🔇 Voice Off** button in the top bar.

---

## 🖥️ UI Layout

Three-panel layout visible at all times:

```
┌─────────────────┬──────────────────────────┬──────────────────┐
│   LEFT PANEL    │       CHAT PANEL         │   RIGHT PANEL    │
│                 │                          │                  │
│ Input Mode      │  🤖 RailSpeak            │ Session Stats    │
│ ● Text Chat     │  "Namaste! 🙏 ..."       │ Messages:    5   │
│ ○ Voice (STT)   │                          │ Intents:     2   │
│ ○ DTMF Keypad   │  You                     │ Avg Conf:   87%  │
│                 │  "Check PNR 1234567890"  │                  │
│ Quick Queries   │                          │ NLU Debug        │
│ 📋 PNR Status   │  🤖 RailSpeak            │ Intent: pnr_...  │
│ 🎫 Book Ticket  │  "✅ CONFIRMED..."       │ Confidence: 87%  │
│ ⚡ Tatkal       │  [Check another PNR]     │ State: idle      │
│ 📍 Track Train  │  [Track this train]      │ PNR: 1234567890  │
│ 🕐 Schedule     │                          │ Train: —         │
│ 💰 Fare         │  [🎤] [input box]  [➤]  │ From: —          │
│ ❌ Cancel       │                          │ To: —            │
│ 📢 Complaint    │  Press 🎤 or type above  │                  │
│                 │                          │ Last Result      │
│ Sample PNRs     │                          │ 📋 PNR 1234...   │
│ 1234567890 →    │                          │ CONFIRMED        │
│ 9876543210 →    │                          │                  │
│ 5555555555 →    │                          │ Intent History   │
│ 4444444444 →    │                          │ 10:42 pnr_status │
└─────────────────┴──────────────────────────┴──────────────────┘
```

---

## 🐛 Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Mic button does nothing | Browser not supported | Use Chrome or Edge — Firefox does not support Web Speech API |
| Microphone access denied | Browser permissions | Click the 🔒 icon in the address bar → Allow microphone |
| Voice recognised incorrectly | Background noise or fast speech | Speak clearly at moderate pace; try typing the same query |
| Bot says "I didn't understand" | Low NLU confidence | Use keywords: "book", "PNR", "track", "fare", "cancel" — check NLU Debug panel for what was detected |
| TTS not speaking | System volume muted | Check system and browser volume; click Voice On button in top bar |

---

## 🛣️ Milestone Roadmap

| Milestone | Status | Description |
|-----------|--------|-------------|
| **M1** | ✅ Complete | Legacy analysis & requirements gathering |
| **M2** | ✅ Complete | FastAPI integration layer + DTMF web simulator |
| **M3** | ✅ Complete | Conversational AI — **this milestone** |
| **M4** | 🔜 Upcoming | Testing & deployment |

---

## 🧰 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Vanilla JavaScript (ES6+) |
| UI | HTML5 + CSS3 (no framework dependencies) |
| Fonts | Plus Jakarta Sans + IBM Plex Mono (Google Fonts) |
| Speech-to-Text | Web Speech API — browser-native, powered by Google STT |
| Text-to-Speech | SpeechSynthesis API — browser-native |
| NLU Engine | Custom Regex + Keyword pattern matching (JavaScript) |
| Dialogue Manager | JavaScript state machine with entity persistence |
| Live Demo | Replit |
| Local Dev | GitHub Codespaces |
| Target Cloud — M4 | Azure Communication Services + BAP / Twilio |
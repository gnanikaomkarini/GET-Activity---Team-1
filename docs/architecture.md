# System Architecture

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Browser (React App)                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  HomeForm → gemini.js → Gemini API                   │   │
│  │  Results ← JSON response                              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Flow

### 1. User Fills Form
```
User → HomeForm → Selects appliances and usage
```

### 2. AI Analysis
```
HomeForm → construct prompt → gemini.js
gemini.js → fetch() → Google Gemini API
Gemini API → JSON response → gemini.js
gemini.js → parse JSON → HomeForm
```

### 3. Display Results
```
Results component → Show summary, waste, tips, recommendations
```

---

## Components

### HomeForm
- Household info inputs (occupants, location)
- Appliance selection grid
- Usage presets per appliance
- Additional context textarea
- Submit button

### Results
- Summary cards (kWh, biggest consumer)
- Waste analysis list
- Saving tips list
- Recommendations accordion
- After-savings estimate

### Loading
- Spinner animation during API call

---

## API Integration

**Endpoint**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent`

**Request:**
```json
{
  "contents": [{
    "parts": [{ "text": "analyze my energy usage..." }]
  }]
}
```

**Response:**
```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "text": "{ json analysis }"
      }]
    }
  }]
}
```

---

## Environment

API key stored in `.env`:
```
VITE_GEMINI_API_KEY=your_key_here
```

Get free key from: https://aistudio.google.com/apikey

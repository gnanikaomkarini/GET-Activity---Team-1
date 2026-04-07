# Technology Stack

## Simple React Frontend

```
┌─────────────────────────────────────────────────────┐
│  Frontend: React + Vite                              │
│  ┌─────────────────────────────────────────────────┐ │
│  │  HomeForm (Appliance Input)                      │ │
│  │  Results (AI Recommendations)                   │ │
│  └─────────────────────┬───────────────────────────┘ │
│                        │                             │
└────────────────────────┼─────────────────────────────┘
                         │ fetch()
                         ▼
┌─────────────────────────────────────────────────────┐
│  Google Gemini API (gemini-2.5-flash)               │
│  - Direct REST API calls                            │
│  - No SDK (avoids CORS issues)                     │
└─────────────────────────────────────────────────────┘
```

---

## Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Frontend | React 18 + Vite | Fast, modern |
| AI | Google Gemini 2.5 Flash | Fast, affordable |
| Styling | CSS | Simple, no dependencies |

---

## File Structure

```
frontend/
├── src/
│   ├── App.jsx              # Main app
│   ├── App.css              # Styles
│   ├── main.jsx             # Entry point
│   ├── components/
│   │   ├── HomeForm.jsx    # Appliance input form
│   │   ├── Results.jsx     # AI recommendations display
│   │   └── Loading.jsx     # Loading spinner
│   ├── services/
│   │   └── gemini.js       # Gemini API integration
│   └── data/
│       └── appliances.js    # Appliance database
├── .env.example             # API key template
├── package.json
└── index.html
```

---

## Dependencies

```
react
react-dom
@google/generative-ai (optional - using direct fetch)
vite
```

---

## AI: Google Gemini

**API**: Direct REST calls to `generativelanguage.googleapis.com`

**How it works:**
```javascript
fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${API_KEY}`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    contents: [{ parts: [{ text: prompt }] }]
  })
})
```

**Benefits:**
- Free tier available (15 requests/minute, 1500 requests/day)
- Fast responses
- Good quality analysis
- No SDK needed

---

## No Database

This app is session-based:
- No backend
- No database
- All data is temporary (per session)
- Future: could add localStorage for history

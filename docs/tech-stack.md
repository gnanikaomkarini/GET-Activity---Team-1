# Technology Stack

## Simple Stack (No API Keys)

```
┌─────────────────────────────────────────────────────┐
│  Frontend: HTML + JS + Chart.js + Puter.js           │
│  - Puter.js calls Claude Sonnet 4.6 (free, no key)   │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│  Backend: Python + FastAPI                           │
│  - Simulator engine                                  │
│  - Caching                                          │
│  - API endpoints                                     │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│  Database: SQLite (dev) / PostgreSQL (prod)          │
└─────────────────────────────────────────────────────┘
```

---

## Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Frontend | Vanilla JS + Chart.js | No build step |
| AI | Puter.js (Claude Sonnet 4.6) | Free, no API key |
| Backend | Python 3.11 + FastAPI | Simple, async |
| Database | SQLite (dev) / PostgreSQL (prod) | Zero config |

---

## File Structure

```
backend/
├── main.py              # FastAPI app
├── database.py          # DB setup
├── simulator.py         # Device simulation
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── routers/
│   ├── devices.py       # Device CRUD
│   ├── readings.py      # Readings
│   └── simulation.py    # Simulation + cache
frontend/
└── index.html           # Dashboard with Puter.js
```

---

## Dependencies

```
fastapi>=0.100
uvicorn[standard]>=0.23
sqlalchemy>=2.0
pydantic>=2.0
python-dotenv>=1.0
```

---

## AI: Puter.js

[Puter.js](https://js.puter.com) provides free access to Claude AI from the browser.

**Benefits:**
- No API key needed
- Free for developers (users pay)
- Uses Claude Sonnet 4.6
- Simple `puter.ai.chat()` API

**How it works:**
```javascript
puter.ai.chat("Analyze this...", { model: 'claude-sonnet-4-6' })
  .then(response => JSON.parse(response.message.content[0].text));
```

---

## Caching

Analysis is cached based on readings hash:

```
readings → md5 hash → check cache → return cached or call AI
```

- Same readings = same hash = cached result
- Different readings = new hash = new analysis
- Stored in `analyses` table

---

## Cost (Monthly)

| Component | Cost |
|-----------|------|
| Compute | $5-10 (Railway/Render) |
| Database | Free (SQLite) or $5 (PostgreSQL) |
| AI | Free (Puter.js) |
| **Total** | **$5-15/month** |

# System Architecture

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Browser (HTML + JS + Chart.js + Puter.js)                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  puter.ai.chat() → Claude Sonnet 4.6                 │   │
│  │  Returns: { summary, forecast, anomalies, recs }   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ POST /api/analysis (save cache)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Python Backend (FastAPI)                                    │
│  - Simulates devices and readings                           │
│  - Stores devices, readings, analyses                       │
│  - Caches AI analysis results                               │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  SQLite / PostgreSQL                                        │
│  - devices, readings, analyses                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Flow

### 1. User generates data
```
Frontend → POST /api/simulate/generate
Backend → Creates device readings in DB
```

### 2. AI Analysis (Client-side)
```
Frontend → GET /api/devices/:id/readings
Backend → Returns readings + checks cache

Frontend → puter.ai.chat() (Claude Sonnet)
Backend → Parse JSON response

Frontend → POST /api/analysis
Backend → Cache the analysis
```

### 3. Subsequent requests (Cached)
```
Frontend → GET /api/devices/:id/readings
Backend → Returns cached analysis (same hash)
Frontend → Display without calling AI
```

---

## Components

### Simulator Engine
Generates realistic energy data for virtual devices.

**Patterns:**
- Time-of-day (low at night, peaks morning/evening)
- Weekday vs weekend
- Seasonal adjustments
- Random variations

### Caching System
- Hash of readings determines cache key
- Same data = same hash = cached result
- No redundant AI calls

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/devices` | GET/POST/DELETE | Device management |
| `/api/readings` | GET | Get energy readings |
| `/api/devices/:id/readings` | GET | Get readings + cache check |
| `/api/simulate/generate` | POST | Generate readings |
| `/api/simulate/scenario` | POST | Run scenario |
| `/api/analysis` | POST | Save AI analysis (cache) |

---

## Data Models

```python
Device: id, name, type, location, params, status
Reading: id, device_id, timestamp, power_watts, energy_kwh, voltage, current
Analysis: id, device_id, readings_hash, analysis_data, readings_count, cached
```

### Analysis Cache
```python
readings_hash = md5(json.dumps(readings, sort_keys=True))
# Same readings = same hash = cached analysis
```

---

## Security

- No authentication (open for demo)
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy)

---

## Deployment

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Free hosting: Railway, Render, Fly.io

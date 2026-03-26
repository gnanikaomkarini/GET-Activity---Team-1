# System Architecture

## Simple Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Browser (HTML + JS + Chart.js)                             │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/JSON
┌─────────────────────────▼───────────────────────────────────┐
│  Python Backend (FastAPI)                                    │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Auth      │  │  Simulator  │  │    ML       │          │
│  │   (JWT)     │  │   Engine    │  │  (Forecast, │          │
│  │             │  │             │  │   Anomaly)  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   API       │  │   Models    │  │ Recommendations│       │
│  │  Endpoints  │  │  (SQLAlchemy)│  │   Engine    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│  SQLite / PostgreSQL                                          │
│  - users, devices, readings, recommendations                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. Simulator Engine

Generates realistic energy data for virtual devices.

```
Device Factory → Pattern Generator → Reading Generator
```

**Patterns:**
- Time-of-day (low at night, peaks morning/evening)
- Weekday vs weekend
- Seasonal (heating/cooling)
- Random variation (±10%)

### 2. ML Models

| Model | Purpose |
|-------|---------|
| Forecasting | Predict next 24h consumption |
| Anomaly | Detect spikes/drops |
| Recommendations | Generate energy tips |

### 3. API

RESTful endpoints:

```
POST   /api/auth/register
POST   /api/auth/login
GET    /api/devices
POST   /api/devices
GET    /api/readings?device_id=...
POST   /api/readings (simulator writes here)
GET    /api/recommendations
GET    /api/forecast
POST   /api/simulator/scenario
```

### 4. Data Models

```python
User: id, email, password_hash, created_at
Device: id, user_id, type, name, params, status
Reading: id, device_id, timestamp, power, energy
Recommendation: id, user_id, title, description, savings
```

---

## Security

- JWT tokens for auth
- Password hashing (bcrypt)
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy)

---

## Deployment

Single Python process + SQLite = runs anywhere.

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Free hosting: Railway, Render, Fly.io

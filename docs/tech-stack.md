# Technology Stack

## Simple Python-Only Stack

No Node.js, no Redis. Just Python + database.

```
┌─────────────────────────────────────────────────────┐
│  Frontend: HTML + JavaScript (served by Python)       │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│  Backend: Python + FastAPI                           │
│  - Simulation engine                                 │
│  - ML models (forecasting, anomaly detection)       │
│  - API endpoints                                     │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│  Database: SQLite (dev) / PostgreSQL (prod)          │
│  - Users, devices, readings, recommendations         │
└─────────────────────────────────────────────────────┘
```

---

## Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Backend | Python 3.11 + FastAPI | Simple, async, auto-docs |
| Database | SQLite (dev) / PostgreSQL (prod) | File-based or scalable |
| ML | PyTorch, NumPy | Forecasting, anomaly |
| Frontend | Vanilla JS + Chart.js | No build step, simple |
| Auth | JWT (built into FastAPI) | Simple tokens |

---

## File Structure

```
/
├── app/
│   ├── main.py          # FastAPI app
│   ├── models.py        # Database models
│   ├── schemas.py       # API schemas
│   ├── auth.py          # JWT auth
│   ├── simulator.py     # Device simulation
│   ├── ml/
│   │   ├── forecast.py  # Forecasting model
│   │   ├── anomaly.py   # Anomaly detection
│   │   └── recommend.py # Recommendations
│   └── routers/
│       ├── users.py
│       ├── devices.py
│       └── readings.py
├── static/
│   └── index.html       # Dashboard
├── requirements.txt
└── README.md
```

---

## Dependencies

```
fastapi>=0.100
uvicorn
sqlalchemy
pydantic
python-jose[cryptography]  # JWT
pytorch
numpy
pandas
chart.js
```

---

## Cost (Monthly)

Free to run locally. For hosting:

| Component | Cost |
|-----------|------|
| Compute | $5-10 (Railway/Render) |
| Database | Free (SQLite) or $5 (PostgreSQL) |
| **Total** | **$5-15/month** |

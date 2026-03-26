# Technology Stack

## Simple Python Stack with AI

```
┌─────────────────────────────────────────────────────┐
│  Frontend: HTML + JavaScript (served by Python)       │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│  Backend: Python + FastAPI                           │
│  - Simulator engine                                  │
│  - AI service (OpenAI/Anthropic)                    │
│  - API endpoints                                    │
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
| Backend | Python 3.11 + FastAPI | Simple, async, auto-docs |
| Database | SQLite (dev) / PostgreSQL (prod) | File-based or scalable |
| AI | OpenAI GPT-4 or Anthropic Claude | Recommendations, chat |
| Frontend | Vanilla JS + Chart.js | No build step |
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
│   ├── ai/
│   │   ├── client.py    # AI API client
│   │   ├── recommend.py # AI recommendations
│   │   ├── explain.py   # AI anomaly explanations
│   │   └── chat.py      # AI chat
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
openai>=1.0  # or anthropic
chart.js
```

---

## AI Service

Uses LLMs for:

| Task | Prompt Example |
|------|----------------|
| Recommendations | "Based on this user's data, suggest 3 specific ways to reduce their energy bill." |
| Anomaly Explanation | "Explain why this spike happened and how to prevent it." |
| Forecasting | "Predict their monthly bill and explain the factors." |
| Chat | Answer questions about their energy usage." |

---

## Cost (Monthly)

| Component | Cost |
|-----------|------|
| Compute | $5-10 (Railway/Render) |
| Database | Free (SQLite) or $5 (PostgreSQL) |
| AI (OpenAI) | ~$10-50 (depending on usage) |
| **Total** | **$15-65/month** |

**Note:** AI costs depend on number of requests. Most users will cost <$1/month in AI tokens.

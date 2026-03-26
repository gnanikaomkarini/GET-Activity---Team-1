# System Architecture

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Browser (HTML + JS + Chart.js)                             │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/JSON
┌─────────────────────────▼───────────────────────────────────┐
│  Python Backend (FastAPI)                                    │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Auth      │  │  Simulator  │  │    AI       │          │
│  │   (JWT)     │  │   Engine    │  │  (LLM)      │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐                            │
│  │   API       │  │   Database  │                            │
│  │  Endpoints  │  │  (SQLite)   │                            │
│  └─────────────┘  └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. Simulator Engine

Generates realistic energy data for virtual devices.

**Patterns:**
- Time-of-day (low at night, peaks morning/evening)
- Weekday vs weekend
- Seasonal (heating/cooling)
- Random variation (±10%)

### 2. AI Service (LLM)

Uses a Large Language Model to:

| Task | How AI Helps |
|------|--------------|
| Recommendations | Generate personalized energy-saving tips |
| Anomaly Explanation | Explain why usage spiked/dropped |
| Forecasting | Narrate trends and predict bills |
| Chat | Answer user questions about energy |

**Example:**
```python
# AI generates recommendation based on user's data
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{
        "role": "user",
        "content": f"User's AC runs 6+ hours daily. "
                   f"Monthly bill: $180. "
                   f"Suggest 3 specific tips to reduce AC usage."
    }]
)
```

### 3. API Endpoints

```
POST   /api/auth/register
POST   /api/auth/login
GET    /api/devices
POST   /api/devices
GET    /api/readings?device_id=...
POST   /api/readings
GET    /api/recommendations (AI-generated)
GET    /api/forecast
POST   /api/simulator/scenario
POST   /api/chat (ask AI questions)
```

### 4. Data Models

```python
User: id, email, password_hash, created_at
Device: id, user_id, type, name, params, status
Reading: id, device_id, timestamp, power, energy
Recommendation: id, user_id, title, description, savings, generated_at
```

---

## AI Integration

The AI service analyzes user data and generates:

1. **Personalized Tips** - Based on consumption patterns
2. **Anomaly Explanations** - Why did usage spike?
3. **Bill Predictions** - Project monthly costs
4. **Actionable Advice** - Specific steps to save energy

---

## Security

- JWT tokens for auth
- Password hashing (bcrypt)
- Input validation (Pydantic)
- SQL injection prevention (SQLAlchemy)
- API key for AI service stored securely

---

## Deployment

Single Python process + SQLite.

```bash
pip install -r requirements.txt
OPENAI_API_KEY=sk-... uvicorn app.main:app --reload
```

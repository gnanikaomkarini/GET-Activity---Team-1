# Energy Efficiency Advisor

AI-powered energy simulation and personalized recommendations.

## Setup

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key

# 3. Run the backend
uvicorn main:app --reload

# 4. Open browser
# Go to http://localhost:8000
```

## Features

- Simulate virtual energy devices
- Generate realistic consumption data
- **Single AI call** for complete analysis (summary, forecast, anomalies, recommendations, score)
- Run scenarios (heating, cooling, vacation, anomalies)
- Energy score and recommendations

## Structure

```
backend/
├── main.py         - FastAPI app
├── models/         - Database models
├── schemas/        - API schemas
├── routers/        - API routes
├── ai/
│   └── service.py  - AI service (single analyze_energy function)
├── simulator.py    - Device simulation
├── .env            - Configuration
frontend/
└── index.html      - Dashboard UI
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/devices` | List all devices |
| `POST /api/devices` | Add a device |
| `DELETE /api/devices/:id` | Remove a device |
| `GET /api/readings` | Get energy readings |
| `POST /api/simulate/generate` | Generate readings |
| `POST /api/simulate/scenario` | Run scenario |
| `GET /api/analysis` | **Get complete AI analysis** (one call) |
| `GET /api/recommendations` | Get recommendations only |

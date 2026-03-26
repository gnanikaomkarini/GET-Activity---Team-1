# Energy Efficiency Advisor

AI-powered energy simulation and personalized recommendations.

## Quick Start

```bash
# 1. Install backend dependencies
cd backend
pip install -r requirements.txt

# 2. Set your OpenAI API key
export OPENAI_API_KEY=sk-your-key

# 3. Run the backend
uvicorn main:app --reload

# 4. Open browser
# Go to http://localhost:8000
```

## Structure

```
backend/
  main.py        - FastAPI app
  models/        - Database models
  schemas/       - API schemas
  routers/       - API routes
  ai/            - AI service
  simulator.py   - Device simulation
frontend/
  index.html     - Dashboard UI
```

## Features

- Simulate virtual energy devices
- Generate realistic consumption data
- AI-powered recommendations
- AI chat for energy questions
- Scenario runner (heating, cooling, vacation)
- Energy forecasting

## API

- `POST /api/auth/register` - Register
- `POST /api/auth/login` - Login
- `GET /api/devices` - List devices
- `POST /api/devices` - Create device
- `GET /api/readings` - Get readings
- `POST /api/simulate/generate` - Generate data
- `POST /api/simulate/scenario` - Run scenario
- `GET /api/recommendations` - AI recommendations
- `POST /api/chat` - AI chat

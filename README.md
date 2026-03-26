# Energy Efficiency Advisor

AI-powered energy simulation with Claude AI (free, no API key needed).

## Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://localhost:8000

## Features

- Simulate virtual energy devices
- Generate realistic consumption data
- **Claude AI** analysis (via Puter.js - free)
- Smart caching (avoid redundant AI calls)
- Run scenarios (heating, cooling, vacation)
- Energy score and recommendations

## Architecture

```
Frontend (Puter.js) → Claude Sonnet 4.6 → POST to Backend → Cache
```

# Energy Efficiency Advisor

AI-powered energy simulation with Claude AI (free, no API key needed).

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 for frontend, http://localhost:8000 for API.

## Features

- **Simulate** virtual energy devices
- **Generate** realistic consumption data
- **Claude AI** analysis (via Puter.js - free)
- **Smart caching** - avoid redundant AI calls
- **Run scenarios** - heating, cooling, vacation
- **Energy score** - grade your efficiency (A-F)
- **Recommendations** - personalized tips with savings

## Tech Stack

- **Frontend**: React + Vite + Chart.js
- **Backend**: Python + FastAPI + SQLAlchemy
- **AI**: Puter.js (Claude Sonnet 4.6) - free, no API key
- **Database**: SQLite

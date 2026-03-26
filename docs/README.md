# AI-Based Energy Efficiency Advisor

An intelligent system that **simulates** energy consumption and uses **Claude AI** to generate personalized energy-saving recommendations.

## No API Keys Required

Uses [Puter.js](https://js.puter.com) to access Claude Sonnet 4.6 for free.

---

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Simulate  │ ──▶ │    Claude   │ ──▶ │  Dashboard  │
│  Energy    │     │    AI       │     │  + Cache    │
└─────────────┘     └─────────────┘     └─────────────┘
```

1. **Simulate** virtual devices generating energy data
2. **Claude AI** analyzes the data (via Puter.js)
3. **View** personalized recommendations and score
4. **Cache** results for fast reload

---

## Features

- **IoT Simulator** - Virtual devices with realistic patterns
- **Claude AI** - Complete analysis in one call
- **Smart Caching** - Avoid redundant AI calls
- **Scenarios** - Test heating, cooling, vacation
- **Energy Score** - Grade your efficiency (A-F)
- **Recommendations** - Personalized tips with savings

---

## Quick Start

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Run (no config needed!)
uvicorn main:app --reload

# 3. Open browser
# Go to http://localhost:8000
```

That's it! No API keys, no configuration.

---

## Documentation

- [Architecture](./architecture.md)
- [Features](./features.md)
- [Tech Stack](./tech-stack.md)
- [Roadmap](./roadmap.md)

# AI-Based Energy Efficiency Advisor

An intelligent system that **simulates** energy consumption and uses **AI** to generate personalized energy-saving recommendations.

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Simulate   │ ──▶ │  Collect    │ ──▶ │    Ask      │
│  Energy     │     │  Data       │     │    AI       │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
                                        ┌─────────────┐
                                        │  Personalized│
                                        │  Tips       │
                                        └─────────────┘
```

1. **Simulate** virtual devices generating realistic energy data
2. **Collect** consumption patterns over time
3. **Ask AI** to analyze and suggest improvements
4. **Get** personalized energy-saving tips

---

## Features

- **IoT Simulator** - Virtual devices with realistic patterns
- **Energy Dashboard** - Visualize simulated consumption
- **AI Recommendations** - Personalized tips from AI
- **AI Anomaly Detection** - AI explains unusual patterns
- **AI Forecasting** - Predict bills and trends
- **AI Chat** - Ask questions about your energy
- **Scenario Runner** - Test heating, cooling, vacation
- **Gamification** - Energy score, badges, challenges

---

## AI Features

Uses LLMs (OpenAI GPT-4 or Anthropic Claude) to:

| Feature | AI Does |
|---------|---------|
| Recommendations | "Here are 3 specific ways to reduce your AC usage" |
| Anomaly Explanation | "Your spike happened because you ran dryer + oven" |
| Forecasting | "You're on track to spend $220 this month" |
| Chat | Answer any question about your energy usage |

---

## Documentation

- [Architecture](./architecture.md)
- [Features](./features.md)
- [Tech Stack](./tech-stack.md)
- [Roadmap](./roadmap.md)

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set your AI API key
export OPENAI_API_KEY=sk-...

# Run the app
uvicorn app.main:app --reload
```

Open http://localhost:8000 to see the dashboard.

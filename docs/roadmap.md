# Implementation Roadmap

## Overview

Python + AI (LLM). Simple 8-week build.

---

## Phase 1: Foundation (Weeks 1-2)

**Goal:** Working app with simulation

### Week 1: Backend + Database
- [ ] Set up FastAPI project
- [ ] Create database models
- [ ] Implement JWT auth
- [ ] Basic CRUD endpoints

### Week 2: Simulator
- [ ] Build device simulator
- [ ] Time-of-day patterns
- [ ] CRUD endpoints for devices
- [ ] Reading generation

**Deliverable:** API with working simulation.

---

## Phase 2: AI Integration (Weeks 3-4)

**Goal:** AI-powered features

### Week 3: AI Service
- [ ] Set up OpenAI/Anthropic client
- [ ] Build recommendation prompt
- [ ] Build anomaly explanation prompt
- [ ] Build chat prompt

### Week 4: AI Features
- [ ] Connect AI to recommendations endpoint
- [ ] Connect AI to anomaly explanations
- [ ] Build AI chat endpoint
- [ ] Add AI-powered forecast

**Deliverable:** AI generates personalized insights.

---

## Phase 3: Frontend (Weeks 5-6)

**Goal:** Dashboard

- [ ] Simple HTML/JS dashboard
- [ ] Energy charts
- [ ] Recommendation display
- [ ] Chat interface
- [ ] Scenario selector

**Deliverable:** Working dashboard.

---

## Phase 4: Polish (Weeks 7-8)

**Goal:** Launch-ready

- [ ] Add scenarios (heating, cooling, vacation)
- [ ] Gamification (energy score, badges)
- [ ] Cost estimation
- [ ] Error handling
- [ ] Documentation

**Deliverable:** Ready to use.

---

## Timeline

```
Week 1-2    Week 3-4    Week 5-6    Week 7-8
    │           │           │           │
    ▼           ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Backend │→│   AI   │→│Frontend│→│ Polish │
└────────┘ └────────┘ └────────┘ └────────┘
  Sim                               
```

---

## Team

1 developer can complete this in 8 weeks.

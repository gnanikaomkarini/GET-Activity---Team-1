# Implementation Roadmap

## Overview

Python-only stack. Simple and minimal.

---

## Phase 1: Foundation (Weeks 1-2)

**Goal:** Working app with simulation

### Week 1: Backend + Database
- [ ] Set up FastAPI project
- [ ] Create database models (users, devices, readings)
- [ ] Implement JWT auth
- [ ] Basic CRUD endpoints

### Week 2: Simulator + API
- [ ] Build device simulator
- [ ] Time-of-day patterns
- [ ] CRUD endpoints for devices
- [ ] Reading ingestion endpoint

**Deliverable:** API with working simulation.

---

## Phase 2: Intelligence (Weeks 3-4)

**Goal:** AI features

### Week 3: ML Models
- [ ] Forecasting (simple LSTM or statistical)
- [ ] Anomaly detection (Isolation Forest)
- [ ] Recommendation engine (rule-based)

### Week 4: Integration
- [ ] Connect ML to API
- [ ] Alert system
- [ ] Recommendation generation

**Deliverable:** AI-powered insights.

---

## Phase 3: Frontend (Weeks 5-6)

**Goal:** Dashboard

- [ ] Simple HTML/JS dashboard
- [ ] Energy charts (Chart.js)
- [ ] Device management UI
- [ ] Recommendation display

**Deliverable:** Working dashboard.

---

## Phase 4: Polish (Weeks 7-8)

**Goal:** Launch-ready

- [ ] Add scenarios (heating, cooling, vacation)
- [ ] Gamification (energy score, badges)
- [ ] Cost estimation
- [ ] Documentation

**Deliverable:** Ready to use.

---

## Timeline

```
Week 1-2    Week 3-4    Week 5-6    Week 7-8
    │           │           │           │
    ▼           ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Backend │→│   ML   │→│Frontend│→│ Polish │
└────────┘ └────────┘ └────────┘ └────────┘
```

---

## Team

1 developer can complete this in 8 weeks.

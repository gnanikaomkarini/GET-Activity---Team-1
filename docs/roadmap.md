# Implementation Roadmap

## Overview

Python + Puter.js (Claude AI). Simple 4-week build.

---

## Phase 1: Foundation (Week 1)

**Goal:** Working simulation

- [ ] Set up FastAPI project
- [ ] Create database models (devices, readings)
- [ ] Build simulator engine
- [ ] Device CRUD endpoints
- [ ] Reading generation

---

## Phase 2: AI Integration (Week 2)

**Goal:** Claude-powered analysis

- [ ] Frontend with Puter.js
- [ ] Call Claude with energy data
- [ ] Parse JSON response
- [ ] Display analysis

---

## Phase 3: Caching (Week 3)

**Goal:** Efficient AI usage

- [ ] Add Analysis model
- [ ] Hash readings
- [ ] Cache results
- [ ] Return cached when same data

---

## Phase 4: Polish (Week 4)

**Goal:** Launch-ready

- [ ] Dashboard UI
- [ ] Scenarios
- [ ] Energy score
- [ ] Documentation

---

## Timeline

```
Week 1      Week 2      Week 3      Week 4
   │           │           │           │
   ▼           ▼           ▼           ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Backend │→│   AI   │→│ Caching│→│ Polish │
└────────┘ └────────┘ └────────┘ └────────┘
  Sim                              
```

---

## Team

1 developer can complete in 4 weeks.

# Technology Stack

## Overview

Simulation-only stack. No physical IoT devices or real-world protocols.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                          │
│  React 18 + TypeScript + Tailwind + Recharts        │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│                    BACKEND                           │
│  Node.js/Fastify  │  Python/FastAPI                  │
│  Prisma ORM       │  SQLAlchemy                       │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│                  SIMULATOR + ML                      │
│  Python: Simulation Engine, ML Models                 │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│                    DATA LAYER                        │
│  PostgreSQL + TimescaleDB + Redis                    │
└─────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Frontend

| Layer | Technology | Notes |
|-------|------------|-------|
| Framework | React 18+ or Next.js 14 | SPA or SSR |
| Language | TypeScript | Type safety |
| State | Zustand | Lightweight |
| UI | Tailwind CSS + shadcn/ui | Customizable |
| Charts | Recharts | Energy visualizations |
| Forms | React Hook Form + Zod | Validation |
| HTTP | Axios | API calls |
| Auth | JWT (self-hosted) or Clerk | Authentication |

### Backend

| Layer | Technology | Notes |
|-------|------------|-------|
| Runtime | Node.js 20+ or Python 3.11 | Choose one |
| API | Fastify (Node) or FastAPI (Python) | Fast, typed |
| ORM | Prisma (Node) or SQLAlchemy (Python) | Database access |
| Validation | Zod (Node) or Pydantic (Python) | Runtime types |
| Queue | BullMQ or Celery | Background jobs |
| Cache | Redis 7+ | Sessions, rate limit |

### Simulator Engine

| Layer | Technology | Notes |
|-------|------------|-------|
| Core | Python 3.11+ | Pattern generation |
| Data | NumPy + Pandas | Efficient computation |
| Scheduling | APScheduler | Real-time simulation |
| Config | JSON/YAML | Scenario definitions |

### ML Services

| Layer | Technology | Notes |
|-------|------------|-------|
| Framework | PyTorch | Forecasting, anomaly detection |
| Training | MLflow | Experiment tracking |
| Serving | FastAPI | Model endpoints |
| Time Series | PyTorch Forecasting | Pre-built models |

### Data Storage

| Type | Technology | Use Case |
|------|------------|----------|
| Relational | PostgreSQL 15+ | Users, devices, settings |
| Time Series | TimescaleDB | Energy readings |
| Cache | Redis 7+ | Sessions, rate limits |
| Object | S3 or local | Exports, reports |

---

## ML Models

| Model | Algorithm | Purpose |
|-------|-----------|---------|
| Forecasting | LSTM, XGBoost | Predict future consumption |
| Anomaly | Isolation Forest | Detect unusual patterns |
| Recommendations | Rule-based + ML | Generate energy tips |

---

## Infrastructure

| Category | Technology | Notes |
|----------|------------|-------|
| Container | Docker + Docker Compose | Local dev |
| CI/CD | GitHub Actions | Auto deploy |
| Monitoring | Prometheus + Grafana | Optional for MVP |
| Hosting | Railway, Render, Vercel | Simple deployment |

---

## Quick Start (MVP)

```
Frontend:  Next.js 14 (Vercel)
Backend:   Next.js API Routes
Database:  PostgreSQL (Supabase/Neon)
Simulator: Python + FastAPI (Railway)
Auth:      Clerk
Hosting:   Vercel + Railway
```

---

## Cost Estimate (1000 users/month)

| Component | Cost |
|-----------|------|
| Compute | $50-100 |
| Database | $20-50 |
| Cache | $10-20 |
| Storage | $10-20 |
| **Total** | **$90-190** |

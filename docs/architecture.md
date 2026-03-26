# System Architecture

## Overview

This is a **simulation-only** architecture. All IoT devices are virtual and data is generated programmatically. No physical hardware or real-world IoT protocols are used.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                      │
│  │   Web App   │  │  Dashboard  │  │   Widget    │                      │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                      │
└─────────┼────────────────┼────────────────┼───────────────────────────────┘
          │                │                │
          └────────────────┴────────────────┘
                             │
                       API Gateway
                       (Auth, Rate Limit)
                             │
┌────────────────────────────┼─────────────────────────────────────────────┐
│                      SERVICES LAYER                                      │
│                                                                            │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │  User Service    │  │  Energy Service  │  │  Recommendation   │      │
│  │  - Auth          │  │  - Data Storage  │  │    Service       │      │
│  │  - Profiles      │  │  - Forecasting   │  │  - ML Models     │      │
│  │  - Preferences   │  │  - Analytics     │  │  - Tips Engine   │      │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘      │
│                                                                            │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │ Simulator Service│  │  Alert Service   │  │  Gamification    │      │
│  │  - Device Sim    │  │  - Notifications │  │    Service       │      │
│  │  - Scenarios     │  │  - Alerts        │  │  - Challenges    │      │
│  │  - Data Gen      │  │                  │  │  - Achievements  │      │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘      │
│                                                                            │
└────────────────────────────┼─────────────────────────────────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────────────────────┐
│                        DATA LAYER                                         │
│                                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                   │
│  │   PostgreSQL │  │   TimescaleDB │  │    Redis     │                   │
│  │  (Users/Dev) │  │  (Time Series)│  │   (Cache)    │                   │
│  └──────────────┘  └──────────────┘  └──────────────┘                   │
│                                                                            │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     ML/AI Infrastructure                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │    │
│  │  │ Forecasting │  │  Anomaly    │  │Recommendation│             │    │
│  │  │   Model     │  │  Detector   │  │    Engine    │             │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘             │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Simulator Service

The central component that generates all energy data virtually.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Simulator Service                                   │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      Device Factory                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │
│  │  │Virtual   │  │Virtual   │  │Virtual   │  │Virtual   │       │   │
│  │  │Smart     │  │Thermo-   │  │Smart     │  │Energy    │       │   │
│  │  │Meter     │  │stat      │  │Plugs     │  │Monitor   │       │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Pattern Engine                                 │   │
│  │  - Time-of-day patterns                                          │   │
│  │  - Day-of-week variations                                        │   │
│  │  - Seasonal adjustments                                           │   │
│  │  - Weather correlation                                           │   │
│  │  - Occupancy simulation                                          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Scenario Manager                               │   │
│  │  - Preset scenarios (heating, cooling, vacation)                 │   │
│  │  - Custom scenario configuration                                 │   │
│  │  - Anomaly injection                                            │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

**Simulation Modes:**
| Mode | Description |
|------|-------------|
| Real-time | Generate readings at configurable intervals (1s-1h) |
| Batch | Generate historical data for specified date range |
| Scenario | Run predefined or custom consumption scenario |

### 2. Data Generation Patterns

**Time-of-Day Pattern:**
```
12am ─────────────────────────────────────────── 12am
       │     │           │        │     │
       │     │           │        │     │
   Night    Morning    Midday   Evening  Night
   (Low)   (Rising)   (Peak)   (High)  (Low)
```

**Weekday vs Weekend:**
```
Weekday: Higher morning/evening peaks, daytime work hours
Weekend: Distributed usage, afternoon peak
```

**Seasonal Adjustment:**
```
Winter: +20-40% HVAC, +lighting
Summer: +30-50% AC
Spring/Fall: Baseline
```

### 3. ML Services

```
┌─────────────────────────────────────────────────────────────────┐
│                       ML Pipeline                                 │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Forecasting │    │   Anomaly    │    │Recommendation│      │
│  │    Model    │    │   Detector   │    │    Engine    │      │
│  │   (LSTM)    │    │ (Isolation  │    │ (Rule-based  │      │
│  │             │    │   Forest)   │    │  + ML)       │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │               │
│         └───────────────────┴───────────────────┘               │
│                             │                                   │
│                    ┌────────┴────────┐                        │
│                    │  Recommendation │                        │
│                    │    Router       │                        │
│                    └─────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

### 4. API Gateway

- JWT authentication
- Rate limiting (requests per minute)
- Request validation (Zod schemas)
- API versioning (/api/v1, /api/v2)
- OpenAPI documentation

---

## Data Models

### User
```typescript
interface User {
  id: string;
  email: string;
  name: string;
  tariffPlan: 'flat' | 'time-of-use' | 'tiered';
  preferences: {
    units: 'metric' | 'imperial';
    notifications: boolean;
    currency: string;
  };
}
```

### Simulated Device
```typescript
interface SimulatedDevice {
  id: string;
  userId: string;
  type: 'smart_meter' | 'thermostat' | 'plug' | 'energy_monitor';
  name: string;
  location: string;
  parameters: {
    // Smart Meter
    homeSize?: number; // sq ft
    occupancy?: number;
    
    // Thermostat
    mode?: 'heat' | 'cool' | 'auto' | 'off';
    setpoint?: number;
    schedule?: Schedule[];
    
    // Smart Plug
    applianceType?: string;
    wattage?: number;
    
    // Energy Monitor
    circuits?: number;
  };
  status: 'active' | 'paused';
}
```

### Energy Reading
```typescript
interface EnergyReading {
  deviceId: string;
  timestamp: Date;
  powerWatts: number;
  energyKwh: number;
  voltage?: number;
  current?: number;
  metadata: {
    source: 'simulated';
    scenario?: string;
  };
}
```

### Recommendation
```typescript
interface Recommendation {
  id: string;
  userId: string;
  type: 'behavioral' | 'timing' | 'settings' | 'pattern';
  title: string;
  description: string;
  estimatedSavingsKwh: number;
  estimatedSavingsCurrency: number;
  confidenceScore: number;
  effortLevel: 'low' | 'medium' | 'high';
  actions: string[];
}
```

### Scenario
```typescript
interface Scenario {
  id: string;
  name: string;
  description: string;
  duration: 'hourly' | 'daily' | 'weekly';
  config: {
    consumptionMultiplier: number;
    peakHours: [number, number];
    anomalyType?: 'spike' | 'drop' | 'gradual';
    anomalyMagnitude?: number;
  };
}
```

---

## Security

| Layer | Implementation |
|-------|----------------|
| Authentication | JWT with refresh tokens |
| Authorization | Role-based (owner, viewer) |
| Data | Encryption at rest, TLS in transit |
| API | Rate limiting, input validation |
| Storage | Isolated per-user data |

---

## Scalability

| Component | Approach |
|-----------|----------|
| API | Horizontal scaling (stateless) |
| Database | Connection pooling, read replicas |
| Cache | Redis with TTL, invalidation |
| Simulation | Background workers, job queue |
| ML | Batch inference, model caching |

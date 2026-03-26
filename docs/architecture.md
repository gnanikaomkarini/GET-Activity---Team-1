# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT LAYER                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   Web App   │  │  Mobile App │  │  Dashboard  │  │   Widget    │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
└─────────┼────────────────┼────────────────┼────────────────┼───────────┘
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                    │
                              API Gateway
                              (Rate Limiting, Auth)
                                    │
┌───────────────────────────────────┼─────────────────────────────────────┐
│                           SERVICES LAYER                                 │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │  User Service    │  │  Energy Service  │  │  Recommendation  │      │
│  │  - Auth/Auth     │  │  - Data Ingestion│  │    Service       │      │
│  │  - Profiles      │  │  - Analytics     │  │  - ML Models     │      │
│  │  - Preferences   │  │  - Forecasting   │  │  - Tips Engine   │      │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘      │
│                                                                          │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │  Device Service  │  │  Alert Service   │  │  Gamification    │      │
│  │  - IoT Devices  │  │  - Notifications │  │    Service       │      │
│  │  - Schedules    │  │  - Alerts        │  │  - Challenges    │      │
│  │  - Control      │  │  - Reports       │  │  - Achievements  │      │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘      │
│                                                                          │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
┌───────────────────────────────────┼─────────────────────────────────────┐
│                           DATA LAYER                                     │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │   PostgreSQL │  │   TimescaleDB │  │    Redis     │  │    S3/MinIO│  │
│  │  (Users/Dev) │  │  (Time Series)│  │   (Cache)    │  │  (Models)  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     ML/AI Infrastructure                         │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │    │
│  │  │ Feature Store│  │ Model Reg. │  │  Training   │               │    │
│  │  │             │  │             │  │  Pipeline   │               │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘               │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Data Ingestion Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Simulated IoT Device Layer                          │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    IoT Simulator Service                         │   │
│  │                                                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │Virtual   │  │Virtual   │  │Virtual   │  │Virtual   │        │   │
│  │  │Smart     │  │Thermo-   │  │Smart     │  │Energy    │        │   │
│  │  │Meter     │  │stat      │  │Plugs     │  │Monitor   │        │   │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │   │
│  │       │             │             │             │                │   │
│  │       └─────────────┴─────────────┴─────────────┘                │   │
│  │                           │                                      │   │
│  │                    Data Generator                                │   │
│  │                    (Realistic patterns)                          │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
Smart Meters → MQTT Broker → Kafka → Stream Processing → Time Series DB
                    ↓
              IoT Devices → REST API → Message Queue → Processing
```

**Components:**
- **IoT Simulator**: Generates realistic energy data for virtual devices
- **MQTT Broker** (Mosquitto/EMQX): Handles IoT device connections
- **Apache Kafka**: Message streaming for high-volume data
- **Apache Flink/Spark Streaming**: Real-time stream processing
- **TimescaleDB**: Optimized for time-series data storage

### 1b. IoT Device Simulator

The simulator mimics real-world IoT devices for testing and demonstration without physical hardware.

**Simulated Device Types:**
| Device | Parameters | Generated Data |
|--------|------------|----------------|
| Smart Meter | Location, tariff type | kWh readings, voltage, current |
| Smart Thermostat | Mode, setpoint, location | Temperature, humidity, HVAC cycles |
| Smart Plugs | Connected appliance type | Power (W), energy (kWh), state |
| Energy Monitor | Main panel, circuit count | Per-circuit power, total consumption |

**Simulation Features:**
- Time-of-day usage patterns (realistic behavioral patterns)
- Day-of-week variations (weekday vs weekend)
- Seasonal variations (heating/cooling seasons)
- Random anomalies (equipment issues, unusual usage)
- Weather correlation (temperature-based HVAC demand)
- Occupancy simulation (home/away patterns)

**Data Generation Strategy:**
```
User Profile + Time Context + Weather → Simulated Device Behavior
                                    ↓
                              Energy Readings
                                    ↓
                              Stored in DB
```

**API Endpoints for Simulation:**
```
POST   /api/simulator/devices          - Create simulated device
GET    /api/simulator/devices/:id       - Get device state
PUT    /api/simulator/devices/:id       - Update device parameters
POST   /api/simulator/devices/:id/control - Send control command
DELETE /api/simulator/devices/:id       - Remove device
POST   /api/simulator/generate          - Generate historical data
POST   /api/simulator/scenario          - Run preset scenario
```

### 2. ML Recommendation Engine

```
┌─────────────────────────────────────────────────────────────────┐
│                      Recommendation Pipeline                      │
│                                                                  │
│  User Context ──┐                                               │
│  Device Data ────┼──→ Feature Engineering ──→ ML Model ──→ Tips│
│  Weather Data ───┘                     │                        │
│  Historical ────┐                     ▼                        │
│                  │            Personalization Layer              │
│                  └──────────→ Priority Scoring                   │
└─────────────────────────────────────────────────────────────────┘
```

**Models:**
- **Consumption Forecasting**: LSTM/Transformer for usage prediction
- **Anomaly Detection**: Isolation Forest/Autoencoder for unusual patterns
- **Recommendation Engine**: Collaborative filtering + Content-based
- **Optimal Timing**: Reinforcement learning for best action times

### 3. API Gateway

- Authentication (JWT, OAuth2)
- Rate limiting and throttling
- Request validation
- Load balancing
- API versioning

### 4. Notification System

```
Event Trigger → Message Queue → Push/Fetch → User
                    ↓
              Email/SMS → SMTP/SMS Gateway
```

## Data Models

### User Profile
```
User {
  id: UUID
  email: string
  name: string
  location: GeoLocation
  utility_provider: string
  tariff_plan: string
  preferences: JSON
  goals: JSON
}
```

### Device
```
Device {
  id: UUID
  user_id: UUID
  type: enum (smart_meter, thermostat, plug, light, appliance)
  manufacturer: string
  model: string
  location: string
  capabilities: JSON
  status: enum (online, offline, error)
}
```

### Energy Reading
```
EnergyReading {
  device_id: UUID
  timestamp: DateTime
  power_watts: float
  energy_kwh: float
  voltage: float
  current: float
  metadata: JSON
}
```

### Recommendation
```
Recommendation {
  id: UUID
  user_id: UUID
  type: enum (behavioral, upgrade, automation, tariff)
  title: string
  description: string
  estimated_savings_kwh: float
  estimated_savings_currency: float
  confidence_score: float
  priority: int
  actions: JSON
  created_at: DateTime
  expires_at: DateTime
}
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Security Layers                          │
│                                                                  │
│  1. Network Security                                            │
│     - VPC/Private Subnets                                       │
│     - WAF (Web Application Firewall)                            │
│     - DDoS Protection                                           │
│                                                                  │
│  2. Application Security                                        │
│     - OAuth 2.0 / OpenID Connect                               │
│     - JWT with refresh tokens                                   │
│     - API key management                                        │
│     - Input validation & sanitization                           │
│                                                                  │
│  3. Data Security                                               │
│     - Encryption at rest (AES-256)                              │
│     - Encryption in transit (TLS 1.3)                           │
│     - PII anonymization                                         │
│     - Audit logging                                             │
│                                                                  │
│  4. Compliance                                                  │
│     - GDPR compliance                                           │
│     - Energy data privacy                                       │
│     - SOC 2 readiness                                           │
└─────────────────────────────────────────────────────────────────┘
```

## Scalability Considerations

| Component | Strategy |
|-----------|----------|
| API Servers | Horizontal scaling with auto-scaling groups |
| Database | Read replicas, sharding for time-series data |
| Caching | Redis cluster with automatic failover |
| ML Inference | GPU instances, model quantization, batch processing |
| Message Queue | Kafka cluster with partitioning |

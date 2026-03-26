# Features Specification

## Overview

This is a **simulation-only** AI Energy Efficiency Advisor. All features work with simulated/virtual IoT devices. No physical hardware required.

---

## Core Features

### 1. IoT Device Simulator

**Description**: Built-in engine for creating and managing virtual IoT devices that generate realistic energy data.

**Simulated Device Types:**

| Device | Generates | Configurable Parameters |
|--------|-----------|------------------------|
| Smart Meter | kWh readings, voltage, current | Location, home size, occupancy |
| Thermostat | Temperature, humidity, HVAC cycles | Mode, setpoint, schedule |
| Smart Plugs | Power (W), energy (kWh), on/off state | Appliance type, usage patterns |
| Energy Monitor | Per-circuit power, total consumption | Circuit count, main panel |

**Simulation Capabilities:**
- Realistic time-of-day usage patterns
- Day-of-week variations (weekday vs weekend)
- Seasonal variations (heating/cooling seasons)
- Random anomalies (equipment issues, unusual usage)
- Weather correlation (temperature-based HVAC demand)
- Occupancy simulation (home/away patterns)

**Data Generation:**
```
User Profile + Time Context + Weather → Simulated Readings
```

---

### 2. Energy Dashboard

**Description**: Real-time visualization of simulated energy consumption.

**Features:**
- Live power consumption display (watts/kWh)
- Historical charts (daily, weekly, monthly)
- Comparison with previous periods
- Cost projection based on tariff rates
- Carbon footprint estimation

**Visualizations:**
- Line charts for trends
- Pie charts for device breakdown
- Heat maps for time-of-day usage
- Gauge meters for current consumption

---

### 3. Scenario Runner

**Description**: Execute preset or custom scenarios to simulate different energy situations.

**Preset Scenarios:**

| Scenario | Behavior |
|----------|----------|
| Normal Usage | Baseline consumption patterns |
| High Consumption | Elevated usage to test detection |
| Seasonal Heating | Winter HVAC patterns |
| Seasonal Cooling | Summer AC patterns |
| Weekend Pattern | Different from weekday usage |
| Vacation Mode | Extended absence simulation |
| Gradual Increase | Slowly growing consumption |
| Anomaly Spike | Sudden consumption spike |
| Anomaly Drop | Unexpected consumption drop |
| Peak Demand | Time-of-use peak period |

**Custom Scenarios:**
- Define custom patterns via JSON configuration
- Adjust time ranges, intensity, and device involvement
- Inject specific anomalies at defined times

---

### 4. AI-Powered Recommendations

**Description**: Intelligent suggestions based on simulated consumption patterns.

**Recommendation Types:**

| Type | Example |
|------|---------|
| Behavioral | "AC runs 4+ hours while simulated occupancy is away" |
| Timing | "Shift dishwasher to after 9 PM for off-peak savings" |
| Settings | "Raising thermostat 2°F during sleep saves $45/month" |
| Pattern | "Weekend usage is 40% higher than weekdays" |

**Properties:**
- Estimated savings (kWh and currency)
- Confidence score
- Effort level (Low/Medium/High)
- Action steps

---

### 5. Load Forecasting

**Description**: Predict future energy consumption based on simulated data patterns.

**Capabilities:**
- 24-hour ahead forecast
- 7-day forecast with seasonal patterns
- Monthly trend prediction
- Peak demand warnings

**Models:**
- LSTM neural networks
- Gradient boosting (XGBoost)
- Weather-correlated predictions

---

### 6. Anomaly Detection

**Description**: Identify unusual patterns in simulated energy data.

**Detection Types:**
| Anomaly | Pattern |
|---------|---------|
| Spike | Sudden increase in consumption |
| Drop | Unexpected decrease |
| Gradual Change | Slow increase/decrease over time |
| Time Shift | Usage at unusual times |
| Pattern Break | Deviation from typical patterns |

**Features:**
- Real-time anomaly alerts
- Historical anomaly review
- Configurable sensitivity thresholds
- Anomaly explanation and root cause

---

### 7. Alerts & Notifications

**Description**: Notifications for important simulation events.

**Alert Types:**
| Category | Examples |
|----------|----------|
| Usage Alerts | "Daily consumption is 40% higher than average" |
| Cost Alerts | "Projected to exceed $150 monthly budget" |
| Anomaly Alerts | "Unusual spike detected - 3x normal consumption" |
| Savings Alerts | "You saved $25 this week!" |
| Forecast Alerts | "Peak demand expected tomorrow afternoon" |

**Delivery:**
- In-app notifications
- Email digest (optional)
- Webhook notifications (for integration)

---

### 8. Gamification

**Description**: Make simulation-based learning engaging.

**Features:**
- Energy Score (0-100)
- Achievement badges
- Savings challenges
- Comparison with simulated benchmarks
- Streak tracking

**Badges:**
| Badge | Earned By |
|-------|-----------|
| Early Bird | Shift usage to off-peak hours |
| Consistency | Maintain stable usage for 7 days |
| Saver | Achieve weekly savings target |
| Investigator | Review 10 anomaly explanations |

---

### 9. Cost Analysis

**Description**: Detailed breakdown of simulated energy costs.

**Features:**
- Current bill estimation
- Historical cost comparison
- Tariff rate simulation (flat, time-of-use, tiered)
- Budget tracking and alerts
- Cost forecast

---

### 10. API

**Description**: REST API for programmatic access to simulation.

**Endpoints:**

| Category | Endpoints |
|----------|-----------|
| Devices | POST/GET/PUT/DELETE /devices |
| Readings | POST /readings, GET /readings/history |
| Simulation | POST /simulate/start, /simulate/stop, /simulate/scenario |
| Recommendations | GET /recommendations |
| Forecasts | GET /forecast |
| Alerts | GET /alerts |

---

## User Management

### User Preferences
- Custom tariff rates
- Notification preferences
- Display units (metric/imperial)
- Theme (light/dark mode)

### Multi-User Support
- Multiple simulated properties per user
- User roles (owner, viewer)

---

## Pricing Tiers

| Feature | Free | Pro |
|---------|------|-----|
| Simulated Devices | 5 | Unlimited |
| Historical Data | 30 days | 2 years |
| Recommendations | 10/month | Unlimited |
| Scenarios | Preset only | Custom |
| API Access | No | Yes |
| Alerts | 10/day | Unlimited |

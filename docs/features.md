# Features Specification

## Overview

Simulation-only AI Energy Advisor powered by **Claude AI** (via Puter.js). No API keys required.

---

## Core Features

### 1. IoT Device Simulator

**Description**: Creates virtual devices that generate realistic energy data.

**Simulated Device Types:**

| Device | Generates |
|--------|-----------|
| Smart Meter | kWh readings, voltage, current |
| Thermostat | Temperature, HVAC cycles |
| Smart Plugs | Power (W), energy (kWh), on/off |
| Energy Monitor | Per-circuit power, total |

**Simulation Patterns:**
- Time-of-day (low at night, peaks morning/evening)
- Weekday vs weekend
- Seasonal adjustments
- Random variations

---

### 2. Energy Dashboard

**Description**: Visualize simulated energy consumption.

**Features:**
- Average power (watts)
- Daily usage (kWh)
- Estimated monthly cost
- Energy score/grade
- Usage chart

---

### 3. AI-Powered Analysis (Claude)

**Description**: Single AI call returns complete analysis.

**Returns:**
```json
{
  "summary": { "avg_power", "peak_power", "daily_kwh", "monthly_cost" },
  "forecast": { "projected_monthly_kwh", "trend", "confidence" },
  "anomalies": [{ "type", "description", "cause", "recommendation" }],
  "recommendations": [{ "title", "description", "savings", "actions", "priority" }],
  "score": { "value", "grade", "breakdown" }
}
```

**How:**
1. Frontend gets readings from backend
2. Frontend calls `puter.ai.chat()` with data
3. Claude returns JSON analysis
4. Frontend POSTs to backend for caching

---

### 4. Caching System

**Description**: Avoid redundant AI calls.

**How:**
- Readings hashed (md5)
- Same hash = cached analysis returned
- Different readings = new AI call

**Benefits:**
- Faster responses
- Reduced AI usage
- Consistent results for same data

---

### 5. Scenarios

**Description**: Test different energy situations.

| Scenario | Effect |
|----------|--------|
| Normal Usage | Baseline patterns |
| Winter Heating | Higher consumption |
| Summer Cooling | Peak AC usage |
| Vacation Mode | Minimal usage |
| High Consumption | Elevated baseline |
| Anomaly Spike | Sudden spike |
| Anomaly Drop | Sudden drop |

---

### 6. Recommendations

**Description**: Personalized tips from Claude.

**Types:**
| Type | Example |
|------|---------|
| Behavioral | "Turn off lights when leaving" |
| Timing | "Run appliances after 9 PM" |
| Settings | "Adjust thermostat 2°F" |

**Each includes:**
- Estimated kWh savings
- Estimated cost savings
- Action steps
- Priority (high/medium/low)

---

### 7. Energy Score

**Description**: Grade your energy efficiency.

**Grade Scale:**
- A: 85-100 (Excellent)
- B: 70-84 (Good)
- C: 55-69 (Average)
- D: 40-54 (Below Average)
- F: 0-39 (Poor)

---

## User Flow

```
1. Add Device → "Living Room Meter"
2. Generate Data → Creates 96 readings
3. AI Analyzes → Claude returns analysis
4. View Dashboard → Shows stats + recommendations
5. Run Scenario → "Heating" → New readings → AI re-analyzes
6. Cache Hit → Same data returns cached results
```

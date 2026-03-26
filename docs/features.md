# Features Specification

## Overview

Simulation-only AI Energy Advisor. All features powered by AI (LLM).

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

**Simulation Capabilities:**
- Realistic time-of-day patterns
- Day-of-week variations
- Seasonal adjustments
- Random anomalies

---

### 2. Energy Dashboard

**Description**: Visualize simulated energy consumption.

**Features:**
- Live power consumption display
- Historical charts (daily, weekly, monthly)
- Cost projection
- Device breakdown

---

### 3. AI-Powered Recommendations

**Description**: The AI analyzes your energy data and generates personalized tips.

**How It Works:**
```
Your Data → AI Analysis → Personalized Recommendations
```

**Example Recommendations:**
| Situation | AI Recommendation |
|-----------|-------------------|
| High AC usage | "Your AC runs 40% more than similar homes. Try raising the thermostat 2°F or using a fan." |
| Peak hours usage | "40% of your energy is used during peak hours (2-7 PM). Running appliances after 9 PM saves ~$25/month." |
| Standby power | "Devices in standby cost you $15/month. Unplugging chargers and electronics when not in use saves $180/year." |

**Features:**
- Daily personalized tips
- Context-aware suggestions
- Estimated savings for each tip
- One-click actions

---

### 4. AI Anomaly Detection

**Description**: AI explains unusual patterns in your energy data.

**Anomaly Types:**
- Spike (sudden increase)
- Drop (unexpected decrease)
- Pattern break

**AI Explanation Example:**
> "Your energy usage tripled on Tuesday between 2-4 PM. This coincides with running the electric dryer and oven simultaneously. Consider staggering high-power appliances."

---

### 5. AI Forecasting

**Description**: AI predicts future consumption and explains trends.

**Features:**
- 7-day forecast
- Monthly bill projection
- Trend explanations
- "What if" scenarios

**Example:**
> "Based on your patterns, you're on track to spend $220 this month (up from $185 last month). The increase is due to higher AC usage during the heatwave. Running AC 2 hours less daily would save ~$35."

---

### 6. AI Chat

**Description**: Ask questions about your energy usage in plain English.

**Examples:**
- "Why is my bill so high this month?"
- "How can I reduce energy in my home office?"
- "What appliances use the most energy?"
- "Compare my usage to last month"

---

### 7. Scenario Runner

**Description**: Test different energy situations.

**Scenarios:**
| Scenario | Effect |
|----------|--------|
| Normal Usage | Baseline patterns |
| High Consumption | Elevated usage |
| Seasonal Heating | Winter HVAC |
| Seasonal Cooling | Summer AC |
| Vacation Mode | Reduced usage |
| Anomaly Spike | Sudden spike |

---

### 8. Cost Analysis

**Description**: Track simulated energy costs.

**Features:**
- Bill estimation
- Historical comparison
- Tariff simulation (flat, time-of-use)
- Budget alerts

---

### 9. Gamification

**Description**: Stay motivated to save energy.

**Features:**
- Energy Score (AI-evaluated)
- Achievement badges
- Savings challenges
- Streak tracking

---

## User Management

### Preferences
- Tariff rates
- Notification settings
- Display units

### Multi-Property
- Multiple simulated homes
- Consolidated view

---

## Pricing Tiers

| Feature | Free | Pro |
|---------|------|-----|
| Simulated Devices | 5 | Unlimited |
| AI Recommendations | 20/month | Unlimited |
| AI Chat | No | Yes |
| Historical Data | 30 days | 1 year |
| Scenarios | Preset only | Custom |

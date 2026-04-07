# Features Specification

## Overview

AI Energy Advisor powered by **Google Gemini AI**. Analyzes household appliances and provides personalized recommendations to reduce energy consumption.

---

## Core Features

### 1. Appliance Input

**Description**: Select and configure household appliances.

**Supported Appliances:**
| Appliance | Icon | Typical Wattage |
|-----------|------|-----------------|
| Lights | 💡 | 15W |
| Air Conditioning | ❄️ | 3500W |
| Water Heater | 🚿 | 4500W |
| Refrigerator | 🧊 | 150W |
| Washing Machine | 👕 | 500W |
| Dryer | 👔 | 3000W |
| Dishwasher | 🍽️ | 1800W |
| Microwave | 📦 | 1200W |
| TV | 📺 | 100W |
| Computer | 💻 | 200W |
| Phone Chargers | 📱 | 10W |
| Fans | 🌀 | 75W |
| Stove/Oven | 🍳 | 2500W |
| WiFi Router | 📡 | 15W |
| Gaming Console | 🎮 | 150W |
| Iron | 👔 | 1100W |
| Vacuum Cleaner | 🧹 | 1400W |
| Coffee Maker | ☕ | 800W |

**For each appliance:**
- Number of units
- Usage presets: Off / Light / Normal / Heavy / Custom hours

---

### 2. Household Info

**Description**: Basic household context.

**Fields:**
- Number of occupants
- Location (city, country)

---

### 3. Additional Context

**Description**: User-provided context for personalized advice.

**Examples:**
- "Work from home 3 days a week"
- "Have elderly parents visiting"
- "Pool pump runs 6 hours daily"
- "Live in hot climate zone"

---

### 4. AI Analysis (Gemini)

**Description**: Single AI call returns complete analysis.

**Returns:**
```json
{
  "summary": { 
    "totalMonthlyKwh": 450,
    "largestConsumer": "Air Conditioning",
    "comparisonToAverage": "20% above average"
  },
  "wasteAnalysis": [{ "appliance", "issue", "monthlyWasteKwh" }],
  "savingTips": [{ "appliance", "tip", "potentialMonthlyKwh", "difficulty" }],
  "recommendations": [{ "title", "description", "impact", "actionSteps" }],
  "estimatedAfterSavings": { "monthlyKwh", "percentReduction" }
}
```

**How:**
1. App constructs prompt with appliance data
2. Prompt sent to Gemini API
3. AI returns JSON analysis
4. Results displayed to user

---

### 5. Results Display

**Description**: Shows analysis results.

**Sections:**
- Summary (total kWh, biggest consumer)
- Waste Analysis (where energy is wasted)
- Saving Tips (specific advice per appliance)
- Recommendations (high/medium/low impact)
- After-Savings Estimate (projected usage + reduction %)

---

## User Flow

```
1. Fill Household Info → "4 occupants, Mumbai"
2. Select Appliances → "10 lights, 2 ACs, 1 fridge..."
3. Set Usage → "Normal (8h/day)" for each
4. Add Context → "Work from home"
5. Click Analyze → Gemini returns recommendations
6. View Results → See waste, tips, and savings
```

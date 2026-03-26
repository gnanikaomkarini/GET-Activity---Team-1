import os
import json
from typing import List, Dict, Optional
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

SYSTEM_PROMPT = """You are an energy efficiency advisor. Analyze the user's energy data and provide personalized, actionable recommendations to help them save energy and reduce their electricity bills.

Always be specific, practical, and helpful. Include estimated savings when possible.
"""


def generate_recommendations(user_data: Dict, readings: List[Dict]) -> List[Dict]:
    if not readings:
        return _default_recommendations()

    prompt = f"""Based on the following energy data for a user, suggest 3-5 specific, actionable recommendations to reduce energy consumption and save money.

User Profile:
- Home size: {user_data.get("home_size", "unknown")} sq ft
- Number of occupants: {user_data.get("occupancy", "unknown")}

Recent Energy Data Summary:
- Average power consumption: {sum(r.get("power_watts", 0) for r in readings[-48:]) / len(readings[-48:]):.0f} watts
- Peak consumption: {max(r.get("power_watts", 0) for r in readings[-48:]):.0f} watts
- Latest reading: {readings[-1].get("power_watts", 0):.0f} watts

Provide recommendations in JSON format:
{{
  "recommendations": [
    {{
      "type": "behavioral|timing|settings",
      "title": "Short title",
      "description": "Detailed explanation",
      "estimated_savings_kwh": number,
      "estimated_savings_currency": number,
      "confidence_score": 0.0-1.0,
      "actions": ["action1", "action2"]
    }}
  ]
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )

        result = json.loads(response.choices[0].message.content)
        return result.get("recommendations", _default_recommendations())
    except Exception as e:
        print(f"AI Error: {e}")
        return _default_recommendations()


def explain_anomaly(anomaly_data: Dict, context: Dict) -> str:
    prompt = f"""Explain this energy anomaly in simple, non-technical terms:

Anomaly Details:
- Type: {anomaly_data.get("type", "unknown")}
- Value: {anomaly_data.get("value", 0):.0f} watts
- Expected: {anomaly_data.get("expected", 0):.0f} watts
- Deviation: {anomaly_data.get("deviation", 0):.0f}%

Context:
- Device: {context.get("device_name", "unknown")}
- Time: {context.get("timestamp", "unknown")}

Provide a brief, friendly explanation of what likely happened and what the user can do about it.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You explain energy anomalies in a friendly, helpful way.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Energy spike detected: usage was {anomaly_data.get('deviation', 0):.0f}% above normal. This could be due to multiple appliances running simultaneously."


def generate_forecast(readings: List[Dict], user_data: Dict) -> Dict:
    if len(readings) < 10:
        return _default_forecast()

    recent_kwh = sum(r.get("energy_kwh", 0) for r in readings[-48:])
    projected_monthly = recent_kwh * 30

    prompt = f"""Based on this energy data, provide a forecast and bill estimate:

Current usage rate: {recent_kwh:.2f} kWh per day
Projected monthly: {projected_monthly:.0f} kWh
Location: {user_data.get("location", "unknown")}

Return JSON:
{{
  "forecast": {{
    "daily_average_kwh": number,
    "projected_monthly_kwh": number,
    "projected_monthly_cost": number,
    "trend": "increasing|decreasing|stable",
    "explanation": "brief text"
  }}
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You provide energy forecasts and bill projections.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )

        result = json.loads(response.choices[0].message.content)
        return result.get("forecast", _default_forecast())
    except Exception as e:
        return _default_forecast()


def chat(message: str, context: Dict) -> str:
    context_summary = f"""
User context:
- {len(context.get("devices", []))} devices
- Recent avg consumption: {context.get("avg_consumption", 0):.0f} watts
- Current bill estimate: ${context.get("bill_estimate", 0):.0f}/month
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + context_summary},
                {"role": "user", "content": message},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return "I'm having trouble connecting to my AI brain. Please try again."


def _default_recommendations() -> List[Dict]:
    return [
        {
            "type": "behavioral",
            "title": "Turn off lights when leaving rooms",
            "description": "Simple habit that can save $5-10 monthly",
            "estimated_savings_kwh": 15,
            "estimated_savings_currency": 2,
            "confidence_score": 0.9,
            "actions": [
                "Turn off lights when leaving",
                "Use natural light when possible",
            ],
        },
        {
            "type": "settings",
            "title": "Adjust thermostat by 2°F",
            "description": "Small temperature adjustments add up significantly",
            "estimated_savings_kwh": 50,
            "estimated_savings_currency": 8,
            "confidence_score": 0.85,
            "actions": ["Lower heat in winter", "Raise AC in summer when away"],
        },
        {
            "type": "timing",
            "title": "Use major appliances during off-peak hours",
            "description": "Running washer/dryer/dishwasher after 9 PM reduces strain on grid",
            "estimated_savings_kwh": 30,
            "estimated_savings_currency": 5,
            "confidence_score": 0.8,
            "actions": ["Run appliances after 9 PM", "Use delay start features"],
        },
    ]


def _default_forecast() -> Dict:
    return {
        "daily_average_kwh": 30,
        "projected_monthly_kwh": 900,
        "projected_monthly_cost": 120,
        "trend": "stable",
        "explanation": "Based on recent usage patterns",
    }

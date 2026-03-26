import os
import json
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

SYSTEM_PROMPT = """You are an energy efficiency advisor. Analyze the user's energy data and provide comprehensive insights.

Return a single JSON response with all the information the user needs.
"""


def analyze_energy(
    readings: List[Dict], device_name: str = "your home", tariff_rate: float = 0.12
) -> Dict:
    """
    Single AI call that returns:
    - summary: Overview of energy usage
    - forecast: 7-day projection
    - anomaly: Any detected anomalies
    - recommendations: Personalized tips
    """

    if not readings or len(readings) < 5:
        return _empty_response()

    recent_readings = readings[-48:] if len(readings) >= 48 else readings

    total_kwh = sum(r.get("energy_kwh", 0) for r in recent_readings)
    avg_power = sum(r.get("power_watts", 0) for r in recent_readings) / len(
        recent_readings
    )
    max_power = max(r.get("power_watts", 0) for r in recent_readings)
    min_power = min(r.get("power_watts", 0) for r in recent_readings)

    daily_kwh = total_kwh / (len(readings) / 48) if readings else 0
    projected_monthly_kwh = daily_kwh * 30
    projected_monthly_cost = projected_monthly_kwh * tariff_rate

    prompt = f"""Analyze this energy data and return a comprehensive analysis.

Device: {device_name}
Readings count: {len(readings)}

Usage Statistics:
- Average power: {avg_power:.0f} watts
- Peak power: {max_power:.0f} watts
- Min power: {min_power:.0f} watts
- Daily kWh: {daily_kwh:.1f}
- Projected monthly cost: ${projected_monthly_cost:.0f}

Return ONLY valid JSON (no markdown, no explanation):
{{
  "summary": {{
    "average_power_watts": number,
    "peak_power_watts": number,
    "daily_kwh": number,
    "monthly_cost_estimate": number,
    "description": "2-3 sentence overview of usage patterns"
  }},
  "forecast": {{
    "projected_monthly_kwh": number,
    "projected_monthly_cost": number,
    "trend": "increasing|decreasing|stable",
    "confidence": "high|medium|low",
    "explanation": "Why this trend is expected"
  }},
  "anomalies": [
    {{
      "type": "spike|drop|pattern_break",
      "description": "What happened",
      "possible_cause": "Likely reason",
      "recommendation": "What to do"
    }}
  ],
  "recommendations": [
    {{
      "type": "behavioral|timing|settings|equipment",
      "title": "Short title",
      "description": "What to do",
      "estimated_savings_kwh": number,
      "estimated_savings_currency": number,
      "actions": ["step1", "step2"],
      "priority": "high|medium|low"
    }}
  ],
  "score": {{
    "value": 0-100,
    "grade": "A|B|C|D|F",
    "breakdown": "Brief assessment"
  }}
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
        return result

    except Exception as e:
        print(f"AI Error: {e}")
        return _default_response(avg_power, daily_kwh, projected_monthly_cost)


def _empty_response() -> Dict:
    return {
        "summary": {
            "average_power_watts": 0,
            "peak_power_watts": 0,
            "daily_kwh": 0,
            "monthly_cost_estimate": 0,
            "description": "No data available. Add a device and generate readings.",
        },
        "forecast": {
            "projected_monthly_kwh": 0,
            "projected_monthly_cost": 0,
            "trend": "stable",
            "confidence": "low",
            "explanation": "Not enough data yet.",
        },
        "anomalies": [],
        "recommendations": [
            {
                "type": "behavioral",
                "title": "Add a device to get started",
                "description": "Create a simulated device and generate readings to get personalized recommendations.",
                "estimated_savings_kwh": 0,
                "estimated_savings_currency": 0,
                "actions": ["Go to Devices tab", "Add a device", "Generate readings"],
                "priority": "high",
            }
        ],
        "score": {"value": 0, "grade": "N/A", "breakdown": "No data yet"},
    }


def _default_response(avg_power: float, daily_kwh: float, monthly_cost: float) -> Dict:
    return {
        "summary": {
            "average_power_watts": avg_power,
            "peak_power_watts": avg_power * 2,
            "daily_kwh": daily_kwh,
            "monthly_cost_estimate": monthly_cost,
            "description": f"You use approximately {daily_kwh:.1f} kWh daily. This is typical for a residential home.",
        },
        "forecast": {
            "projected_monthly_kwh": daily_kwh * 30,
            "projected_monthly_cost": monthly_cost,
            "trend": "stable",
            "confidence": "medium",
            "explanation": "Based on recent usage patterns.",
        },
        "anomalies": [],
        "recommendations": [
            {
                "type": "behavioral",
                "title": "Turn off lights when leaving",
                "description": "Simple habit changes can save 5-10% on your bill.",
                "estimated_savings_kwh": 15,
                "estimated_savings_currency": 2,
                "actions": ["Turn off lights", "Use natural light", "Unplug chargers"],
                "priority": "medium",
            },
            {
                "type": "settings",
                "title": "Adjust thermostat 2°F",
                "description": "Small temperature adjustments add up significantly over time.",
                "estimated_savings_kwh": 50,
                "estimated_savings_currency": 6,
                "actions": ["Lower heat in winter", "Raise AC in summer"],
                "priority": "high",
            },
        ],
        "score": {"value": 70, "grade": "C", "breakdown": "Room for improvement"},
    }

import random
from datetime import datetime, timedelta
from typing import Dict, List


class Simulator:
    def __init__(self):
        self.scenarios = {
            "normal": lambda p, t: 1.0,
            "high_consumption": lambda p, t: 1.8,
            "heating": lambda p, t: 1.5,
            "cooling": lambda p, t: 1.7,
            "vacation": lambda p, t: 0.3,
            "weekend": lambda p, t: 1.1,
            "anomaly_spike": lambda p, t: 3.0,
            "anomaly_drop": lambda p, t: 0.2,
        }

    def generate_reading(
        self, device_type: str, params: Dict, timestamp=None, household=None
    ):
        if timestamp is None:
            timestamp = datetime.utcnow()
        hour = timestamp.hour

        size_mult = 1.0
        occupancy_mult = 1.0
        if household:
            size_sqft = household.get("size_sqft", 1500)
            occupants = household.get("occupants", 4)
            size_mult = size_sqft / 1500
            occupancy_mult = occupants / 4

        base_power = {
            "smart_meter": 500,
            "thermostat": 1000,
            "plug": 200,
            "energy_monitor": 600,
        }.get(device_type, 500)

        if 7 <= hour <= 9:
            mult = 2.5 * occupancy_mult
        elif 17 <= hour <= 21:
            mult = 3.0 * occupancy_mult
        elif 22 <= hour <= 6:
            mult = 0.4
        else:
            mult = 1.2

        power = base_power * mult * size_mult * random.uniform(0.9, 1.1)
        return {
            "power_watts": round(power, 2),
            "energy_kwh": round(power / 1000 / 60, 4),
            "voltage": round(random.uniform(118, 122), 1),
            "current": round(power / 120, 2),
        }

    def generate_historical(
        self, device_type: str, params: Dict, days: int = 7, household=None
    ):
        readings = []
        now = datetime.utcnow()
        for day in range(days):
            for hour in range(24):
                for minute in [0, 30]:
                    ts = now - timedelta(days=day, hours=23 - hour, minutes=minute)
                    reading = self.generate_reading(device_type, params, ts, household)
                    reading["timestamp"] = ts
                    readings.append(reading)
        return readings

    def run_scenario(
        self,
        device_type: str,
        params: Dict,
        scenario: str,
        hours: int = 24,
        household=None,
    ):
        readings = []
        now = datetime.utcnow()
        scenario_func = self.scenarios.get(scenario, self.scenarios["normal"])
        for i in range(hours * 2):
            ts = now - timedelta(minutes=(hours * 60 - i * 30))
            reading = self.generate_reading(device_type, params, ts, household)
            mult = scenario_func(params, ts)
            reading["power_watts"] *= mult
            reading["energy_kwh"] *= mult
            reading["timestamp"] = ts
            readings.append(reading)
        return readings


simulator = Simulator()

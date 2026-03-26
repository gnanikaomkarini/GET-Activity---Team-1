import random
import math
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class DeviceParams:
    home_size: int = 1500  # sq ft
    occupancy: int = 2
    base_consumption: float = 0.8  # kWh per sq ft per month


class Simulator:
    def __init__(self):
        self.scenarios = {
            "normal": self._normal_pattern,
            "high_consumption": self._high_consumption_pattern,
            "heating": self._heating_pattern,
            "cooling": self._cooling_pattern,
            "vacation": self._vacation_pattern,
            "weekend": self._weekend_pattern,
            "anomaly_spike": self._anomaly_spike_pattern,
            "anomaly_drop": self._anomaly_drop_pattern,
        }

    def generate_reading(
        self,
        device_type: str,
        params: Dict[str, Any],
        timestamp: Optional[datetime] = None,
    ) -> Dict[str, float]:
        if timestamp is None:
            timestamp = datetime.utcnow()

        generators = {
            "smart_meter": self._smart_meter_reading,
            "thermostat": self._thermostat_reading,
            "plug": self._plug_reading,
            "energy_monitor": self._energy_monitor_reading,
        }

        generator = generators.get(device_type, self._smart_meter_reading)
        return generator(params, timestamp)

    def _smart_meter_reading(
        self, params: Dict, timestamp: datetime
    ) -> Dict[str, float]:
        hour = timestamp.hour
        day_of_week = timestamp.weekday()

        base_power = 500  # watts

        if 7 <= hour <= 9:  # morning peak
            multiplier = 2.5
        elif 17 <= hour <= 21:  # evening peak
            multiplier = 3.0
        elif 22 <= hour <= 6:  # night
            multiplier = 0.4
        else:  # daytime
            multiplier = 1.2

        if day_of_week >= 5:  # weekend
            multiplier *= 0.9

        home_size = params.get("home_size", 1500)
        multiplier *= home_size / 1500

        noise = random.uniform(0.9, 1.1)
        power_watts = base_power * multiplier * noise

        energy_kwh = power_watts / 1000 / 60

        return {
            "power_watts": round(power_watts, 2),
            "energy_kwh": round(energy_kwh, 4),
            "voltage": round(random.uniform(118, 122), 1),
            "current": round(power_watts / 120, 2),
        }

    def _thermostat_reading(
        self, params: Dict, timestamp: datetime
    ) -> Dict[str, float]:
        hour = timestamp.hour
        mode = params.get("mode", "auto")

        if mode == "heat":
            base_power = 1500
            if 6 <= hour <= 9 or 18 <= hour <= 22:
                base_power *= 1.5
        elif mode == "cool":
            base_power = 1200
            if 12 <= hour <= 18:
                base_power *= 1.8
        else:
            base_power = 100

        noise = random.uniform(0.95, 1.05)
        power_watts = base_power * noise

        return {
            "power_watts": round(power_watts, 2),
            "energy_kwh": round(power_watts / 1000 / 60, 4),
            "voltage": round(random.uniform(118, 122), 1),
            "current": round(power_watts / 120, 2),
        }

    def _plug_reading(self, params: Dict, timestamp: datetime) -> Dict[str, float]:
        hour = timestamp.hour
        appliance = params.get("appliance_type", "general")

        wattages = {
            "refrigerator": 150,
            "washer": 500,
            "dryer": 3000,
            "dishwasher": 1800,
            "microwave": 1000,
            "tv": 100,
            "computer": 200,
            "lighting": 60,
            "charger": 20,
            "general": 50,
        }

        base_power = wattages.get(appliance, 50)

        if appliance == "refrigerator":
            multiplier = 1.0
        elif appliance == "lighting":
            multiplier = 1.5 if 18 <= hour <= 22 else 0.3
        elif appliance in ["washer", "dryer", "dishwasher"]:
            multiplier = 1.5 if 8 <= hour <= 20 else 0.1
        else:
            multiplier = 0.5 if 23 <= hour <= 6 else 1.0

        noise = random.uniform(0.9, 1.1)
        power_watts = base_power * multiplier * noise

        return {
            "power_watts": round(power_watts, 2),
            "energy_kwh": round(power_watts / 1000 / 60, 4),
            "voltage": round(random.uniform(118, 122), 1),
            "current": round(power_watts / 120, 2),
        }

    def _energy_monitor_reading(
        self, params: Dict, timestamp: datetime
    ) -> Dict[str, float]:
        result = self._smart_meter_reading(params, timestamp)
        result["power_watts"] *= random.uniform(0.95, 1.05)
        return result

    def _normal_pattern(self, params: Dict, timestamp: datetime) -> float:
        return 1.0

    def _high_consumption_pattern(self, params: Dict, timestamp: datetime) -> float:
        return 1.8

    def _heating_pattern(self, params: Dict, timestamp: datetime) -> float:
        return 1.5

    def _cooling_pattern(self, params: Dict, timestamp: datetime) -> float:
        return 1.7

    def _vacation_pattern(self, params: Dict, timestamp: datetime) -> float:
        return 0.3

    def _weekend_pattern(self, params: Dict, timestamp: datetime) -> float:
        return 1.1

    def _anomaly_spike_pattern(self, params: Dict, timestamp: datetime) -> float:
        return 3.0

    def _anomaly_drop_pattern(self, params: Dict, timestamp: datetime) -> float:
        return 0.2

    def generate_historical(
        self, device_type: str, params: Dict, days: int = 7
    ) -> List[Dict]:
        readings = []
        now = datetime.utcnow()

        for day in range(days):
            for hour in range(24):
                for minute in [0, 30]:  # every 30 minutes
                    timestamp = now - timedelta(
                        days=day, hours=23 - hour, minutes=minute
                    )
                    reading = self.generate_reading(device_type, params, timestamp)
                    reading["timestamp"] = timestamp
                    readings.append(reading)

        return readings

    def run_scenario(
        self, device_type: str, params: Dict, scenario: str, duration_hours: int = 24
    ) -> List[Dict]:
        readings = []
        now = datetime.utcnow()
        scenario_func = self.scenarios.get(scenario, self._normal_pattern)

        for i in range(duration_hours * 2):  # every 30 minutes
            timestamp = now - timedelta(minutes=(duration_hours * 60 - i * 30))
            reading = self.generate_reading(device_type, params, timestamp)

            scenario_multiplier = scenario_func(params, timestamp)
            reading["power_watts"] *= scenario_multiplier
            reading["energy_kwh"] *= scenario_multiplier

            reading["timestamp"] = timestamp
            readings.append(reading)

        return readings


simulator = Simulator()

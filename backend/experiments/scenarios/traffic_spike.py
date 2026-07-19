import random


def traffic_spike(steps=40):
    states = []
    for i in range(steps):
        in_spike = steps // 3 < i < steps * 2 // 3
        cpu = (75 + 20 * random.random()) if in_spike else (20 + 12 * random.random())
        carbon = 420 + 80 * random.random()
        trend = "rising" if i < steps * 2 // 3 and in_spike else "steady"
        states.append({
            "cpu_usage": cpu,
            "carbon_intensity": carbon,
            "predicted_traffic": [int(cpu * 5 + random.uniform(-20, 20)) for _ in range(6)],
            "trend": trend,
            "hour": 11,
        })
    return states


def normal_day(steps=40):
    states = []
    for i in range(steps):
        cpu = 22 + 18 * random.random()
        carbon = 380 + 60 * random.random()
        states.append({
            "cpu_usage": cpu,
            "carbon_intensity": carbon,
            "predicted_traffic": [int(cpu * 4 + random.uniform(-20, 20)) for _ in range(6)],
            "trend": "steady",
            "hour": 14,
        })
    return states


def low_traffic_night(steps=40):
    states = []
    for i in range(steps):
        cpu = 8 + 10 * random.random()
        carbon = 280 + 50 * random.random()
        states.append({
            "cpu_usage": cpu,
            "carbon_intensity": carbon,
            "predicted_traffic": [int(cpu * 3 + random.uniform(-10, 10)) for _ in range(6)],
            "trend": "steady",
            "hour": 3,
        })
    return states
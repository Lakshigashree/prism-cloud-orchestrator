import random


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


def normal_day(steps=40):
    states = []
    for i in range(steps):
        cpu = 35 + 25 * random.random()
        carbon = 380 + 80 * random.random()
        states.append({
            "cpu_usage": cpu,
            "carbon_intensity": carbon,
            "predicted_traffic": [int(cpu * 2.5 + random.uniform(-15, 15)) for _ in range(6)],
            "trend": "rising" if i > 20 else "steady",
            "hour": 14,
        })
    return states


def traffic_spike(steps=40):
    states = []
    for i in range(steps):
        if i < 10:
            cpu = 30 + 10 * random.random()
        elif i < 25:
            cpu = 70 + 15 * random.random()
        else:
            cpu = 45 + 15 * random.random()
        carbon = 420 + 100 * random.random()
        states.append({
            "cpu_usage": cpu,
            "carbon_intensity": carbon,
            "predicted_traffic": [int(cpu * 2.8 + random.uniform(-20, 20)) for _ in range(6)],
            "trend": "rising" if 10 <= i < 25 else "falling" if i >= 25 else "steady",
            "hour": 14,
        })
    return states
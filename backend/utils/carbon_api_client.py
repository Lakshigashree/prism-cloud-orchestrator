import os
import random
import requests

CARBON_API_KEY = os.getenv("CARBON_API_KEY", "")
CARBON_API_ZONE = os.getenv("CARBON_API_ZONE", "IN")
CARBON_API_URL = "https://api.electricitymap.org/v3/carbon-intensity/latest"

# Fallback used if no API key is set, or the API call fails (rate limit, network, etc.)
# so the rest of the pipeline never breaks because of this one dependency.
_last_value = 420.0


def get_carbon_intensity() -> dict:
    global _last_value

    if CARBON_API_KEY:
        try:
            resp = requests.get(
                CARBON_API_URL,
                params={"zone": CARBON_API_ZONE},
                headers={"auth-token": CARBON_API_KEY},
                timeout=4,
            )
            if resp.status_code == 200:
                data = resp.json()
                _last_value = data.get("carbonIntensity", _last_value)
                return {
                    "region": CARBON_API_ZONE,
                    "carbonIntensity": round(_last_value, 1),
                    "unit": "gCO2eq/kWh",
                    "source": "live",
                }
        except requests.RequestException:
            pass  # fall through to simulated value below

    # Simulated fallback: drift the last known value slightly so it still
    # behaves realistically instead of returning a flat constant forever.
    _last_value = max(150, min(650, _last_value + random.uniform(-15, 15)))
    return {
        "region": CARBON_API_ZONE,
        "carbonIntensity": round(_last_value, 1),
        "unit": "gCO2eq/kWh",
        "source": "simulated",
    }

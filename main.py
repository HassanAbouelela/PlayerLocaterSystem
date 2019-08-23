import requests
import json
import math


def coords(system):
    """Obtains the coordinates of any system from EDSM. Returns dict with cords, or None if there is any error."""
    try:
        coordinates = requests.get(url=f"https://www.edsm.net/api-v1/systems?systemName={system}&coords=1").content
        if coordinates != "[]":
            return json.loads(coordinates)[0]["coords"]
        else:
            return None
    except Exception:
        return None


def distance_calculator(system1, system2):
    """Calculates distance between any two given systems. Returns int, or None if there is any error."""
    try:
        system1 = coords(system1)
        system2 = coords(system2)
        if not system1 or not system2:
            return None
        diff_x = abs(system1["x"] - system2["x"])
        diff_y = abs(system1["y"] - system2["y"])
        diff_z = abs(system1["z"] - system2["z"])
        distance = round(math.sqrt(diff_x**2 + diff_y**2 + diff_z**2), 2)
        return distance
    except Exception:
        return None

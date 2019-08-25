import asyncio
import aiohttp
import asyncpg
import math
import logging


# Event Logger
logger = logging.getLogger("log")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="log.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
logger.addHandler(handler)


async def coords(system: str):
    """Obtains the coordinates of any system from EDSM. Returns dict with cords, or None if there is any error."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.edsm.net/api-v1/systems?systemName={system}&coords=1") as response:
                coordinates = await response.json()
        if coordinates != "[]":
            return coordinates[0]["coords"]
        else:
            return None
    except Exception:
        return None


async def distance_calculator(system1: str, system2: str):
    """Calculates distance between any two given systems. Returns int, or None if there is any error."""
    try:
        system1 = await coords(system1)
        system2 = await coords(system2)
        if not system1 or not system2:
            return None
        diff_x = abs(system1["x"] - system2["x"])
        diff_y = abs(system1["y"] - system2["y"])
        diff_z = abs(system1["z"] - system2["z"])
        distance = round(math.sqrt(diff_x**2 + diff_y**2 + diff_z**2), 2)
        return distance
    except Exception:
        return None


async def seal_search(seal: str, automaticadd=False):
    """Searches the database for current seal location, if the seal is not found withing the database they are
    automatically added."""


async def main():
    something = await distance_calculator("sol", "beagle point")
    print(something)


loop = asyncio.get_event_loop()
try:
    loop.create_task(main())
    loop.run_forever()
finally:
    loop.close()

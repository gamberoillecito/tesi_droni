import asyncio
from loguru import logger
from drone import Drone
from base_station import BaseStation

async def main():
    addr = [[50040, 14540], [50041, 14541]]
    addrs = [14540, 14541]
    d = Drone(*addr[0])
    await d.connect()
    await d.takeoff_and_land()
    return
    Drones = [Drone(i) for i in addrs]
    connections = asyncio.gather(*[d.connect() for d in Drones])
    drones = await connections

    
if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(main())

#!/usr/bin/env python3
import asyncio
from loguru import logger
from drone import Drone
from base_station import BaseStation

async def main():
    # addr = [[50040, 14540], [50041, 14541]]
    # addrs = [14540, 14541]
    # d = Drone(*addr[0])
    # await d.connect()
    # await d.takeoff_and_land()
    # return
    # Drones = [Drone(i) for i in addrs]
    # connections = asyncio.gather(*[d.connect() for d in Drones])
    # drones = await connections

    BS = BaseStation()
    await BS.connect_to_n_drones(2)
    d0, d1 = BS.drones
    await d0.add_neighbour(14541)
    asyncio.gather(d1.takeoff_and_land(), d0.test_neighbour_altitude())
    # cacca = asyncio.gather(*[i.takeoff_and_land() for i in BS.drones])
    
if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(main())

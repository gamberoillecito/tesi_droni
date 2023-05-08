#!/usr/bin/env python3
import asyncio
from mavsdk import System
from loguru import logger
from drone import Drone
from base_station import BaseStation

async def main():
    addr = [[50040, 14540], [50041, 14541]]
    d = Drone(*addr[0])
    await d.connect()
    await d.takeoff_and_land()
    return
    Drones = [Drone(i[0], i[1]) for i in addr]
    connections = asyncio.gather(*[d.connect() for d in Drones])
    drones = await connections


    # pipi = asyncio.ensure_future(print_status_text(drones[0]))
    cacca = asyncio.gather(*[i.takeoff_and_land() for i in Drones])
    # pipi.cancel()
    await cacca
    
if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(main())

import asyncio
from drone import Drone
from loguru import logger

class BaseStation:
    def __init__(self) -> None:
        self.drones = None

    async def connect_to_n_drones(self, n=2) -> None:
        addrs = [14540, 14541]
        # d = Drone(*addr[0])
        # await d.connect()
        # await d.takeoff_and_land()
        # return
        self.drones = [Drone(i) for i in addrs]
        connections = asyncio.gather(*[d.connect() for d in self.drones])
        await connections


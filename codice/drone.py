from loguru import logger
from mavsdk import System
import asyncio

async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return
        
@logger.catch
class Drone:
    def __init__(self, sys_port, sys_addr) -> None:
        self.sys_addr = sys_addr
        self.sys_port = sys_port
        self.__drone = System(port=self.sys_port)
    
    async def connect(self):
        # await drone.connect()
        await self.__drone.connect(system_address=f"udp://:{self.sys_addr}")

        status_text_task = asyncio.ensure_future(print_status_text(self.__drone))

        logger.debug("Waiting for drone to connect...")
        async for state in self.__drone.core.connection_state():
            if state.is_connected:
                logger.debug(f"Connected sys_addr{self.sys_addr}, sys_port{self.sys_port}!")
                break

        logger.debug("Waiting for drone to have a global position estimate...")
        async for health in self.__drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                logger.debug("Global position estimate OK")
                break

        status_text_task.cancel()
    
    async def arm(self):
        logger.debug("Arming")
        await self.__drone.action.arm()

    async def takeoff(self):
        logger.debug("Taking off")
        await self.__drone.action.takeoff()

    async def land(self):
        logger.debug("Landing")
        await self.__drone.action.land()

    async def takeoff_and_land(self):
        await self.arm()
        await self.takeoff()
        await asyncio.sleep(10)
        await self.land()
from loguru import logger
from pprint import pprint
from mavsdk import System
import asyncio
from typing import List, Callable
from systemwrapper import SystemWrapper
from droneposition import DronePosition


class Swarm:
    # indirizzo del prossimo drone creato (incrementata dopo la creazione di ciascun drone)
    next_drone_address = 14540 
    def __init__(self,
                target_scanner:Callable[[System], float],
                drones_number:int,
                drones_addrs:List[int]=None) -> None:
        '''Inizializza una flotta di drones_number droni agli indirizzi
        specificati oppure ad indirizzi progressivi.

        Arguments:
            drones_number -- Numero di droni da cui è composta la flotta

        pass
        Keyword Arguments:
            drones_addrs -- Indirizzi dei droni (default: {None})

        Raises:
            ValueError: il numero di droni deve corrispondere al numero
            di indirizzi specificati
        '''                
        self.target_scanner = target_scanner
        self.__discoveries:List[float] = []
        self.drones_number = drones_number
        self.__positions = []
        self.drones:List[System] = []
        # se non viene passata una lista di indirizzi vengono usati quelli di 
        # default a partire da next_drone_address
        if drones_addrs == None:
            self.drones_addrs = []
            for i in range(drones_number):
                self.drones_addrs.append(self.next_drone_address)
                self.next_drone_address += 1
        elif drones_number != len(drones_addrs):
            raise ValueError; "The number of drones specified does not match with the list size"
        else:
            self.drones_addrs = drones_addrs
        logger.info(f"Creating swarm with {self.drones_number} drones at {self.drones_addrs}")


    async def connect(self):
        logger.info("Connecting to drones...")
        for a in self.drones_addrs:
            logger.info(f"Connecting to drone at {a}")
            sysW = SystemWrapper(a)
            drone = await sysW.connect()
            logger.info(f"Coonection to drone at {a} completed")
            self.drones.append(drone)

    async def takeoff(self):
        #TODO controllare se i droni sono connessi 
        for d in self.drones:
            await d.action.arm()
            await d.action.takeoff()

    async def land(self):
        for d in self.drones:
            await d.action.land()

    @property
    async def positions(self) -> List[DronePosition]:
        self.__positions = []
        for d in self.drones:
            p = await anext(d.telemetry.position())
            pos = DronePosition.from_mavsdk_position(p)
            self.__positions.append(pos)

        return self.__positions
    
    # Non si possono fare i setter asincroni
    # @positions.setter
    # async def positions(self, target_positions:List[List[float]]):
    #     for n, d in enumerate(self.drones):
    #         pos = self.positions[n]
    #         await d.action.goto_location(pos.latitude_deg, pos.longitude_deg, pos.absolute_altitude_m + 1, 0)
    # async def do_for_all(self, function:Callable):
    #     for d in self.drones:
    #         function(d)
    async def set_positions(self, target_positions:List[DronePosition]):
        prev_pos = await self.positions
        print(prev_pos)
        for n, d in enumerate(self.drones):
            pos = target_positions[n]
            logger.info(f"Moving drone {self.drones_addrs[n]} to {pos}")
            await d.action.goto_location(*pos.to_goto_location(prev_pos[n]))
    async def do_for_all(self, function:Callable):
        for d in self.drones:
            function(d)

    @property
    async def discoveries(self):
        self.__discoveries = []
        for d in self.drones:
            self.__discoveries.append(self.target_scanner(d))

        return self.__discoveries

def print_pos(pos):
    for p in pos:
        print(p)
    print("#"*10)

async def main():
    sw = Swarm(lambda x: 1, 2)
    await sw.connect()
    await sw.takeoff()
    print(await sw.discoveries)
    # print_pos(await sw.positions)
    await asyncio.sleep(10)
    pos = await sw.positions
    for n, p in enumerate(pos):
        n += 1
        p.increment_m(2*n, 2*n, 2*n)
    await sw.set_positions(pos)
    await asyncio.sleep(10)
    await sw.land()
    # print_pos(await sw.positions)

if __name__ == "__main__":
    asyncio.run(main())
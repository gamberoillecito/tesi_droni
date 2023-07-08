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
            raise ValueError; "Il numero di droni indicato non corrisponde all'array fornito"
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
    async def positions(self) -> List[List[DronePosition]]:
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
    async def set_positions(self, target_positions:List[List[float]]):
        positions = await self.positions
        for n, d in enumerate(self.drones):
            pos = positions[n]
            logger.debug("vado in posizione")
            await d.action.goto_location(pos.latitude_deg+1, pos.longitude_deg+1, pos.absolute_altitude_m + 1, 0)
    async def do_for_all(self, function:Callable):
        for d in self.drones:
            function(d)

def print_pos(pos):
    for p in pos:
        print(p)
    print("#"*10)

async def main():
    sw = Swarm(2)
    await sw.connect()
    await sw.takeoff()
    print_pos(await sw.positions)
    await asyncio.sleep(10)
    await sw.set_positions([[2.0], [1.0]])
    await asyncio.sleep(10)
    await sw.land()
    print_pos(await sw.positions)

if __name__ == "__main__":
    asyncio.run(main())
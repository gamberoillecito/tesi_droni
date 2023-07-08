from loguru import logger
from mavsdk import System
import asyncio
from typing import List, Callable
from systemwrapper import SystemWrapper


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

        Keyword Arguments:
            drones_addrs -- Indirizzi dei droni (default: {None})

        Raises:
            ValueError: il numero di droni deve corrispondere al numero
            di indirizzi specificati
        '''                
        self.drones_number = drones_number
        self.__positions = []
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
        self.drones:List[System] = []
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
        #TODO controllare se i droni sono connessi 
        for d in self.drones:
            await d.action.land()

    @property
    async def positions(self):
        p = await anext(self.drones[0].telemetry.position())
        print(p)
        # try:
        #     async for pos in self.drones[0].telemetry.position():
        #         print(pos)
        # except asyncio.CancelledError:
        #     return 0
        # self.__positions = []
        # # for n,d in enumerate(self.drones):
        # #     self.__positions.append(d.telemetry.position())
        # # return self.__positions

    async def do_for_all(self, function:Callable):
        for d in self.drones:
            function(d)

async def main():
    sw = Swarm(2)
    await sw.connect()
    # for p in sw.positions:
    #     async for i in p:
    #         print(p)
    await sw.positions
    await sw.takeoff()
    await asyncio.sleep(10)
    await sw.land()

if __name__ == "__main__":
    asyncio.run(main())
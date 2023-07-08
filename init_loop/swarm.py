from loguru import logger
import random
import asyncio
from utility import print_status_text
from mavsdk import System
from dataclasses import dataclass
from typing import List, Callable

class SystemWrapper:
    '''Nasconde parte della complessità della classe Systema di MavSDK.
    Al momento prevede di istanziare un elemento della classe System e di
    connetervicisi. In futuro potrebbe essere utile per sfruttare meglio
    gli altri parametri previsti

        Attributi:
        system_addr -- Indirizzo del remote system (il drone)
        mav_sdk_server_addr -- Controllare documentazione mavsdk (default: {None})
        port -- Controllare documentazione mavsdk (default: {None})
        sysid -- Controllare documentazione mavsdk (default: {None})
    '''
    @logger.catch
    def __init__(self,
                 system_addr:int) -> None:
        self.system_addr = system_addr
        # la porta casuale è copiata da uno script, ancora devo capirne il motivo
        self.server_port = random.randint(1000, 65535)

        logger.debug(f"Creating System: system_addr={self.system_addr}, server_port={self.server_port}")
        self.system = System(port=self.server_port)
    
    @logger.catch
    async def connect(self) -> System:
        '''Effettua la connessione a un System (il drone). Per ridurre
        la complessità, dall'esterno è accessibile solo un drone già
        connesso.

        Returns:
            L'istanza di System già connessa.
        '''
        logger.debug(f"Connecting to system at {self.system_addr}")
        await self.system.connect(f"udp://:{self.system_addr}")
        async for state in self.system.core.connection_state():
            if state.is_connected:
                logger.debug("Connection completed")
                break

        logger.debug("Waiting for drone to have a global position estimate...")
        async for health in self.system.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                logger.debug("Global position estimate OK")
                break
        return self.system
    

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
        self.drones = []
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

    async def positions(self):
        pass
    
    async def do_for_all(self, function:Callable):
        for d in self.drones:
            function(d)

async def main():
    sw = Swarm(2)
    await sw.connect()
    await sw.takeoff()
    await asyncio.sleep(10)
    await sw.land()

if __name__ == "__main__":
    asyncio.run(main())
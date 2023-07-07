from loguru import logger
import asyncio
from utility import print_status_text
from mavsdk import System
from dataclasses import dataclass
from typing import List

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
    def __init__(self,
                 remote_addr:int,
                 mav_sdk_server_addr:int = None,
                 port:int = None, sysid:int = None) -> None:
        self.system_addr = remote_addr
        self.addr =mav_sdk_server_addr 
        self.port = port 
        self.sysid = sysid

        self.system = System(address= self.addr, port=self.port, sysid=self.sysid)
    
    def connect(self) -> System:
        '''Effettua la connessione a un System (il drone). Per ridurre
        la complessità, dall'esterno è accessibile solo un drone già
        connesso.

        Returns:
            L'istanza di System già connessa.
        '''
        self.system.connect(f"udp://:{self.system_addr}")
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
        
        if drones_addrs == None:
            self.drones_addrs = []
            for i in range(drones_number):
                self.drones_addrs.append(self.next_drone_address)
                self.next_drone_address += 1
        elif drones_number != len(drones_addrs):
            raise ValueError; "Il numero di droni indicato non corrisponde all'array fornito"
        else:
            self.drones_addrs = drones_addrs

        self.drones = []
        for a in self.drones_addrs:
            sys = SystemWrapper(a)
            drone = sys.connect()
            self.drones.append(drone)



def initialization():
    '''Contiene il codice che deve essere eseguito una sola volta
    all'avvio del programma. L'utilizzo principale è quello di stabilire
    la connessione con i droni.
    '''
    pass


def receive_drones_info():
    '''Esegue le operazioni necessarie a recuperare le informazioni dai
    droni. La funzione viene eseguita ciclicamente all'interno di
    main_loop().'''
    pass


def pilot_drones():
    '''Esegue le operazioni necessarie a controllare i movimenti dei
    droni. La funzione viene eseguita ciclicamente all'interno di
    main_loop().'''
    pass


def check_for_target(drone):
    ''''''
    pass


def main_loop():
    '''Contiene il codice che deve essere eseguito ciclicamente dalla
    ground station (GS).
    '''
    pass

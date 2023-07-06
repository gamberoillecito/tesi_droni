from loguru import logger
import asyncio
from utility import print_status_text
from mavsdk import System
class Swarm:
    '''Rappresenta la flotta di droni'''

    def __init__(self) -> None:
        self.drones = []

    async def connect(self):
        '''Effettua la connessione a tutti i droni'''

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

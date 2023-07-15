from swarm import Swarm
import asyncio
import random
from droneposition import DronePosition
from loguru import logger
import math

# Sarà inizializzata a un'istanza della classe DronePosition
# che rappresenta la posizione dell'obiettivo virtuale
VIRTUAL_TARGET = None

# Funzione di testing che si occupa di creare un obiettivo virtuale
# nelle vicianze del punto di decollo dei droni. Più nello specifico
# l'obiettivo virtuale verrà generato all'interno di un cerchio di raggio
# `max_distance` dal punto di decollo del primo drone della `swarm`
async def create_virtual_target(swarm:Swarm, max_distance) -> DronePosition:
    assert max_distance > 1, "Il target non può coincidere con i droni"
    
    # recupero le informazioni sui droni
    starting_pos = await swarm.positions
    # creo un punto casuale in un cerchio di raggio `max_distance` centrato 
    # nel punto di decollo del primo drone
    center = starting_pos[0]
    alpha = 2 * math.pi * random.random()
    u = random.random() + random.random()

    r = max_distance * (2 - u if u > 1 else u)
    target_x_incr = r * math.cos(alpha)
    target_y_incr = r * math.sin(alpha)
    target_z_incr = random.randrange(0, max_distance)

    # Il virtual target coinciderà con il punto di decollo traslato
    # delle quantità appena calcolate
    virtual_target = center.increment_m(target_x_incr, target_y_incr, target_z_incr)
    return virtual_target

# Funzione passata alla Swarm per il riconoscimento dell'obiettivo.
# In questo caso fa riferimento al "sensore" (simulato) destinato
# al riconoscimento dei virutal target
async def target_scanner(drone) -> float:
    # Recupero la posizione del drone
    p = await anext(drone.telemetry.position())
    drone_pos = DronePosition.from_mavsdk_position(p)
    # Calcolo la distanza tra il drone e il VIRTUAL_TARGET
    distance = drone_pos.distance_2D_m(VIRTUAL_TARGET)
    # Restituisco un valore che diminuisce esponenzialmente con la distanza
    discovery = math.exp(-distance/10)
    return discovery 


async def main():
    global VIRTUAL_TARGET
    # Creo una swarm con 2 droni e mi ci connetto
    sw = Swarm(target_scanner, 2)
    await sw.connect()

    # Creo un VIRTUAL_TARGET (l'operazione è asincrona quindi attendo che
    # la creazione sia ultimata)
    while VIRTUAL_TARGET == None:
        VIRTUAL_TARGET = await create_virtual_target(sw, 100)
    logger.debug(f"Virtual Target: {VIRTUAL_TARGET}")

    # Per poter visualizzare la posizione del target su QGC creo una Swarm
    # composta da un singolo drone e faccio spostare il drone sul VIRTUAL_TARGET
    # (Questa operazione è solamente per scopi di debug e non ha niente a che
    # vedere con il funzionamento reale delle operazioni). 
    # Dato che è solo per motivi di test, il valore della funzione target_scanner
    # non è significativo
    target_swarm = Swarm(lambda x: 0, 1) 
    await target_swarm.connect()
    await target_swarm.takeoff()
    await asyncio.sleep(5)
    await target_swarm.set_positions([VIRTUAL_TARGET])
    await asyncio.sleep(10)
    await target_swarm.land()

    # Quanto segue è una serie di esempi che illustrano il funzionamento della
    # classe Swarm. Il comportamento atteso è che i droni si alzino in volo e 
    # si spostino verso Nord, verso Est e in Alto di un numero di metri doppio
    # rispetto al proprio indice (il primo drone si sposta di 2 metri a Est,
    # 2 metri a Nord e 2 metri in alto), il secondo invece di 4 metri.
    # Durante gli spostamenti verranno stamapate le discoveries che saranno
    # tanto più alte quanto i droni saranno vicini al VIRTUAL_TARGET
    await sw.takeoff()
    disc = await sw.discoveries
    logger.info(f"Discoveries pre volo: {disc}")
    await asyncio.sleep(10)
    original_pos = await sw.positions
    
    new_poss = []
    for n, p in enumerate(original_pos):
        n += 1
        new_poss.append(p.increment_m(2*n, 2*n, 2*n))
    await sw.set_positions(new_poss)

    await asyncio.sleep(10)
    disc = await sw.discoveries
    logger.info(f"Discoveries in volo: {disc}")
    await sw.set_positions(original_pos)
    await asyncio.sleep(10)
    await sw.land()

if __name__ == "__main__":
    asyncio.run(main())
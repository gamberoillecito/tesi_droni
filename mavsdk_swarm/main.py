from swarm import Swarm
import asyncio
import random
from droneposition import DronePosition
from loguru import logger
import math

VIRTUAL_TARGET = None

async def create_virtual_target(swarm:Swarm, max_distance) -> DronePosition:
    assert max_distance > 1, "Il target non può coincidere con i droni"
    starting_pos = await swarm.positions
    # creo un punto casuale in un cerco di raggio `max_distance` centrato 
    # nel punto di decollo dei droni
    center = starting_pos[0]
    alpha = 2 * math.pi * random.random()
    u = random.random() + random.random()

    r = max_distance * (2 - u if u > 1 else u)
    target_x_incr = r * math.cos(alpha)
    target_y_incr = r * math.sin(alpha)
    target_z_incr = random.randrange(0, max_distance)

    virtual_target = center.increment_m(target_x_incr, target_y_incr, target_z_incr)
    return virtual_target

async def target_scanner(drone) -> float:
    p = await anext(drone.telemetry.position())
    drone_pos = DronePosition.from_mavsdk_position(p)
    distance = drone_pos.distance_m(VIRTUAL_TARGET)
    return distance

def print_pos(pos):
    for p in pos:
        print(p)
    print("#"*10)


async def main():
    global VIRTUAL_TARGET
    sw = Swarm(target_scanner, 2)
    await sw.connect()

    ########################################################
    # Codice temporaneo per la gestione del virtual target #
    ########################################################
    while VIRTUAL_TARGET == None:
        VIRTUAL_TARGET = await create_virtual_target(sw, 3)
    # drone che rappresenta il target (soluzione temporanea)
    logger.debug(f"Virtual Target: {VIRTUAL_TARGET}")
    target_swarm = Swarm(lambda x: 0, 1) 
    await target_swarm.connect()
    await target_swarm.takeoff()
    await target_swarm.set_positions([VIRTUAL_TARGET])
    await asyncio.sleep(10)

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
    # print_pos(await sw.positions)

if __name__ == "__main__":
    asyncio.run(main())
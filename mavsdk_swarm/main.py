from swarm import Swarm
import asyncio
import random
from droneposition import DronePosition
from loguru import logger

VIRTUAL_TARGET = None

async def create_virtual_target(swarm:Swarm, max_distance) -> DronePosition:
    assert max_distance > 1, "Il target non può coincidere con i droni"
    starting_pos = await swarm.positions
    starting_pos = starting_pos[0]
    target_x_incr = random.randrange(1,max_distance)
    target_y_incr = random.randrange(1,max_distance)
    target_z_incr = random.randrange(1,max_distance)

    virtual_target = starting_pos.increment_m(target_x_incr, target_y_incr, target_z_incr)
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
    while VIRTUAL_TARGET == None:
        VIRTUAL_TARGET = await create_virtual_target(sw, 3)
    logger.debug(f"Virtual Target: {VIRTUAL_TARGET}")
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
#!/usr/bin/env python3
import threading
import time
import asyncio
from mavsdk import System
from pymavlink import mavutil

POSITION_MESSAGE_ID = 33

# Function to send position message to another drone
def send_position_message(target, position):
    msg = target.mav.message_factory.set_position_target_local_ned_encode(
        0,  # time_boot_ms
        0,  # target_system
        0,  # target_component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111000111,  # type_mask (ignore everything except position)
        position[0],  # x
        position[1],  # y
        position[2],  # z
        0,  # vx
        0,  # vy
        0,  # vz
        0,  # afx
        0,  # afy
        0,  # afz
        0,  # yaw
        0,  # yaw_rate
    )
    target.send_mavlink(msg)

# Function to periodically send position message
async def send_position_periodically(drone, target, period):
    try:
        async for current_position in drone.telemetry.position():
            send_position_message(target, [current_position.latitude_deg, current_position.longitude_deg, current_position.absolute_altitude_m])
            time.sleep(period)
    except asyncio.CancelledError:
        return


async def connect_to_drone(s, u):

    drone = System(port=s)
    # await drone.connect()
    await drone.connect(system_address=f"udp://:{u}")

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone on ports {s}, {u}!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    status_text_task.cancel()
    return drone
    
async def takeoff_and_land(drone):
    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(10)

    print("-- Landing")
    await drone.action.land()

async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return

async def main():
    addr = [[50040, 14540], [50041, 14541]]
    connections = asyncio.gather(*[connect_to_drone(i[0], i[1]) for i in addr])
    drones = await connections
    drone1 = drones[0]
    drone2 = drones[1]
    # Start sending position messages from drone1 to drone2
    s = asyncio.gather(send_position_periodically(drone1, drone2, 1),send_position_periodically(drone2, drone1, 2))
    await s


    # pipi = asyncio.ensure_future(print_status_text(drones[0]))
    # cacca = asyncio.gather(*[takeoff_and_land(i) for i in drones])
    # pipi.cancel()
    # await cacca
    
if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(main())

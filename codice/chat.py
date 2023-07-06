from mavsdk import System
from pymavlink import mavutil
import threading
import asyncio
import time

# Constants
DRONE1_UDP_URL = "udp://127.0.0.1:14540"
DRONE2_UDP_URL = "udp://127.0.0.1:14541"
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
def send_position_periodically(drone, target, period):
    while True:
        current_position = drone.telemetry.local_position_ned()
        send_position_message(target, [current_position.north_m, current_position.east_m, current_position.down_m])
        time.sleep(period)

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

async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return

# Main script
def main():
    # Create connections to the drones
    drone1 = connect_to_drone(50040, 14540)

    drone2 = connect_to_drone(50041, 14541)


    # Start sending position messages from drone1 to drone2
    drone1_thread = threading.Thread(target=send_position_periodically, args=(drone1, drone2, 1))
    drone1_thread.start()

    # Start sending position messages from drone2 to drone1
    drone2_thread = threading.Thread(target=send_position_periodically, args=(drone2, drone1, 2))
    drone2_thread.start()

    # Let the script run for some time
    time.sleep(10)

    # Stop the threads and disconnect from the drones
    drone1_thread.join()
    drone2_thread.join()
    drone1.disconnect()
    drone2.disconnect()

if __name__ == "__main__":
    main()

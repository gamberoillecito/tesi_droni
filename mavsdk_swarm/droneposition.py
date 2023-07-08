
from mavsdk import telemetry
from typing import List
from math import sqrt
# rappresentazione di default = []
# http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/plugins/telemetry.html#mavsdk.telemetry.Position
# http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/plugins/telemetry.html#mavsdk.telemetry.PositionBody
# http://mavsdk-python-docs.s3-website.eu-central-1.amazonaws.com/plugins/action.html#mavsdk.action.Action.goto_location

def deg_to_m(deg) -> float:
    # 1 deg = 111319.9 m
    return deg * 111319.9

def m_to_deg(m) -> float:
    return m / 111319.9

# goto_location(latitude_deg, longitude_deg, absolute_altitude_m, yaw_deg)
# mavsdk.telemetry.PositionBody(x_m, y_m, z_m)
# mavsdk.telemetry.Position(latitude_deg, longitude_deg, absolute_altitude_m, relative_altitude_m)
class DronePosition:
    '''Rappresentazione della posizione del drone
    indipendente da quella di MavSDK. Implementa i metodi per
    convertire le posizioni nei vari formati necessari
    (da Telemetry.position a lista di float, da lista di float al
    formato richiesto da action.goto_location, ecc.)
    '''    
    def __init__(self,
                 latitude_deg:float,
                 longitude_deg:float,
                 relative_altitude_m:float) -> None:
        self.latitude_deg = latitude_deg
        self.longitude_deg = longitude_deg
        self.relative_altitude_m = relative_altitude_m
    
    @classmethod
    def from_mavsdk_position(self, pos:telemetry.Position) -> None:
        self.latitude_deg = pos.latitude_deg
        self.longitude_deg = pos.longitude_deg
        self.relative_altitude_m = pos.relative_altitude_m

    def increment_m(self, lat_increment_m, long_increment_m, alt_increment_m):
        # TODO: questo metodo di convertire metri in gradi non è molto accurato
        self.latitude_deg += m_to_deg(lat_increment_m)
        self.longitude_deg += m_to_deg(long_increment_m)
        self.relative_altitude_m += alt_increment_m
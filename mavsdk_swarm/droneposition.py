
from mavsdk import telemetry
from typing import List
import math
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
                 absolute_altitude_m:float) -> None:
        self.latitude_deg = latitude_deg
        self.longitude_deg = longitude_deg
        self.absolute_altitude_m = absolute_altitude_m
    
    @classmethod
    def from_mavsdk_position(cls, pos:telemetry.Position) -> None:
        return cls(pos.latitude_deg, pos.longitude_deg, pos.absolute_altitude_m)

    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    
    # goto_location(latitude_deg, longitude_deg, absolute_altitude_m, yaw_deg)
    def to_goto_location(self, prev_pos:'DronePosition'=None) -> List[float]:
        if prev_pos == None:
            yaw = 0
        else:
            # ATTENZIONE: i calcoli fatti qui sono solo un'approssimazione
            d_lat = self.latitude_deg - prev_pos.latitude_deg
            d_lon = self.longitude_deg - prev_pos.longitude_deg
            tan_angle = 90 + d_lon/d_lat
            yaw = math.atan(tan_angle)
        return (self.latitude_deg, self.longitude_deg, self.absolute_altitude_m, yaw)

    def increment_m(self, lat_increment_m, long_increment_m, alt_increment_m):
        # TODO: questo metodo non è molto accurato
        new_lat = self.latitude_deg + m_to_deg(lat_increment_m)
        new_lon = self.longitude_deg + m_to_deg(long_increment_m)
        new_alt = self.absolute_altitude_m + alt_increment_m
        return DronePosition(new_lat, new_lon, new_alt)

    def distance_m(self, point:'DronePosition') -> float:
        # TODO: questo metodo non è molto accurato
        dx_m = deg_to_m(self.longitude_deg - point.longitude_deg)
        dy_m = deg_to_m(self.latitude_deg - point.latitude_deg)
        dz_m = deg_to_m(self.absolute_altitude_m - point.absolute_altitude_m)
        distance = math.sqrt(dx_m**2 + dy_m**2 + dz_m**2)
        return distance
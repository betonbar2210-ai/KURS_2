class Airplane:
    def __init__(self, callsign: str, origin_country: str, velocity: float, altitude: float, on_ground: bool) -> None:
        self.validate_data(callsign, origin_country, velocity, altitude)
        self.callsign = callsign.strip()
        self.origin_country = origin_country.strip()
        self.velocity = velocity
        self.altitude = altitude
        self.on_ground = on_ground

    def validate_data(self, callsign, origin_country, velocity, altitude):
        if not callsign or not isinstance(callsign, str):
            raise ValueError("Позывной должен быть непустой строкой")
        if not origin_country or not isinstance(origin_country, str):
            raise ValueError("Страна регистрации должна быть непустой строкой")
        if velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")
        if altitude < 0:
            raise ValueError("Высота не может быть отрицательной")

    def __lt__(self, other):
        return self.altitude < other.altitude

    def __gt__(self, other):
        return self.altitude > other.altitude

    def compare_by_velocity(self, other):
        if self.velocity > other.velocity:
            return 1
        elif self.velocity < other.velocity:
            return -1
        else:
            return 0

    @classmethod
    def cast_to_object_list(cls, data):
        airplanes = []
        for item in data:
            try:
                callsign = item[1] or "N/A"
                origin_country = item[2] or "Unknown"
                velocity = float(item[9]) * 3.6 if item[9] else 0
                altitude = float(item[7]) if item[7] else 0
                on_ground = item[8]

                airplanes.append(cls(callsign, origin_country, velocity, altitude, on_ground))
            except (ValueError, IndexError, TypeError):
                continue
        return airplanes

    def to_dict(self):
        return {
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "altitude": self.altitude,
            "on_ground": self.on_ground,
        }

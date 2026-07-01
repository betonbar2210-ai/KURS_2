import requests
from src.baseclass import BaseAPIClient


class APIAdapter(BaseAPIClient):
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Gluyki/1.0 betonbar@bk.ru"})

    def get_country_coordinates(self, country_name):
        params = {"q": country_name, "format": "json", "limit": 1}
        try:
            response = self.session.get(self.NOMINATIM_URL, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if not data:
                    raise Exception(f"Страна '{country_name}' не найдена в Nominatim")

                if "boundingbox" not in data[0]:
                    raise Exception("Boundingbox отсутствует в ответе API")

                bbox = data[0]["boundingbox"]
                if len(bbox) != 4:
                    raise Exception("Неверный формат boundingbox")

                return {
                    "south": float(bbox[0]),
                    "north": float(bbox[1]),
                    "west": float(bbox[2]),
                    "east": float(bbox[3]),
                }
            else:
                raise Exception(f"Ошибка API Nominatim: {response.status_code}")
        except requests.exceptions.Timeout:
            raise Exception("Таймаут при запросе к Nominatim")
        except Exception as e:
            raise Exception(f"Ошибка при запросе к Nominatim: {str(e)}")

    def get_airplanes_in_area(self, south, north, west, east):
        params = {"lamin": south, "lamax": north, "lomin": west, "lomax": east}
        try:
            response = self.session.get(self.OPENSKY_URL, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data.get("states", []) if data else []
            else:
                raise Exception(f"Ошибка API OpenSky: {response.status_code}")
        except requests.exceptions.Timeout:
            raise Exception("Таймаут при запросе к OpenSky")
        except Exception as e:
            raise Exception(f"Ошибка при запросе к OpenSky: {str(e)}")

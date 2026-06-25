import json
import os

from config import ROOT_DIR
from src.airplane import Airplane
from src.baseclass import BaseFileSaver


class JSONSaver(BaseFileSaver):
    def __init__(self, filename: str = "airplanes.json"):
        self.filename = os.path.join(ROOT_DIR, "data", filename)
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def read_data(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    return []
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write_data(self, data):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_airplane(self, airplane: Airplane) -> None:
        data = self.read_data()
        data.append(airplane.to_dict())
        self.write_data(data)

    def get_airplanes(self, **filters):
        data = self.read_data()

        def matches(record):
            for key, value in filters.items():
                if key not in record:
                    return False
                if record[key] != value:
                    return False
            return True

        return [a for a in data if matches(a)]

    def delete_airplane(self, airplane: Airplane) -> bool:
        data = self.read_data()
        initial_len = len(data)
        data = [
            a
            for a in data
            if not (a.get("callsign") == airplane.callsign and a.get("origin_country") == airplane.origin_country)
        ]
        if len(data) == initial_len:
            return False
        self.write_data(data)
        return True

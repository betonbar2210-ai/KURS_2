from abc import ABC, abstractmethod

from src.airplane import Airplane


class BaseAPIClient(ABC):
    @abstractmethod
    def get_country_coordinates(self, country_name):
        pass

    @abstractmethod
    def get_airplanes_in_area(self, south, north, west, east):
        pass


class BaseFileSaver(ABC):
    @abstractmethod
    def add_airplane(self, airplane: Airplane):
        pass

    @abstractmethod
    def get_airplanes(self, **filters) -> list:
        pass

    @abstractmethod
    def delete_airplane(self, airplane: Airplane):
        pass

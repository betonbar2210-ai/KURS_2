import pytest

from src.airplane import Airplane




def test_airplane_init(air_fly_1):
    assert air_fly_1.callsign == "UPS496"
    assert air_fly_1.origin_country == "United States"
    assert air_fly_1.velocity == 194.9
    assert air_fly_1.altitude == 305.87
    assert air_fly_1.on_ground == False

def test_callsign_no(air_fly_1):
    with pytest.raises(ValueError, match="Позывной должен быть непустой строкой"):
        Airplane("", "United States", 194.9, 305.87, False)


def test_country_no_raises(air_fly_1):
    with pytest.raises(ValueError, match="Страна регистрации должна быть непустой строкой"):
        Airplane("UPS496", "", 194.9, 305.87, False)

def test_velocity_no_raises(air_fly_1):
    with pytest.raises(ValueError, match="Скорость не может быть отрицательной"):
        Airplane("UPS496", "United States", -1, 305.87, False)

def test_altitude_no_raises(air_fly_1):
    with pytest.raises(ValueError, match="Высота не может быть отрицательной"):
        Airplane("UPS496", "United States", 194.9, -100, False)


def test_lt_by_altitude(air_fly_1, air_fly_2):
    assert air_fly_1 < air_fly_2

def test_gt_by_altitude(air_fly_1, air_fly_2):
    assert air_fly_2 > air_fly_1

def test_compare_by_velocity_greater(air_fly_1, air_fly_2):
    assert air_fly_2.compare_by_velocity(air_fly_1) == 1

def test_compare_by_velocity_less(air_fly_1, air_fly_2):
    assert air_fly_1.compare_by_velocity(air_fly_2) == -1

def test_compare_by_velocity_equal(air_fly_2, air_fly_3):
    assert air_fly_2.compare_by_velocity(air_fly_3) == 0


def test_airplane_to_dict_(air_fly_3):
    data = air_fly_3.to_dict()
    assert data == {
        "callsign": "FRA50",
        "origin_country": "France",
        "velocity": 600,
        "altitude": 400,
        "on_ground": True,
    }



def test_cast_valid_open_sky_row(test_fly_1):
    planes = Airplane.cast_to_object_list(test_fly_1)
    assert len(planes) == 1
    p = planes[0]
    assert p.callsign == "UPS496"
    assert p.origin_country == "United States"
    assert p.velocity == 701.64
    assert p.altitude == 9144.0
    assert p.on_ground == False


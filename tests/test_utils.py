import pytest
from unittest.mock import MagicMock, patch
from src.utils import Airplane

def test_read_data_empty_or_missing(saver_with_temp_dir):
    assert saver_with_temp_dir.read_data() == []


def test_add_and_read_one_airplane(saver_with_temp_dir):
    plane = Airplane(
    callsign = "TEST123",
    origin_country = "TestLand",
    velocity = 0,
    altitude = 0,
    on_ground = True)
    saver_with_temp_dir.add_airplane(plane)

    data = saver_with_temp_dir.read_data()
    assert len(data) == 1
    assert data[0]["callsign"] == "TEST123"
    assert data[0]["origin_country"] == "TestLand"
    assert data[0]["velocity"] == 0
    assert data[0]["altitude"] == 0
    assert data[0]["on_ground"] == True


def test_add_multiple_airplanes_order(saver_with_temp_dir):
    planes = [
        Airplane(callsign=f"MULTI{i}", origin_country="Land", velocity = 0, altitude = 0, on_ground = True)
        for i in range(3)
    ]
    for p in planes:
        saver_with_temp_dir.add_airplane(p)

    data = saver_with_temp_dir.read_data()
    assert len(data) == 3
    assert [d["callsign"] for d in data] == ["MULTI0", "MULTI1", "MULTI2"]


def test_get_airplanes_filter_by_country(saver_with_temp_dir):
    planes = [
        Airplane(callsign = "1",
                origin_country = "USA",
                velocity = 0,
                altitude = 0,
                on_ground = True),
        Airplane(callsign = "2",
                origin_country = "USA",
                velocity = 0,
                altitude = 0,
                on_ground = True),
        Airplane(callsign = "3",
                origin_country = "Canada",
                velocity = 0,
                altitude = 0,
                on_ground = True),
    ]
    for p in planes:
        saver_with_temp_dir.add_airplane(p)

    result = saver_with_temp_dir.get_airplanes(origin_country="USA")
    assert len(result) == 2
    assert all(r["origin_country"] == "USA" for r in result)


def test_delete_airplane_success(saver_with_temp_dir):
    fly1 = Airplane(callsign = "1",
                origin_country = "USA",
                velocity = 0,
                altitude = 0,
                on_ground = True)
    fly2 = Airplane(callsign = "2",
                origin_country = "USA",
                velocity = 0,
                altitude = 0,
                on_ground = True)

    for f in [fly1, fly2]:
        saver_with_temp_dir.add_airplane(f)

    assert saver_with_temp_dir.delete_airplane(fly1) is True

    data = saver_with_temp_dir.read_data()
    assert len(data) == 1
    assert data[0]["callsign"] == "2"




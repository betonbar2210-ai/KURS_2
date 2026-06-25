import shutil
import tempfile

import pytest

import types
from unittest.mock import patch

from src.airplane import Airplane
from src.api_client import APIAdapter
from src.utils import JSONSaver


@pytest.fixture
def saver_with_temp_dir(monkeypatch):
    tmp_dir = tempfile.mkdtemp()
    monkeypatch.setattr("src.utils.ROOT_DIR", tmp_dir)
    try:
        yield JSONSaver(filename="test_airplanes.json")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


@pytest.fixture
def test_fly_1():
    return [['a53eef', 'UPS496', 'United States', 1782387534, 1782387534, -95.6289,
             46.154, 9144, False, 194.9, 305.87, 0, None, 9296.4, None, False, 0]]



@pytest.fixture
def adapter():
    return APIAdapter()


@pytest.fixture
def air_fly_1():
    return Airplane(
        callsign="UPS496",
        origin_country="United States",
        velocity=194.9,
        altitude=305.87,
        on_ground=False
    )


@pytest.fixture
def air_fly_2():
    return Airplane(
        callsign="RUS12",
        origin_country="Russia",
        velocity=600,
        altitude=1000,
        on_ground=True
    )



@pytest.fixture
def air_fly_3():
    return Airplane(
        callsign="FRA50",
        origin_country="France",
        velocity=600,
        altitude=400,
        on_ground=True
    )

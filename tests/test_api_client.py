from unittest.mock import MagicMock, patch

import pytest
import requests

from src.api_client import APIAdapter


def test_init_api(test_fly_1):
    mock_session = MagicMock()
    mock_session.get.return_value.json.return_value = test_fly_1

    with patch("requests.Session", return_value=mock_session):
        api = APIAdapter()
        assert api.session == mock_session


def test_country_coordinates(adapter):
    country = "Canada"
    expected_bbox = ["41.6765597", "83.3362128", "-141.00275", "-52.3237664"]
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "boundingbox": expected_bbox,
            "display_name": f"{country}, North America",
        }
    ]
    with patch.object(adapter.session, "get", return_value=mock_response) as mock_get:
        result = adapter.get_country_coordinates(country)
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args.kwargs["params"]["q"] == country
        assert call_args.kwargs["params"]["format"] == "json"
        assert call_args.kwargs["params"]["limit"] == 1
        assert call_args.kwargs["timeout"] == 10

        assert result == {
            "south": float(expected_bbox[0]),
            "north": float(expected_bbox[1]),
            "west": float(expected_bbox[2]),
            "east": float(expected_bbox[3]),
        }


def test_country_no(adapter):
    country = "NoName"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []

    with patch.object(adapter.session, "get", return_value=mock_response):
        with pytest.raises(Exception, match="не найдена"):
            adapter.get_country_coordinates(country)

def test_missing_boundingbox_raises(adapter):
    country = "Canada"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"display_name": country}]

    with patch.object(adapter.session, "get", return_value=mock_response):
        with pytest.raises(Exception, match="Boundingbox отсутствует"):
            adapter.get_country_coordinates(country)

def test_invalid_bbox_format_raises(adapter):
    country = "Canada"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"boundingbox": ["a", "b"]}]

    with patch.object(adapter.session, "get", return_value=mock_response):
        with pytest.raises(Exception, match="Неверный формат"):
            adapter.get_country_coordinates(country)

def test_nominatim_non_200_raises(adapter):
    country = "Canada"

    mock_response = MagicMock()
    mock_response.status_code = 503
    mock_response.json.side_effect = Exception("Не должен вызываться")

    with patch.object(adapter.session, "get", return_value=mock_response):
        with pytest.raises(Exception, match="Ошибка API Nominatim"):
            adapter.get_country_coordinates(country)

def test_nominatim_timeout_raises(adapter):
    country = "Canada"

    with patch.object(
            adapter.session,
            "get",
            side_effect=requests.exceptions.Timeout
    ):
        with pytest.raises(Exception, match="Таймаут при запросе к Nominatim"):
            adapter.get_country_coordinates(country)

def test_airplanes_in_area_ok(adapter, test_fly_1):
    south, north, west, east = 40.0, 50.0, -120.0, -100.0
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"states": test_fly_1}

    with patch.object(adapter.session, "get", return_value=mock_response) as mock_get:
        result = adapter.get_airplanes_in_area(south, north, west, east)
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        params = call_args.kwargs["params"]
        assert params["lamin"] == south
        assert params["lamax"] == north
        assert params["lomin"] == west
        assert params["lomax"] == east
        assert call_args.kwargs["timeout"] == 15

    assert result == test_fly_1

def test_airplanes_in_area_key_no(adapter):
    south, north, west, east = 40.0, 50.0, -120.0, -100.0

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"states": []}

    with patch.object(adapter.session, "get", return_value=mock_response):
        result = adapter.get_airplanes_in_area(south, north, west, east)
        assert result == []

def test_airplanes_in_area_no(adapter):
    south, north, west, east = 40.0, 50.0, -120.0, -100.0

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}

    with patch.object(adapter.session, "get", return_value=mock_response):
        result = adapter.get_airplanes_in_area(south, north, west, east)
        assert result == []


def test_opensky_no_200_raises(adapter):
    south, north, west, east = 40.0, 50.0, -120.0, -100.0

    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_response.json.side_effect = Exception("Не должен вызываться")

    with patch.object(adapter.session, "get", return_value=mock_response):
        with pytest.raises(Exception, match="Ошибка API OpenSky"):
            adapter.get_airplanes_in_area(south, north, west, east)

def test_opensky_timeout_raises(adapter):
    south, north, west, east = 40.0, 50.0, -120.0, -100.0

    with patch.object(
            adapter.session,
            "get",
            side_effect=requests.exceptions.Timeout
    ):
        with pytest.raises(Exception, match="Таймаут при запросе к OpenSky"):
            adapter.get_airplanes_in_area(south, north, west, east)


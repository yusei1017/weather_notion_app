def test_smoke():
    assert True
# tests/test_format_weather.py
from main import format_weather

def test_format_weather_returns_string():
    dummy_data = {
        "current": {
            "time": "2025-01-01T09:00",
            "temperature_2m": 10,
            "apparent_temperature": 8,
            "precipitation": 0,
            "wind_speed_10m": 5,
            "weather_code": 0,
        },
        "daily": {
            "temperature_2m_max": [12],
            "temperature_2m_min": [3],
            "precipitation_sum": [0],
        },
    }

    result = format_weather(dummy_data)

    assert isinstance(result, str)
    assert "気温" in result
    assert "最高" in result

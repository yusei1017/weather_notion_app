import sys
from pathlib import Path

# リポジトリ直下を import できるようにする
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from main import format_weather


def test_format_weather_smoke():
    data = {
        "current": {
            "time": "2025-01-01T00:00",
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

    out = format_weather(data)
    assert "気温" in out


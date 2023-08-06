from typing import Dict
from json import JSONDecodeError, loads


def _load_data(data: str) -> Dict:
    try:
        data = loads(data)
    except JSONDecodeError:
        return {}
    return data


def location_message_geo_uri(location_message: str) -> str:
    location_message_dict = _load_data(location_message)
    return location_message_dict.get("geo_uri", "")


def location_message_latitude(location_message: str) -> str:
    geo_uri = location_message_geo_uri(location_message=location_message)
    latitude, _ = geo_uri.split(":")[1].split(",")
    return latitude


def location_message_longitude(location_message: str) -> str:
    geo_uri = location_message_geo_uri(location_message=location_message)
    _, longitude = geo_uri.split(":")[1].split(",")
    return longitude


def google_location_url(geo_uri: str) -> str:
    latitude, longitude = geo_uri.split(":")[1].split(",")
    return f"https://www.google.com/maps?q={latitude},{longitude}"

from .matrix_filters import (
    google_location_url,
    location_message_geo_uri,
    location_message_latitude,
    location_message_longitude,
    user_bridge_account_id,
    user_bridge_info,
    user_bridge_prefix,
    user_homeserver,
)


class FilterModule(object):
    """Matrix jinja2 filters"""

    def filters(self):
        return {
            "user_bridge_info": user_bridge_info,
            "user_bridge_prefix": user_bridge_prefix,
            "user_bridge_account_id": user_bridge_account_id,
            "user_homeserver": user_homeserver,
            "location_message_geo_uri": location_message_geo_uri,
            "location_message_latitude": location_message_latitude,
            "location_message_longitude": location_message_longitude,
            "google_location_url": google_location_url,
        }

def user_homeserver(user_id: str) -> str:
    _, homeserver = user_id.split(":")
    return homeserver

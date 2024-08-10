DEBUG: dict[str, str] = {
    "on_bot_connected": "Bot successfully connected.",
    "on_client_connected": "Client successfully connected.",

    "flood_wait_error": "Flood for {seconds} in {title}.",
    "slow_mode_wait_error": "Slow mode for {seconds} in {title}",
    "channel_private_error": "You tried to send message in private chat {title}",
    "bad_message_error": "BadMessage error occurred in {title}.",
    "entity_existence_error": "Cannot find any entity corresponding to '{chat}'",
    "key_error": "Key error at {traceback}.",

    "config_changed": "File config.json was changed.",
}


def register(strings: dict) -> dict[str, dict[str, str]]:
    strings["debug"] = {}

    for item in DEBUG.items():
        strings["debug"][item[0]] = item[1]

    return strings

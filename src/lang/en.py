BOT: dict[str, str] = {
    "start": "Verification completed.",
    "posts_number": "Current number of posts: {number}.",
    "add_post": "Send new post.",
    "empty_list": "Post list is empty.",
    "choose_post": "Choose a post",
    "all": "All",
    "post_edited": "Post №{number} was edited.",
    "send_edited": "Send edited post.",
    "no_permissions": "You have no permissions.",
    "add_chat": "Sent new chat.",
    "unexpected_args": "You passed unexpected arguments.",
    "bad_link": "Link wasn't found.",
    "bad_time": "Time wasn't found."
}

CLIENT: dict[str, str] = {
    "post_sent": "Message has been sent into {title}"
}


def register(strings: dict) -> dict[str, dict[str, str]]:
    lang = "en"
    strings[lang] = {}

    for item in BOT.items():
        strings[lang][item[0]] = item[1]

    for item in CLIENT.items():
        strings[lang][item[0]] = item[1]

    return strings

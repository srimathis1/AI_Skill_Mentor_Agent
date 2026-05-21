import json
import os

CHAT_FILE = (
    "storage/chat_history.json"
)


def save_chat(
    username,
    message
):

    if not os.path.exists(
        "storage"
    ):
        os.makedirs(
            "storage"
        )

    if not os.path.exists(
        CHAT_FILE
    ):

        with open(
            CHAT_FILE,
            "w"
        ) as f:

            json.dump(
                {},
                f
            )

    with open(
        CHAT_FILE,
        "r"
    ) as f:

        chats = json.load(f)

    if username not in chats:
        chats[username] = []

    chats[username].append(
        message
    )

    with open(
        CHAT_FILE,
        "w"
    ) as f:

        json.dump(
            chats,
            f,
            indent=4
        )


def load_chat(
    username
):

    if not os.path.exists(
        CHAT_FILE
    ):
        return []

    with open(
        CHAT_FILE,
        "r"
    ) as f:

        chats = json.load(f)

    return chats.get(
        username,
        []
    )
import json

USER_FILE = (
    "storage/users.json"
)


def load_users():

    try:

        with open(
            USER_FILE,
            "r"
        ) as f:

            return json.load(f)

    except:

        return {}


def save_user(
    username,
    data
):

    users = load_users()

    users[username] = data

    with open(
        USER_FILE,
        "w"
    ) as f:

        json.dump(
            users,
            f,
            indent=4
        )
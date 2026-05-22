from flask import (
    Flask,
    jsonify
)

import json

app = Flask(
    __name__
)


@app.route(
    "/users"
)

def get_users():

    with open(
        "storage/users.json",
        "r"
    ) as f:

        users = json.load(
            f
        )

    return jsonify(
        users
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
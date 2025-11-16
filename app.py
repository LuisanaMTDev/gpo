import os
from io import StringIO

from dotenv import load_dotenv
from flask import Flask, abort, make_response, render_template, request
from redis import ConnectionPool, Redis

from sessions import (
    filter_sessions,
    get_unfiltered_sessions_as_list_of_dicts,
    get_unique_days_and_hours,
)

app = Flask(__name__)
_ = load_dotenv()
platform = os.getenv("PLATFORM")

match platform:
    case "DEV":
        redis_client = Redis(host="localhost", port=5002, db=0, decode_responses=True)
    case "PROD":
        redis_pool = ConnectionPool(
            host="localhost",
            port=5002,
            db=1,
            decode_responses=True,
            max_connections=5,
        )

        redis_client = Redis(connection_pool=redis_pool)
    case "TEST":
        redis_pool = ConnectionPool(
            host="localhost",
            port=5002,
            db=3,
            decode_responses=True,
            max_connections=5,
        )

        redis_client = Redis(connection_pool=redis_pool)
    case _:
        print("ERROR: platform is a unknown string (str)")
        abort(500)


# NOTE: for uwsgi
application = app


@app.get("/")
def index_page():
    return render_template("index.html")


@app.post("/send-file")
def get_csv_file():
    sessions_file = request.files["sessions_file"]
    with StringIO(sessions_file.stream.read().decode("UTF8"), newline=None) as stream:

    return render_template(
        "sessions_fragments.html",
        fragment="all_sessions",
        sessions=sessions,
        sessions = get_unfiltered_sessions_as_list_of_dicts(stream)
    )


# TODO: Add when have redis db ready
# when the user goes to this endpoint send then their sessions file or
# redirect them to / is there's none.
# @app.get("/sessions")


if __name__ == "__main__":
    app.run()

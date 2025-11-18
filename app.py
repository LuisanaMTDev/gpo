import os
import time
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
    # # NOTE: 604800 are the amount of seconds that 7 days has
    SF_EXPIRED_DATE = 60
    sessions_file = request.files.get("sessions_file")
    if sessions_file is None:
        # TODO: This should return a response with some html indicating the error
        abort(400)
    with StringIO(sessions_file.stream.read().decode("UTF8"), newline=None) as stream:
        sessions = get_unfiltered_sessions_as_list_of_dicts(stream)
        _ = stream.seek(0)
        days, hours = get_unique_days_and_hours(stream)
        sessions_for_db = stream.getvalue()

    timestamp = int(time.time())
    setted = redis_client.set(f"sf-{timestamp}", sessions_for_db, ex=SF_EXPIRED_DATE)
    if setted is False:
        abort(500)

    response = make_response(
        render_template(
            "sessions_fragments.html",
            fragment="all_sessions",
            sessions=sessions,
            days=days,
            hours=hours,
        )
    )
    response.set_cookie(
        key="sessions_file_key",
        value=f"sf-{timestamp}",
        max_age=SF_EXPIRED_DATE,
        httponly=True,
        # TODO: Add on production secure and samesite parameters.
    )

    return response

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

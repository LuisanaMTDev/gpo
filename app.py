from io import StringIO

from flask import Flask, render_template, request

from sessions import filter_sessions, get_sessions_as_list_of_dicts

app = Flask(__name__)

# NOTE: for uwsgi
application = app


@app.get("/")
def index_page():
    return render_template("index.html")


@app.post("/send-file")
def get_csv_file():
    sessions_file = request.files["sessions_file"]
    with StringIO(sessions_file.stream.read().decode("UTF8"), newline=None) as stream:
        sessions = get_sessions_as_list_of_dicts(stream)

    return render_template(
        "sessions_fragments.html",
        fragment="all_sessions",
        sessions=sessions,
    )


# TODO: Add when have redis db ready
# when the user goes to this endpoint send then their sessions file or
# redirect them to / is there's none.
# @app.get("/sessions")


if __name__ == "__main__":
    app.run()

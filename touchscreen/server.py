import sys, getopt
from flask import Flask
from flask import render_template
from flask import redirect

# Necessary for python pathing for `flask` command
import sys, os; sys.path.append(os.path.dirname(__file__))

from touchscreen.db import DB
from touchscreen.db import start_up
from touchscreen.db import get_application_mode
from touchscreen.db import set_application_mode


start_up()


app = Flask(__name__)


@app.before_request
def before_request():
    DB.connect()


@app.after_request
def after_request(response):
    DB.close()
    return response


@app.route("/")
def index(pathvar=""):
    current_mode = get_application_mode()
    print("OMFG", current_mode)

    return render_template(
        "index.html",
        mode=current_mode
    )


@app.route("/api/dj-mode")
def dj_mode():
    print("=========> dj mode")
    set_application_mode('autoplay')
    return "{}"


@app.route("/api/playlist")
def song_select():
    print("=========> playlist mode")
    set_application_mode('playlist')
    return "{}"


if __name__ == '__main__':
    # argv = sys.argv[1:]
    # opts, args = getopt.getopt(argv, "d", ["disco="])
    app.run(debug=True, host='0.0.0.0')
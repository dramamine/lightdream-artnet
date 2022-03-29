import sys, getopt
from flask import Flask
from flask import render_template
from flask import redirect

# Necessary for python pathing for `flask` command
import sys, os; sys.path.append(os.path.dirname(__file__))


app = Flask(__name__)


@app.route("/")
def index(pathvar=""):
  return render_template(
    "index.html",
    mode='playlist'
  )


@app.route("/api/dj-mode")
def dj_mode():
  return "{}"


@app.route("/api/playlist")
def song_select():
  return "{}"


if __name__ == '__main__':
  # argv = sys.argv[1:]
  # opts, args = getopt.getopt(argv, "d", ["disco="])
  app.run(debug=True, host='0.0.0.0')
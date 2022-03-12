from modes.playlist import Playlist
from modes.autoplay import Autoplay
from modules.artnet import show
from modules.filters import Filters

from util.config import config

from util.periodicrun import periodicrun
from time import time

if config['ENV'] == 'prod':
  from modules.alsa_input import get_energy
else:
  from modules.alsa_input_mock import get_energy


fps = 40

# "playlist" | "autoplay" | "metronome"
mode = config['MODE']

pl = Playlist()
ap = Autoplay()
filters = Filters()
# pl.test_metronome()
# audio_input.init()
# audio_input.open_stream()

if mode == "metronome":
  pl.test_metronome()
elif mode == "autoplay":
  ap.start()
elif mode == "playlist":
  pl.start()

def loop():
  if mode == "autoplay":
    frame = ap.tick()
    # @TODO apply fun filters based on song energy
    energy = get_energy()
  else:
    frame = pl.tick()

  frame = filters.apply_filters_numpy(frame)

  if config['ENV'] == "prod":
    show(frame)
  

def toggle_mode():
  if mode == "playlist":
    mode = "autoplay"
    ap.start()
  else:
    mode = "playlist"
    pl.restart()


start_time = time()
frame_counter = 0

# for debugging. can swap out for 'loop' for final build
def loop_timer():
  global frame_counter, start_time
  frame_counter = frame_counter + 1
  loop_timer = time()

  loop()

  # this should look pretty consistently as a multiple of 1
  if frame_counter % 40 == 0:
    print(time() - start_time)

  loop_time = time() - loop_timer
  if loop_time > 0.020:
    print("warning: loop took too long (needs to be < 0.025):", loop_time)

pr = periodicrun(1/fps, loop_timer, list(), 0, accuracy=0.025)
pr.run()

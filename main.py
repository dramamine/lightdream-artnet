from modes.playlist import Playlist
from modes.autoplay import Autoplay
from modules.artnet import show
from effects.effects import effects_manager

from util.config import config

from util.periodicrun import periodicrun
from time import time

import modules.audio_input.runner as audio_listener


from touchscreen.server import start_touchscreen_server
from touchscreen.server import get_application_mode

fps = 40

# "playlist" | "autoplay" | "metronome"
mode = config['MODE']


start_touchscreen_server(mode=mode)


pl = Playlist()
ap = Autoplay()
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
  if get_application_mode() == "autoplay":
    frame = ap.tick()
    # @TODO apply fun filters based on song energy
    energy = audio_listener.get_energy()
    # print(energy)
  else:
    frame = pl.tick()

  frame = effects_manager.apply_effects(frame)

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
  # if frame_counter % 40 == 0:
  #   print(time() - start_time)

  loop_time = time() - loop_timer
  if loop_time > 0.020:
    print("warning: loop took too long (needs to be < 0.025):", loop_time)

pr = periodicrun(1/fps, loop_timer, list(), 0, accuracy=0.025)

try:
  pr.run()
finally:
  audio_listener.thread_ender()

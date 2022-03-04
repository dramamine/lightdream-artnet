from modules.playlist import Playlist
from modules.autoplay import Autoplay
from modules.artnet import show
from modules.filters import Filters
from lib.periodicrun import periodicrun
from time import time

fps = 40

# "playlist" | "autoplay"
mode = "autoplay"

pl = Playlist()
ap = Autoplay()
filters = Filters()
# pl.test_metronome()



def loop():
  frame = pl.tick() if mode == "playlist" else ap.tick()

  # show(filters.apply_filters(frame))
  # filters.apply_filters_inplace(frame)
  frame = filters.apply_filters_numpy(frame)

  show(frame)
  

def toggle_mode():
  if mode == "playlist":
    mode = "autoplay"
    ap.restart()
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

  loop_time = loop_timer - time()
  if loop_time > 0.020:
    print("warning: loop took too long (needs to be < 0.025):", loop_time)

pr = periodicrun(1/fps, loop_timer, list(), 0, accuracy=0.025)
pr.run()

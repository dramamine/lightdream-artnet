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

start_time = time()
frame_counter = 0

def loop():
  global frame_counter, start_time
  frame_counter = frame_counter + 1

  frame = pl.tick() if mode == "playlist" else ap.tick()
  
  filter_time = time()

  show(filters.apply_filters(frame))
  # filters.apply_filters_inplace(frame)
  # show(frame)

  print("runtime was:", time() - filter_time)

  if frame_counter % 40 == 0:
    print( time() - start_time )

def toggle_mode():
  if mode == "playlist":
    mode = "autoplay"
    ap.restart()
  else:
    mode = "playlist"
    pl.restart()

pr = periodicrun(1/fps, loop, list(), 0, accuracy=0.025)
pr.run()

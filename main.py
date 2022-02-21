from modules.playlist import Playlist
from modules.artnet import show
from time import sleep, time
from lib.periodicrun import periodicrun
fps = 40

pl = Playlist()
# pl.test_metronome()

# start_time = time()
# frame_counter = 0

def loop():
  # global frame_counter, start_time
  # frame_counter = frame_counter + 1
  frame = pl.tick()
  # print(frame)
  show( frame )

  # if frame_counter % 40 == 0:
  #   print( time() - start_time )


pr = periodicrun(0.025, loop, list(), 0, accuracy=0.025)
pr.run()

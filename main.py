from modules.playlist import Playlist
from modules.artnet import show
from time import sleep
fps = 40

pl = Playlist()
pl.test_metronome()

while(True):
  frame = pl.tick()
  # print(frame)
  show( frame )
  # @TODO use precision timer instead of this
  sleep(1/fps)
  # sleep(5)

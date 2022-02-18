from modules.playlist import Playlist
from time import sleep

fps = 40

pl = Playlist()

while(True):
  pl.tick()
  # @TODO use precision timer instead of this
  sleep(1/fps)

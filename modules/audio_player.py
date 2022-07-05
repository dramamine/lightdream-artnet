import os
from util.config import config
from kivy.core.audio import SoundLoader
from util.track_metadata import tracks

from time import time

start_time = time()
print("cacheing music files")
sounds = dict()
for track_name in tracks:
  sounds[track_name] = SoundLoader.load(os.path.join('audio', '{}.ogg'.format(track_name)))
print("they is cached", time() - start_time)

class AudioPlayer:
  sound = None
  def play(self, track_name):
    print("loading...")
    start_time = time()
    self.sound = sounds[track_name]
    print("loaded.", time() - start_time)
    # player.queue(source)

    if config.read("DISABLE_AUDIO") == True:
      self.sound.volume = 0

    print("calling sound.play:")
    self.sound.play()
    print("its played")
    

  def is_playing(self):
    if self.sound:
      return self.sound.state == "play"
    return False

  # @TODO needs testing, i.e. doesn't work
  def stop(self):
    if self.sound:
      self.sound.stop()
  
  def skip_track(self):
    if self.sound:
      self.sound.stop()

  def clear(self):
    if self.sound:
      self.sound.stop()

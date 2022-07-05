import os
from util.config import config
from kivy.core.audio import SoundLoader
from util.track_metadata import tracks

from time import time

start_time = time()
print("audio: music files loading")
sounds = dict()
for track_name in tracks:
  sounds[track_name] = SoundLoader.load(os.path.join('audio', '{}.ogg'.format(track_name)))
print("audio: music files cached", time() - start_time)

class AudioPlayer:
  sound = None
  def play(self, track_name):
    start_time = time()
    self.sound = sounds[track_name]
    # player.queue(source)

    if config.read("DISABLE_AUDIO") == True:
      self.sound.volume = 0

    self.sound.play()
    

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

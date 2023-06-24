import os
from util.config import config
from kivy.core.audio import SoundLoader
from util.track_metadata import tracks
import pickle

from time import time

sounds = dict()

if (config.read("USE_PRELOADED_AUDIO")):
  with open('sounds.pickle', 'rb') as handle:
      sounds = pickle.load(handle)
else:
  start_time = time()
  print("audio: music files loading")
  sounds = dict()
  for track_name in tracks:
    print(f"loading {track_name}")
    sounds[track_name] = SoundLoader.load(os.path.join('audio', '{}.ogg'.format(track_name)))
  sounds['metronome'] = SoundLoader.load(os.path.join('audio', 'metronome.wav'))
  print(f"audio: music files cached in {(time() - start_time):.1f} seconds")

  with open('sounds.pickle', 'wb') as handle:
      pickle.dump(sounds, handle, protocol=pickle.HIGHEST_PROTOCOL)

class AudioPlayer:
  sound = None
  def play(self, track_name):
    self.sound = sounds[track_name]

    if config.read("DISABLE_AUDIO") == True:
      self.sound.volume = 0

    self.sound.play()
    

  def is_playing(self):
    if self.sound:
      return self.sound.state == "play"
    return False

  # @TODO needs testing, i.e. doesn't work or are these unused / repetitive
  def stop(self):
    if self.sound:
      self.sound.stop()
  
  def skip_track(self):
    if self.sound:
      self.sound.stop()

  def clear(self):
    if self.sound:
      self.sound.stop()

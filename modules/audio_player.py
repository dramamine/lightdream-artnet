import os
from util.config import config
from kivy.core.audio import SoundLoader
from util.track_metadata import tracks

import time

#start_time = time()
#print("audio: music files loading")
sounds = dict()
# for track_name in tracks:
#   print(f"loading {track_name}")
#   sounds[track_name] = SoundLoader.load(os.path.join('audio', '{}.ogg'.format(track_name)))
# sounds['metronome'] = SoundLoader.load(os.path.join('audio', 'metronome.wav'))
# print(f"audio: music files cached in {(time() - start_time):.1f} seconds")

class AudioPlayer:
  sound = None
  def play(self, track_name):
    print("starting audio:", track_name)
    self.sound = sounds[track_name]

    if config.read("DISABLE_AUDIO") == True:
      self.sound.volume = 0

    self.sound.play()
    
  def load(self, track_name):
    print(f"loading track: {track_name}")
    sounds[track_name] = SoundLoader.load(os.path.join('audio', '{}.ogg'.format(track_name)))
    time.sleep(5)
    print("done loading track")

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

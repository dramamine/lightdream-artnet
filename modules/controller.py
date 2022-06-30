from util.util import nullframe
from modes.playlist import Playlist
from modes.autoplay import Autoplay
from util.config import config
from effects.effects import effects_manager
from modules.fingers import finger_manager

class Controller:
  def __init__(self, mode):
    self.frame = nullframe
    self.mode = mode
    self.pl = Playlist()
    self.ap = Autoplay()

    self.start(mode)
    pass
  
  def start(self, mode):
    if mode == "metronome":
      self.pl.test_metronome()
    elif mode == "autoplay":
      self.ap.start()
    elif mode == "playlist":
      self.pl.start()

  def set_mode(self, next_mode):
    if self.mode == next_mode:
      return
    self.mode = next_mode
    if next_mode == "autoplay":
      self.pl.stop()
      config.write("MODE", "autoplay")
      self.ap.start()
    elif next_mode == "playlist":
      config.write("MODE", "playlist")
      self.pl.clear()
      self.pl.start()
    elif next_mode == "metronome":
      config.write("MODE", "metronome")
      self.pl.test_metronome()
  
  def get_frame(self):
    return self.frame

  def update_frame(self):
    if self.mode == "autoplay":
      frame = self.ap.tick()
    else:
      frame = self.pl.tick()

    frame = effects_manager.apply_effects(frame, finger_manager)

    self.frame = frame

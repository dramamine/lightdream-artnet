import os
import random
import time
from modules.sequence_player import SequencePlayer
from effects.aural import aural
import numpy as np
from util.config import config

# all blacks
nullframe = np.zeros((30,512))

files = [x for x in os.listdir( os.path.join('video', 'autoclips')) if x.endswith('.mp4')]

def numpy_mixer(frame_a, frame_b, mix):
  return frame_a * (1-mix) + frame_b * mix

class Autoplay:
  def __init__(self):
    pass

  def start(self):
    random.shuffle(files)
    self.idx = 0

    self.spa = SequencePlayer(loop=True)
    self.spa.play(os.path.join('video', 'autoclips', files[self.idx]))
    self.spa_active = True

    self.spb = SequencePlayer(loop=True)
    self.spb_active = False

    self.timer = time.time()
    return self

  def crossfade_to_next_track(self):
    self.idx = (self.idx+1) % len(files)

    if self.idx % 2 == 1:
      # print("need to activate b")
      self.spb.play(os.path.join('video', 'autoclips', files[self.idx]))
      self.spb_active = True
    else:
      # print("need to activate a")
      self.spa.play(os.path.join('video', 'autoclips', files[self.idx]))
      self.spa_active = True
    
   #  print("started playing:", files[self.idx])
    self.timer = time.time()
    aural.rotate_aural_effects()
    pass

  def tick(self):
    time_since = time.time() - self.timer
    # print(time_since)
    if time_since > config.read("autoplay_interval"):
      self.crossfade_to_next_track()
      time_since = 0
    
    if time_since > config.read("autoplay_crossfade"):
      # deactivate one of them
      if self.spa_active and self.idx % 2 == 1:
        # print("deactivating a")
        self.spa_active = False
      elif self.spb_active and self.idx % 2 == 0:
        # print("deactivating b")
        self.spb_active = False

    if self.spa_active and self.spb_active:
      mix = time_since / config.read("autoplay_crossfade")
      if self.idx % 2 == 1:
        # print("fading from a to b", mix)
        # return self.spa.read_frame()
        return numpy_mixer(self.spa.read_frame(), self.spb.read_frame(), mix)
      else:
        # print("fading from b to a", mix)
        # return self.spb.read_frame()
        return numpy_mixer(self.spb.read_frame(), self.spa.read_frame(), mix)

    elif self.spa_active:
      return self.spa.read_frame()
    elif self.spb_active:
      return self.spb.read_frame()

    print("Error: neither SequencePlayer was marked as active")
    return nullframe

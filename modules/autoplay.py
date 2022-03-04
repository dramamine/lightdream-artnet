import os
import random
import time
from modules.sequence_player import SequencePlayer
import numpy as np
# from modules.filters import mixer

# all blacks
nullframe = np.zeros((30,512))

files = [x for x in os.listdir( os.path.join('video', 'autoclips')) if x.endswith('.mp4')]

INTERVAL = 50
CROSSFADE = 5

# mix (float): 0-1, 0 being all A, 1, being all B
def row_mixer(row_a, row_b, mix):
  return list(map(lambda a, b: round(a * (1-mix) + b * mix), row_a, row_b))

# mix (float): 0-1, 0 being all A, 1, being all B
def mixer(frame_a, frame_b, mix):
  return list(map(lambda a, b: row_mixer(a, b, mix), frame_a, frame_b))

class Autoplay:
  def __init__(self):
    self.restart()

  def restart(self):
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
    pass

  def tick(self):
    time_since = time.time() - self.timer
    # print(time_since)
    if time_since > INTERVAL:
      self.crossfade_to_next_track()
      time_since = 0
    
    if time_since > CROSSFADE:
      # deactivate one of them
      if self.spa_active and self.idx % 2 == 1:
        # print("deactivating a")
        self.spa_active = False
      elif self.spb_active and self.idx % 2 == 0:
        # print("deactivating b")
        self.spb_active = False

    if self.spa_active and self.spb_active:
      mix = time_since / CROSSFADE
      if self.idx % 2 == 1:
        # print("fading from a to b", mix)
        return mixer(self.spa.read_frames(), self.spb.read_frames(), mix)
      else:
        # print("fading from b to a", mix)
        return mixer(self.spb.read_frames(), self.spa.read_frames(), mix)

    elif self.spa_active:
      return self.spa.read_frames()
    elif self.spb_active:
      return self.spb.read_frames()

    print("Error: neither SequencePlayer was marked as active")
    return nullframe

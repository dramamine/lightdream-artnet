from modules.sequence_player import SequencePlayer
import os
import numpy as np
import cv2
from util.util import remove_unused_pixels_from_frame

def prefer_a(a, b):
  if a > 0:
    return a
  return b

prefer_a_vectorized = np.vectorize(prefer_a)

# these straight-up replace the input frame
class SourceEffect:
  def __init__(self, key):
    self.key = key
    self.sp = SequencePlayer(loop=True)
    self.sp.play(os.path.join('video', 'sources', "{}.mp4".format(key)))


  def apply(self, frame, fingers):
    if not fingers:
      return frame
    
    source = self.sp.read_frame()
    return prefer_a_vectorized(source, frame)

class SourceEffect2:
  def __init__(self, key, count):
    self.key = key
    self.count = count
    self.frame_idx = 0

  def read_frame(self, key, idx):
    assert(idx >= 0)
    assert(idx <= self.count)
    idx_str = '{:02d}'.format(idx)
    frame = cv2.imread(os.path.join('video', 'sources', key,
      '{}{}.png'.format(key, idx_str)))
    return remove_unused_pixels_from_frame(frame)

  def apply(self, frame, fingers):
    if not fingers:
      return frame

    self.frame_idx = (self.frame_idx + 1) % self.count
    source = self.read_frame(self.key, self.frame_idx)
    return prefer_a_vectorized(source, frame)

class SourceEffect3:
  def __init__(self, key, count):
    self.key = key
    self.count = count
    self.frame_idx = 0

    # frame cache
    self.frames_cache = list(map(
      lambda x: remove_unused_pixels_from_frame( cv2.imread(os.path.join(
        'video', 'sources', key, # folder
        '{}{}.png'.format(key, '{:02d}'.format(x)) # filename
      ))),
      range(count)
    ))

  def read_frame(self, idx):
    assert(idx >= 0)
    assert(idx <= self.count)
    return self.frames_cache[idx]

  def apply(self, frame, fingers):
    if not fingers:
      return frame

    self.frame_idx = (self.frame_idx + 1) % self.count
    source = self.read_frame(self.frame_idx)
    return prefer_a_vectorized(source, frame)

radiant = SourceEffect("radiant")
triforce = SourceEffect("triforce")
lightning = SourceEffect3("lightning", 80)

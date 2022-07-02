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


class SourceEffectCached:
  def __init__(self, key, count):
    self.key = key
    self.count = count
    self.frame_idx = 0

    # frame cache
    format_str = '{:02d}' if count < 100 else '{:03d}'
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
    return source


class SourceEffectCachedVideo:
  def __init__(self, key):
    self.key = key

    self.sp = SequencePlayer(loop=False)
    self.sp.play(os.path.join('video', 'sources', "{}.mp4".format(key)))

    self.frames_cache = []
    self.frame_idx = 0

    frame = self.sp.read_frame()
    while not self.sp.ended:
      self.frames_cache.append(frame)
      frame = self.sp.read_frame()
    
    self.count = len(self.frames_cache)
    print(f"loaded {self.count} frames from source effect video: {key}")

  def read_frame(self, idx):
    assert(idx >= 0)
    assert(idx <= self.count)
    return self.frames_cache[idx]

  def apply(self, frame, fingers):
    if not fingers:
      return frame

    self.frame_idx = (self.frame_idx + 1) % self.count
    source = self.read_frame(self.frame_idx)
    return source

radiant = SourceEffectCachedVideo("radiant")
triforce = SourceEffectCachedVideo("triforce2")
#lightning = SourceEffectCached("lightning", 80)
lightning = SourceEffectCachedVideo("lightning")

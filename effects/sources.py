from effects.filters import FilterNames
from modules.sequence_player import SequencePlayer
import os
import numpy as np

def prefer_a(a, b):
  if a > 0:
    return a
  return b

prefer_a_vectorized = np.vectorize(prefer_a)

class SourceEffectCachedVideo:
  def __init__(self, key):
    self.key = key
    self.cache_video(os.path.join('video', 'sources', "{}.mp4".format(key)))

  def cache_video(self, path):
    sp = SequencePlayer(loop=False)
    sp.play(path)

    self.frames_cache = []
    self.frame_idx = 0

    frame = sp.read_frame()
    while not sp.ended:
      self.frames_cache.append(frame)
      frame = sp.read_frame()

    self.count = len(self.frames_cache)

  def read_frame(self):
    self.frame_idx = (self.frame_idx + 1) % self.count
    assert(self.frame_idx >= 0)
    assert(self.frame_idx <= self.count)
    return self.frames_cache[self.frame_idx]

  def apply(self, frame, fingers):
    if not fingers:
      return frame

    self.frame_idx = (self.frame_idx + 1) % self.count
    source = self.read_frame()
    return source

radiant = SourceEffectCachedVideo(FilterNames.RADIANTLINES)

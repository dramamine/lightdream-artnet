from modules.sequence_player import SequencePlayer
import os
import numpy as np

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

radiant = SourceEffect("radiant")
triforce = SourceEffect("triforce")
lightning = SourceEffect("lightning")

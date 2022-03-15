from modules.sequence_player import SequencePlayer
import os

# these straight-up replace the input frame
class SourceFilter:
  def __init__(self, filename):
    self.sp = SequencePlayer(loop=True)
    self.sp.play(os.path.join('video', 'sources', filename))
  
  def apply(self, frame):
    source = self.sp.read_frame()
    return source

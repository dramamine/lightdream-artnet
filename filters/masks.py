from modules.sequence_player import SequencePlayer
import os

class MaskFilter:
  def __init__(self, filename):
    self.sp = SequencePlayer(loop=True)
    self.sp.play(os.path.join('video', 'masks', filename))
  
  def apply(self, frame):
    mask = self.sp.read_frame().astype(bool)
    return frame * mask


nuclearFilter = MaskFilter("nuclear.mp4")
blobsFilter = MaskFilter("blobs.mp4")
spiralFilter = MaskFilter("spiral.mp4")

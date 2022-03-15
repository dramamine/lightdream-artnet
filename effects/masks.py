from modules.sequence_player import SequencePlayer
import os

class MaskEffect:
  def __init__(self, filename):
    self.sp = SequencePlayer(loop=True)
    self.sp.play(os.path.join('video', 'masks', filename))
  
  def apply(self, frame):
    mask = self.sp.read_frame().astype(bool)
    return frame * mask


nuclearEffect = MaskEffect("nuclear.mp4")
blobsEffect = MaskEffect("blobs.mp4")
spiralEffect = MaskEffect("spiral.mp4")

from modules.sequence_player import SequencePlayer
import os

class MaskEffect:
  def __init__(self, key):
    self.key = key

    self.sp = SequencePlayer(loop=True)
    self.sp.play(os.path.join('video', 'masks', "{}.mp4".format(key)))
  
  def apply(self, frame, fingers):
    if not fingers:
      return frame
    mask = self.sp.read_frame().astype(bool)
    return frame * mask


nuclear = MaskEffect("nuclear")
blobs = MaskEffect("blobs")
spiral = MaskEffect("spiral")

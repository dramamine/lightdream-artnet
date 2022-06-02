from util.config import config
import modules.audio_input.runner as audio_listener
from util.util import make_rgb_frame

effects = [
  lambda x: [0+x, 0, 0],
  lambda x: [0, 0+x, 0],
  lambda x: [0, 0, 0+x],
  lambda x: [0+x, 0+x, 0],
  lambda x: [0, 0+x, 0+x],
  lambda x: [0+x, 0, 0+x],
  lambda x: [0+x, 0+x, 0+x],
]

class Aural:
  def __init__(self):
    self.key = "aural"
    self.effect_idx = 0
    pass

  def value_to_frame_idx(self, value):
    return round(self.count * value)

  def rotate_aural_effects(self):
    self.effect_idx = (self.effect_idx + 1) % len(effects)

  # frame: the frame to which we apply this effect
  # fingers: a list of parameters 0-1
  def apply(self, frame, fingers):
    mode = config.read("MODE")
    if mode != "autoplay":
      return frame
    
    energy = audio_listener.get_visual_strength() * config.read("aural_effect_strength_multiplier")
    enhanced = effects[self.effect_idx](255 * energy)
    return frame + make_rgb_frame(enhanced)

aural = Aural()

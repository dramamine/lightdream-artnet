import math
from random import random
from util.config import config
import modules.audio_input.runner as audio_listener
from util.util import make_rgb_frame, numpy_mixer, scale_to
from effects.filters import wedges


effects = [
  lambda x: [0+x, 0, 0],
  lambda x: [0, 0+x, 0],
  lambda x: [0, 0, 0+x],
  lambda x: [0+x, 0+x, 0],
  lambda x: [0, 0+x, 0+x],
  lambda x: [0+x, 0, 0+x],
]

speed = 0.005
wedge_effects = [
  lambda ticks: [(ticks * speed) % 1, (ticks * speed + 0.5) % 1],
  lambda ticks: [(ticks * speed) % 1, (ticks * speed + 0.33) % 1, (ticks * speed + 0.66) % 1],
  lambda ticks: [(-ticks * speed) % 1, (-ticks * speed + 0.5) % 1],
  lambda ticks: [(-ticks * speed) % 1, (-ticks * speed + 0.33) % 1, (-ticks * speed + 0.66) % 1],
]

effects_count = len(effects) + 1


class Aural:
  def __init__(self):
    self.key = "aural"
    self.ticks = 0

    self.effect_variation_idx = 0
    self.active_effect = self.apply_basic_effects

    pass

  def value_to_frame_idx(self, value):
    return round(self.count * value)

  def rotate_aural_effects(self):
    x = random()
    if x < .8:
      self.active_effect = self.apply_basic_effects
      self.effect_variation_idx = math.floor( len(effects) * (x / .8) )
    else:
      self.active_effect = self.apply_wedge_effects
      self.effect_variation_idx = math.floor( len(wedge_effects) * ((x-.8) / .2) )
    print("updated effects:", x, self.active_effect, self.effect_variation_idx)

  # frame: the frame to which we apply this effect
  # fingers: a list of parameters 0-1
  def apply(self, frame, fingers):
    mode = config.read("MODE")
    if mode != "autoplay":
      return frame
    
    return self.active_effect(frame)
    

  def apply_basic_effects(self, frame):
    energy = audio_listener.get_visual_strength() * config.read("aural_effect_strength_multiplier")
    enhanced = effects[self.effect_variation_idx](255 * energy)
    return frame + make_rgb_frame(enhanced)

  def apply_wedge_effects(self, frame):
    self.ticks += 1
    values_fn = wedge_effects[self.effect_variation_idx]
    energy = audio_listener.get_visual_strength()
    # er, these values would be fun for rings
    # speed = 60
    # values_to_use = [math.sin(self.ticks / speed), 1-math.sin(self.ticks / speed)]

    # energy = scale_to(energy, 0,1, 0.5,1) 

    wedge_frame = wedges.apply(frame, values_fn(self.ticks))
    return numpy_mixer(wedge_frame, frame, scale_to(energy, (0,1), (0, 0.5)))
    

aural = Aural()

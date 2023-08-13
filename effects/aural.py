import math
from random import random
from util.config import config
import modules.audio_input.runner as audio_listener
from util.util import make_rgb_frame, numpy_mixer, scale_to
from effects.filters import wedges, rings, reveal


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

wave_speed = 0.04
ring_effects = [
  lambda ticks: [
    (.5 + .5*(math.cos(ticks * wave_speed))) % 1, 
    (.5 - .5*(math.cos(ticks * wave_speed))) % 1
  ],
  lambda ticks: [(ticks * speed) % 1, (ticks * speed + 0.5) % 1],
  lambda ticks: [(-ticks * speed) % 1, (-ticks * speed + 0.5) % 1],
]

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
    breakpoint_a = config.read("chance_basic_effects")
    breakpoint_b = breakpoint_a + config.read("chance_wedge_effects")
    breakpoint_c = breakpoint_b + config.read("chance_ring_effects")

    if x < breakpoint_a:
      self.active_effect = self.apply_basic_effects
      self.effect_variation_idx = math.floor( len(effects) * (x / config.read("chance_basic_effects")) )
    elif x < breakpoint_b:
      self.active_effect = self.apply_wedge_effects
      self.effect_variation_idx = math.floor( len(wedge_effects) * ((x-breakpoint_a) / config.read("chance_wedge_effects")) )
    elif x < breakpoint_c:
      self.active_effect = self.apply_ring_effects
      self.effect_variation_idx = math.floor( len(ring_effects) * ((x-breakpoint_b) / config.read("chance_ring_effects")) )
    else:
      self.active_effect = self.apply_reveal_effects

    print(f"updated effects: {self.active_effect.__name__} variation {self.effect_variation_idx}")

  # frame: the frame to which we apply this effect
  # fingers: a list of parameters 0-1
  def apply(self, frame, fingers):
    return frame
    
  def apply_basic_effects(self, frame):
    energy = audio_listener.get_visual_strength() * config.read("aural_effect_strength_multiplier")
    enhanced = effects[self.effect_variation_idx](255 * energy)
    return frame + make_rgb_frame(enhanced)

  def apply_wedge_effects(self, frame):
    values_fn = wedge_effects[self.effect_variation_idx]
    energy = audio_listener.get_visual_strength()

    wedge_frame = wedges.apply(frame, values_fn(self.ticks))
    return numpy_mixer(wedge_frame, frame, scale_to(energy, (0,1), (0, 0.5)))
    
  def apply_ring_effects(self, frame):
    values_fn = ring_effects[self.effect_variation_idx]
    energy = audio_listener.get_visual_strength()

    ring_frame = rings.apply(frame, values_fn(self.ticks))
    return numpy_mixer(ring_frame, frame, scale_to(energy, (0,1), (0, 0.5)))

  def apply_reveal_effects(self, frame):
    energy = audio_listener.get_visual_strength()

    reveal_frame = reveal.apply(frame, [energy])
    return numpy_mixer(frame, reveal_frame, config.read("aural_effect_strength_reveal"))

aural = Aural()

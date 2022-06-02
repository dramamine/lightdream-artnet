from math import ceil
import numpy as np
import effects.filters as filters
import effects.reshapers as reshapers
import effects.masks as masks
import effects.sources as sources
import effects.aural as aural
from util.config import config

class EffectsManager:
  def __init__(self):

    self.source_effects = [
      sources.lightning,
      sources.radiant,
      sources.lightning
    ]
    self.mask_effects = [
      masks.nuclear,
      masks.blobs,
      masks.spiral
    ]
    self.filter_effects = [
      filters.rings,
      filters.wedges,
      filters.rainbow,
      filters.hueshift,
      filters.brightness,
      filters.validate,
    ]
    self.reshaper_effects = [
      reshapers.tunnel,
      reshapers.kaleidoscope
    ]
    self.audio_based_effects = [
      aural.aural
    ]

  
  def apply_brightness(self, frame):
    return np.multiply(frame, config.read("brightness"))
    
  # note that 'frame' could be dtype uint8 or float64 at this point.
  # but output has gotta be uint8 so we can convert to bytearray later.
  def apply_effects(self, frame, finger_manager):
    # print("before:", frame[0][0], frame[0][1], frame[0][2])

    for effects_list in [self.source_effects, self.mask_effects, self.filter_effects, self.audio_based_effects, self.reshaper_effects]:
      for effect in effects_list:
        frame = effect.apply(frame, finger_manager.get_values(effect.key) )

    frame = np.minimum(frame, 255)
    frame = np.maximum(frame, 0)
    frame = frame.astype(np.uint8)

    # print("after:", frame[0][0], frame[0][1], frame[0][2])
    return frame

effects_manager = EffectsManager()

from math import ceil
import numpy as np
import effects.filters as filters

class EffectsManager:
  def __init__(self, brightness = 0.5):

    self.source_effects = []
    self.mask_effects = []
    self.filter_effects = [
      filters.rings_filter,
      filters.wedges_filter,
      filters.hueshift_filter,
      filters.brightness_filter,
      filters.validate_filter
    ]
    
    self.set_brightness(brightness)

  def set_brightness(self, brightness):
    assert(brightness >= 0.0)
    assert(brightness <= 1.0)
    self.brightness = brightness
  
  def apply_brightness(self, frame):
    return np.multiply(frame, self.brightness)

  # note that 'frame' could be dtype uint8 or float64 at this point.
  # but output has gotta be uint8 so we can convert to bytearray later.
  def apply_effects(self, frame, finger_manager):
    # print("before:", frame[0][0], frame[0][1], frame[0][2])

    for effects_list in [self.source_effects, self.mask_effects, self.filter_effects]:
      for effect in effects_list:
        frame = effect.apply(frame, finger_manager.get_values(effect.key) )

    frame = np.minimum(frame, 255)
    frame = np.maximum(frame, 0)
    frame = frame.astype(np.uint8)

    # print("after:", frame[0][0], frame[0][1], frame[0][2])
    return frame

effects_manager = EffectsManager()

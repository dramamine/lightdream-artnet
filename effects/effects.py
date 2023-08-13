import numpy as np
import effects.filters as filters
import effects.aural as aural

class EffectsManager:
  def __init__(self):
    self.filter_effects = [
      filters.brightness,
      filters.validate,
    ]
    self.audio_based_effects = [
      aural.aural
    ]
    
  # note that 'frame' could be dtype uint8 or float64 at this point.
  # but output has gotta be uint8 so we can convert to bytearray later.
  def apply_effects(self, frame, finger_manager):
    for effects_list in [self.filter_effects, self.audio_based_effects]:
      for effect in effects_list:
        frame = effect.apply(frame, finger_manager.get_values(effect.key) )

    frame = np.minimum(frame, 255)
    frame = np.maximum(frame, 0)
    frame = frame.astype(np.uint8)

    return frame

effects_manager = EffectsManager()

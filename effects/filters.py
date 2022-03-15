import numpy as np

# these straight-up replace the input frame
class BrightnessFilter:
  def __init__(self, brightness):
    self.brightness = brightness

  def set_brightness(self, brightness):
    assert(brightness >= 0.0)
    assert(brightness <= 1.0)
    self.brightness = brightness
  
  def apply(self, frame):
    return np.multiply(frame, self.brightness)

brightness_filter = BrightnessFilter(0.5)

class ValidateFilter:
  def apply(self, frame):
    frame = np.minimum(frame, 255)
    frame = np.maximum(frame, 0)
    frame = frame.astype(np.uint8)
    return frame

validate_filter = ValidateFilter()

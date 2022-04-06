import numpy as np
from util.hsv2rgb import hsv2rgb
from util.util import numpy_mixer

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

class HueshiftFilter:
  # static method
  # do multiple fingers touch the huewheel? if so,
  # find a nice in-between value
  def reduce_fingers(self, fingersArray):
    return np.average(
      np.add(fingersArray, range(len(fingersArray)))
    ) % 1

  def apply(self, frame, fingers):
    # float in 0-1 range
    val = self.reduce_fingers(fingers)

    # convert to hue. red is up
    # ex. [255,0,0]
    rgb = hsv2rgb(val*360, 1, 1)
    return numpy_mixer(frame, rgb, 0.5)

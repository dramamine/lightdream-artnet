import math
from modules.sequence_player import SequencePlayer
import numpy as np
from util.config import config
from util.hsv2rgb import hsv2rgb
from util.util import make_rgb_frame, numpy_mixer, remove_unused_pixels_from_frame, to_polar
from time import time
import os
import cv2


class FilterNames:
  # HUESHIFT = 'hueshift'
  KALEIDOSCOPE = 'kaleidoscope'
  TUNNEL = 'tunnel'

  RADIANTLINES = 'radiant'
  NUCLEAR = 'nuclear'
  SPIRAL = 'spiral'

  RINGS = 'rings'
  WEDGES = 'wedges'

  CIRCULAR_REVEAL = 'circular-reveal'

# these straight-up replace the input frame
class BrightnessFilter:
  def __init__(self):
    self.key = 'brightness'

  def apply(self, frame, _unused):
    brightness = config.read("brightness")
    return np.multiply(frame, brightness)

brightness = BrightnessFilter()

class ValidateFilter:
  def __init__(self):
    self.key = 'validate'

  def apply(self, frame, _unused):
    frame = np.minimum(frame, 255)
    frame = np.maximum(frame, 0)
    frame = frame.astype(np.uint8)
    return frame

validate = ValidateFilter()

class ImageFilter:
  def __init__(self, key, count):
    self.key = key
    self.count = count
    self.frames_cache = self.cache_images(key, count)
    print(f"done cacheing images for {key}")

  def cache_images(self, key, count):
    # TODO just use a map or whatever
    res = []
    for i in range(count):
      res.append(
        cv2.imread(os.path.join('video', 'overlays', key,
        '{}{}.png'.format(key, '{:03d}'.format(i))))
      )
    return res

  def read_frame(self, idx):
    assert(idx >= 0)
    assert(idx < self.count)
    return remove_unused_pixels_from_frame(self.frames_cache[idx])

  # value is 0-1
  def value_to_frame_idx(self, value):
    try:
      assert(value >= 0)
      assert(value <= 1)
    except AssertionError:
      print(f"value_to_frame_idx called with value {value}, why?? capping it")
      value = max(0, (min(1, value)))
    return min( round(self.count * value), self.count-1)

  # frame: the frame to which we apply this effect
  # fingers: a list of parameters 0-1
  def apply(self, frame, values):
    if not values:
      return frame

    frames = list(map(lambda x: self.read_frame(
      self.value_to_frame_idx(x)
    ), values))
    combined = frames[0] if len(frames) == 1 else np.sum(frames, axis=0)
    return (combined/255) * frame


# each finger = one ring of visibility
# rings000.png = outer edges / base of dome
# rings178.png = dead center of dome
rings = ImageFilter(FilterNames.RINGS, 178)

# each finger = one pie wedge
# wedges000.png = top, going clockwise
wedges = ImageFilter(FilterNames.WEDGES, 202)

reveal = ImageFilter(FilterNames.CIRCULAR_REVEAL, 64)

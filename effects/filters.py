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
  HUESHIFT = 'hueshift'
  KALEIDOSCOPE = 'kaleidoscope'
  TUNNEL = 'tunnel'

  LIGHTNING = 'lightning'
  RADIANTLINES = 'radiant'
  NUCLEAR = 'nuclear'
  SPIRAL = 'spiral'

  RINGS = 'rings'
  SPOTLIGHT = 'spotlight'
  WEDGES = 'wedges'
  TRIFORCE = 'triforce'
  BLOBS = 'blobs'

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

class HueshiftFilter:
  def __init__(self):
    self.key = FilterNames.HUESHIFT
    self.active = False

  # static method
  # do multiple fingers touch the huewheel? if so,
  # find a nice in-between value
  def reduce_fingers(self, finger_values):
    if len(finger_values) == 2:
      if abs(finger_values[1] - finger_values[0]) > 180:
        return (finger_values[0] + finger_values[1] + 360) / 2
    return np.average(
      np.add(finger_values, range(len(finger_values)))
    ) % 360

  def apply(self, frame, fingers):
    if not fingers:
      if self.active:
        self.active = False
      return frame

    finger_values = [to_polar(point)[1] for point in fingers]

    if not self.active:
      self.active = time()

    # seconds since active: (0 - 0.15) mapped to (0.15 - 0.30)
    mix_amount = min(time() - self.active, 0.15) + 0.15

    # float in 0-1 range
    val = self.reduce_fingers(finger_values)

    # flip and rotate
    val = (360 + 90 - val) % 360

    # convert to hue. red is up
    # ex. [255,0,0]
    rgb = np.array(hsv2rgb(val, 1, 1))
    mixed = numpy_mixer(frame, make_rgb_frame(rgb), mix_amount)

    # exponent & divide should fix contrast, i.e. blacks stay black
    return mixed * mixed / 255

hueshift = HueshiftFilter()

class ImageFilter:
  def __init__(self, key, count):
    self.key = key
    self.count = count

  def read_frame(self, key, idx):
    assert(idx >= 0)
    assert(idx <= self.count)
    idx_str = '{:03d}'.format(idx)
    frame = cv2.imread(os.path.join('video', 'overlays', key,
      '{}{}.png'.format(key, idx_str)))
    return remove_unused_pixels_from_frame(frame)

  def value_to_frame_idx(self, point):
    value = to_polar(point)[0]
    return round(self.count * value)

  # frame: the frame to which we apply this effect
  # fingers: a list of parameters 0-1
  def apply(self, frame, fingers):
    if not fingers:
      return frame

    frames = list(map(lambda x: self.read_frame(
      self.key, self.value_to_frame_idx(x)
    ), fingers))
    combined = frames[0] if len(frames) == 1 else np.sum(frames, axis=0)
    return (combined/255) * frame

class WedgeFilter(ImageFilter):
  # try to move top wedge to the top
  wedge_offset = 270
  def value_to_frame_idx(self, point):
    value = ((self.wedge_offset + (360 - to_polar(point)[1])) / 360) % 1
    return round(self.count * value)

# each finger = one ring of visibility
# rings000.png = outer edges / base of dome
# rings178.png = dead center of dome
rings = ImageFilter(FilterNames.RINGS, 178)

# each finger = one pie wedge
# wedges000.png = top, going clockwise
wedges = WedgeFilter(FilterNames.WEDGES, 202)

class RainbowFilter(ImageFilter):
  def __init__(self, key, count):
    self.key = key
    self.count = count

    self.sp = SequencePlayer(loop=True)
    self.sp.play(os.path.join('video', 'sources', 'colorwheels.mp4'))

  def value_to_frame_idx(self, value):
    return math.floor(self.count * value)

  # frame: the frame to which we apply this effect
  # fingers: a list of parameters, which are, pairs of x,y values 0-1
  def apply(self, frame, fingers):
    if not fingers:
      return frame

    verticals = list(map(lambda x: self.read_frame(
      'vertical-stripe', self.value_to_frame_idx(x[0])
    ), fingers))

    horizontals = list(map(lambda x: self.read_frame(
      'horizontal-stripe', self.value_to_frame_idx(x[1])
    ), fingers))

    cwframe = self.sp.read_frame()

    frames = list(map(lambda x: verticals[x] * horizontals[x] * cwframe,
      range(len(fingers))))

    combined = frames[0] if len(frames) == 1 else np.sum(frames, axis=0)
    return combined
    # return (combined/255) * frame



class RainbowFilterCached(ImageFilter):
  def __init__(self, key):
    self.key = key

    self.cache_video(os.path.join('video', 'sources', 'colorwheels.mp4'))

  # @TODO could inherit this from SourceEffectCachedVideo, or somehow share code
  def cache_video(self, path):
      sp = SequencePlayer(loop=False)
      sp.play(path)

      self.frames_cache = []
      self.frame_idx = 0

      frame = sp.read_frame()
      while not sp.ended:
        self.frames_cache.append(frame)
        frame = sp.read_frame()

      self.count = len(self.frames_cache)

  def read_frame(self):
    self.frame_idx = (self.frame_idx + 1) % self.count
    assert(self.frame_idx >= 0)
    assert(self.frame_idx <= self.count)
    return self.frames_cache[self.frame_idx]
  # frame: the frame to which we apply this effect
  # fingers: a list of parameters, which are, pairs of x,y values 0-1
  def apply(self, frame, fingers):
    if not fingers:
      return frame

    verticals = list(map(lambda x: self.read_frame(
      'vertical-stripe', self.value_to_frame_idx(x[0])
    ), fingers))

    horizontals = list(map(lambda x: self.read_frame(
      'horizontal-stripe', self.value_to_frame_idx(x[1])
    ), fingers))

    self.frame_idx = (self.frame_idx + 1) % self.count
    cwframe = self.read_frame(self.frame_idx)

    frames = list(map(lambda x: verticals[x] * horizontals[x] * cwframe,
      range(len(fingers))))

    combined = frames[0] if len(frames) == 1 else np.sum(frames, axis=0)
    return combined
    # return (combined/255) * frame

rainbow = RainbowFilter(FilterNames.SPOTLIGHT, 390)

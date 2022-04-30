from modules.sequence_player import SequencePlayer
import numpy as np
from util.hsv2rgb import hsv2rgb
from util.util import make_rgb_frame, numpy_mixer, remove_unused_pixels_from_frame
from time import time
import os
import cv2


class FilterNames:
  HUESHIFT = 'hueshift'
  KALEIDOSCOPE = 'kaleidoscope'
  TUNNEL = 'tunnel'

  LIGHTNING = 'lightning'
  RADIANTLINES = 'radiant-lines'
  NUCLEAR = 'nuclear'
  SPIRAL = 'spiral'



# these straight-up replace the input frame
class BrightnessFilter:
  def __init__(self, brightness):
    self.key = 'brightness'
    self.brightness = brightness

  def set_brightness(self, brightness):
    assert(brightness >= 0.0)
    assert(brightness <= 1.0)
    self.brightness = brightness

  def apply(self, frame, _unused):
    return np.multiply(frame, self.brightness)

brightness = BrightnessFilter(0.5)

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
  def reduce_fingers(self, fingersArray):
    return np.average(
      np.add(fingersArray, range(len(fingersArray)))
    ) % 1

  def apply(self, frame, fingers):
    if not fingers:
      if self.active:
        self.active = False
      return frame

    if not self.active:
      self.active = time()

    # seconds since active: (0 - 0.15) mapped to (0.15 - 0.30)
    mix_amount = min(time() - self.active, 0.15) + 0.15

    # float in 0-1 range
    val = self.reduce_fingers(fingers)
    print(fingers, "got mixed val:", val)

    # convert to hue. red is up
    # ex. [255,0,0]
    rgb = np.array(hsv2rgb(val*360, 1, 1))
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

  def value_to_frame_idx(self, value):
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

# each finger = one ring of visibility
# rings000.png = outer edges / base of dome
# rings178.png = dead center of dome
rings = ImageFilter('rings', 178)

# each finger = one pie wedge
# wedges000.png = top, going clockwise
wedges = ImageFilter('wedges', 202)

class RainbowFilter(ImageFilter):
  def __init__(self, key, count):
    self.key = key
    self.count = count

    self.sp = SequencePlayer(loop=True)
    self.sp.play(os.path.join('video', 'sources', 'colorwheels.mp4'))

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


rainbow = RainbowFilter('rainbow', 389)

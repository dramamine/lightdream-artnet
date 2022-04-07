import numpy as np
from util.hsv2rgb import hsv2rgb
from util.util import make_rgb_frame, numpy_mixer
from time import time

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

brightness_filter = BrightnessFilter(0.5)

class ValidateFilter:
  def __init__(self):
    self.key = 'validate'

  def apply(self, frame, _unused):
    frame = np.minimum(frame, 255)
    frame = np.maximum(frame, 0)
    frame = frame.astype(np.uint8)
    return frame

validate_filter = ValidateFilter()

class HueshiftFilter:
  def __init__(self):
    self.key = 'hueshift'
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

hueshift_filter = HueshiftFilter()

import os
import cv2

class RingsFilter:
  def __init__(self):
    self.key = 'rings'
    # self.vid = cv2.VideoCapture( os.path.join('video', 'overlays', 'rings-edit.mp4') )

  def read_frame(self, idx):
    # each finger = one ring of visibility
    # rings000.png = outer edges / base of dome
    # rings178.png = dead center of dome
    frame = cv2.imread(os.path.join('video', 'overlays', 'rings', 'rings126.png'))

    if frame.any():
      # @TODO copy pasted from sequence player
      reduced = np.minimum.reduce(
        np.array(frame, dtype=np.uint8), 2
      )
      
      # remove empties
      mask = np.zeros(len(reduced), dtype=bool)
      mask[[0,1,2,3,4,5, 16,17,18,19,20,21, 32,33,34,35,36,37, 48,49,50,51,52,53, 64,65,66,67,68,69]] = True
      data = reduced[mask,...]

      # should be 30, 512
      assert(len(data) == 30)
      assert(len(data[0]) == 512)
      return data
    
    # else, there's a problem
    print("ret was bad", ret, frame)
    return None



  def apply(self, frame, fingers):
    if not fingers:
      return frame

    frame = self.read_frame(126)
    return frame

rings_filter = RingsFilter()

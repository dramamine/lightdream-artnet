import cv2
import math
from util.config import config

from util.util import remove_unused_pixels_from_frame, nullframe

class SequencePlayer:
  def __init__(self, loop=False):
    self.vid = None
    self.path = ""
    self.loop = loop
    self.framecount = 0
    self.delay_frames = config.read("FRAME_DELAY")
    self.delay_frames_left = 0

  def play(self, path):
    self.path = path
    self.vid = cv2.VideoCapture(path)
    self.framecount = 0
    self.ended = False

    self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    assert(self.width == 512)
    # should be 80, ex. len(frame) == 80
    self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    assert(self.height == 80)

    frames = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
    print("starting sequence: track={} frames={} ({}m{}s)".format(
      path, frames, math.floor(frames/(40*60)), math.floor(frames/40) % 60
    ))

    self.delay_frames_left = 0 if "metronome" in self.path else self.delay_frames
  
  def read_frame(self):
    if self.delay_frames_left > 0:
      self.delay_frames_left -= 1
      return nullframe

    if self.ended:
      return nullframe
      
    if not self.vid:
      print("need 2 play a video before reading frames")
      return nullframe

    ret,frame = self.vid.read()
    
    if ret:
      self.framecount += 1

      return remove_unused_pixels_from_frame(frame)

    else:
      if (self.loop):
        self.play(self.path)
        return self.read_frame()
      # print("that was all the frames. end of song probably? framecount={}".format(self.framecount))
      self.ended = True
      return nullframe

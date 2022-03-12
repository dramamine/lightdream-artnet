import cv2
import os
import numpy as np
import math
from time import time 
# all blacks
nullframe = np.zeros((30, 512))

class SequencePlayer:
  def __init__(self, loop=False):
    self.vid = None
    self.path = ""
    self.loop = loop
    self.framecount = 0

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
  
  def read_frames(self):
    if self.ended:
      return nullframe
      
    if not self.vid:
      print("need 2 play a video before reading frames")
      return nullframe

    ret,frame = self.vid.read()
    
    if ret:
      self.framecount += 1

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

    else:
      print("that was all the frames. end of song probably? framecount={}".format(self.framecount))
      if (self.loop):
        self.play(self.path)
        return self.read_frames()
      self.ended = True
      return nullframe

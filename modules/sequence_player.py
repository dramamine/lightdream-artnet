import cv2
import os
import numpy as np

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

    # @TODO nice to have but not necessary... maybe verify
    # these match what we're expecting.
    # should be 512, ex. len(frame[0]) == 512
    self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    # should be 80, ex. len(frame) == 80
    self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT)))
    print("{}x{}".format(self.width, self.height))
  
  def read_frames(self):
    if not self.vid:
      print("need 2 play a video before reading frames")
      return nullframe

    ret,frame = self.vid.read()
    # should be 80, 512
    # print( len(frame), len(frame[0]) )
    
    if ret:
      self.framecount += 1

      reduced = []
      for i in range(5):
        for j in range(6):
          reduced.append(list(map(lambda x: x[0], frame[i*16+j] )))
      # reduced = list(map(lambda row: list(map(lambda x: x[0], row)), frame))
      
      # should be 30, 512
      # print( len(reduced), len(reduced[0]) )
      data = np.array(reduced, dtype=np.uint8)
      return data


    else:
      print("that was all the frames.", ret, self.framecount)
      if (self.loop):
        self.play(self.path)
        return self.read_frames()
      return nullframe

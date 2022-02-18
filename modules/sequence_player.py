import cv2
import os

class SequencePlayer:
  def __init__(self, loop=False):
    self.vid = None

  def play(self, path):
    self.vid = cv2.VideoCapture(path)
    self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
  
  def read_frames(self):
    # while not self.vid:
    #   yield None

    ret,frame = self.vid.read()
    if ret:
      print("a frame")
      yield frame
    else:
      print("that was all the frames.")
      return

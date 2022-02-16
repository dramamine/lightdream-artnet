import cv2
import os

class SequencePlayer:
  def __init__(self, video_path, loop=False):

    # self.video_path = video_path
    self.loop = loop
    self.vid = cv2.VideoCapture(video_path)
    self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

  
  def read_frames(self):
    ret,frame = self.vid.read()
    if ret:
      print("a frame")
      yield frame
    else:
      print("that was all the frames.")
      return


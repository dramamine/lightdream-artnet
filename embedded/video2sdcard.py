
import cv2
import math
import os

output_file_path  = "./output.bin"

# make sure these match on the Teensy
WIDTH = 170
HEIGHT = 8

class SequencePlayer:
  def __init__(self, loop=False):
    self.vid = None
    self.path = ""
    self.loop = loop
    self.framecount = 0
    self.delay_frames = 0
    self.delay_frames_left = 0

  def play(self, path):
    self.path = path
    self.vid = cv2.VideoCapture(path)
    self.framecount = 0
    self.ended = False

    self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    # assert(self.width == 512)
    # should be 80, ex. len(frame) == 80
    self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # assert(self.height == 80)

    frames = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
    print("starting sequence: track={} frames={} ({}m{}s)".format(
      path, frames, math.floor(frames/(40*60)), math.floor(frames/40) % 60
    ))

  def read_frame(self):
    if self.delay_frames_left > 0:
      self.delay_frames_left -= 1
      return None

    if self.ended:
      return None
      
    if not self.vid:
      print("need 2 play a video before reading frames")
      return None

    ret,frame = self.vid.read()
    
    if ret:
      self.framecount += 1

      return frame

    else:
      if (self.loop):
        self.play(self.path)
        return self.read_frame()
      # print("that was all the frames. end of song probably? framecount={}".format(self.framecount))
      self.ended = True
      return None

class Video2SDCard:
  def __init__(self, output_file):
    self.output_file = output_file
    self.sp = SequencePlayer()
    sequencePath = os.path.join('{}.mp4'.format("red-green-wipe-demo"))
    # sequencePath = os.path.join('embedded', '{}.mp4'.format("red-green-wipe-veryslow-30s"))
    self.sp.play(sequencePath)
    print(self.sp.width)
    print(self.sp.height)
  
  def write_header(self):
    
    width = self.sp.width
    width_0 = width % 256
    width_1 = math.floor(width / 256)
    height = 8
    fps = 30
    bytes = bytearray([42, width_0, width_1, height, fps])
    self.output_file.write(bytes)

  def write_frame(self, frame):
    for i in range(HEIGHT):
      for j in range(WIDTH):
        ba = bytearray([
          frame[i][j*3][0], 
          frame[i][j*3+1][0], 
          frame[i][j*3+2][0]
        ])
        self.output_file.write(ba)

  def write_frames(self):
    while(True):
      frame = self.sp.read_frame()
      if frame is None:
        break
      self.write_header()
      self.write_frame(frame)


if __name__ == "__main__":
  output_file = open(output_file_path, "wb")
  x = Video2SDCard(output_file)

  x.write_frames()
  output_file.close()

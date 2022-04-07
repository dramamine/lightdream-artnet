import numpy as np

def numpy_mixer(frame_a, frame_b, mix):
  return frame_a * (1-mix) + frame_b * mix

# ex. [255, 0, 0] becomes a 512x30 frame
def make_rgb_frame(rgb):
  return np.append( np.tile(rgb, 170), [0,0] )

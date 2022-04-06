import numpy as np

def numpy_mixer(frame_a, frame_b, mix):
  return frame_a * (1-mix) + frame_b * mix

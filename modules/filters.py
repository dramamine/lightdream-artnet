from math import ceil

class Filters:
  def __init__(self):
    self.dynamic_filters_list = []
    self.brightness = 0.8

  def _brightness_filter(self, frame):
    return list(map(lambda x: min(255, ceil(x * self.brightness)), frame ))
  
  def apply_filters(self, frame):
    for filter in self.dynamic_filters_list:
      frame = list(map(lambda x: filter(x), frame))
    frame = list(map(lambda x: self._brightness_filter(x), frame))


    return frame

  def apply_filters_inplace(self, frame):
    for i in range(len(frame)):
      for j in range(len(frame[0])):
        frame[i][j] = min(255, ceil(frame[i][j] * self.brightness))

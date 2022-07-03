import math
from effects.filters import FilterNames
from util.util import to_polar
import numpy as np

class Tunnel:
  def __init__(self, key):
    self.key = key

  # frame: the frame to which we apply this effect
  # fingers: a list of x, y pairs
  def apply(self, frame, fingers):
    if not fingers:
      return frame
    
    # take last finger
    finger = fingers[len(fingers) - 1]
    [r, theta] = to_polar(finger)
    
    # 170 = 17 * 2 * 5, trying to get some nice divisions
    # TODO adjust numbers based on touchscreen
    clone_sections = min( math.floor(r * 6), 2)
    clones = [10, 5, 2][clone_sections]

    
    start = math.floor( theta * 169 / 360 )
    
    def universe_remapper_lambda(universe):
      # should be 17, 34, 85
      clone_length = int(170 / clones)
      
      double_universe = np.append(universe, universe)
    
      subsection = double_universe[3*start:3*(start+clone_length)]
      return np.tile(subsection, clones)

    return np.apply_along_axis(universe_remapper_lambda, 1, frame)

tunnel = Tunnel(FilterNames.TUNNEL)

class Kaleidoscope:
  def __init__(self, key):
    self.key = key

  # frame: the frame to which we apply this effect
  # fingers: a list of x, y pairs
  def apply(self, frame, fingers):
    if not fingers:
      return frame
    
    # take last finger
    finger = fingers[len(fingers) - 1]
    [r, theta] = to_polar(finger)
    
    # TODO adjust these numbers based on touchscreen - just need 3 sections
    # and the right equation
    clone_sections = min( math.floor(r * 5.7), 3)
    # pixels_to_clone = [17, 34, 85][clone_sections]
    clones = [5,5,3,2][clone_sections]
    
    # grab some set of the first 30 struts. 26 should be the max
    start = math.floor( 27 * theta / 360 )

    one_brain_of_leds = np.reshape(frame[0:6], (1,510*6))
    subsection = one_brain_of_leds[0][3*start:3*(start+(clones*34))]
    return np.tile(subsection, int(150/clones) ).reshape((30,510))

kaleidoscope = Kaleidoscope(FilterNames.KALEIDOSCOPE)

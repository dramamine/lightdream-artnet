from collections import deque
from math import e
from util.config import config
import subprocess, threading
from itertools import repeat
import numpy as np

# i.e. length of the array; this should be high enough so that 'decay' works,
# and long enough so that the debug display works.
ENERGY_TAIL_LENGTH = 1200

energy_original = deque(maxlen=ENERGY_TAIL_LENGTH)
energy_original.extend(list(repeat(0,ENERGY_TAIL_LENGTH)))
energy_modified = deque(maxlen=ENERGY_TAIL_LENGTH)
energy_modified.extend(list(repeat(0,ENERGY_TAIL_LENGTH)))

audio_condition = threading.Condition()

ticks = 0
def update_energy(value):
  global ticks
  ticks = ticks + 1
  with audio_condition:
    energy_original.appendleft(value)

    # see if a decayed value would be higher
    decayed = energy_modified[0] * e ** config.read("decay_constant")
    energy_modified.appendleft( max(value, decayed) )
  
  if ticks >= ENERGY_TAIL_LENGTH:
    ticks = 0
    recalculate_max_energy()

def recalculate_max_energy():
  if config.read("MODE") == "playlist":
    return
  last = config.read("max_energy")
  if energy_original[0] > 0:
    next = max(energy_original[0] * 1.1, 20)
    print(f"updating max energy from {last:.1f} to {next:.1f}")
    config.write("max_energy", next)

def output_reader(proc):
  return

def thread_ender():
  return

def get_energy():
  return 0

# returns a float 0-1 for how strong we want the audio visualization effect to be
def get_visual_strength():
  return as_float(get_energy())

def as_float(energy):
  try:
    return min( 1, energy / config.read("max_energy") )
  except:
    return 50.0

def float_to_color(val):
  val = min(1, max(val, 0))
  return [
    255 * val,
    255 * (1 - val),
    0
  ]

def as_texture(energies):
  return np.array( list(map(lambda x: float_to_color(as_float(x)), energies)), dtype=np.uint8 )

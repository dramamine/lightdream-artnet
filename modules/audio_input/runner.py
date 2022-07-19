from collections import deque
from math import e
from util.config import config
import subprocess, threading
from itertools import repeat
import numpy as np

# i.e. length of the array; this should be high enough so that 'decay' works,
# and long enough so that the debug display works.
ENERGY_TAIL_LENGTH = 20

energy_original = deque(maxlen=ENERGY_TAIL_LENGTH)
energy_original.extend(list(repeat(0,ENERGY_TAIL_LENGTH)))
energy_modified = deque(maxlen=ENERGY_TAIL_LENGTH)
energy_modified.extend(list(repeat(0,ENERGY_TAIL_LENGTH)))

audio_condition = threading.Condition()

def update_energy(value):
  with audio_condition:
    energy_original.appendleft(value)

    # see if a decayed value would be higher
    decayed = energy_modified[0] * e ** config.read("decay_constant")
    energy_modified.appendleft( max(value, decayed) )

def output_reader(proc):
    global freq, energy
    for line in iter(proc.stdout.readline, b''):
        try:
          values = line.decode('utf-8').strip().split() # (freq, energy)
          update_energy( float(values[1]) )
        except ValueError:
          print("bad line from audio runner:", line.decode('utf-8').strip())
        except IndexError:
          print("bad line from audio runner:", line.decode('utf-8').strip())

# use mock process except on 
suffix = "_mock"
if config.read("PLATFORM") == "win":
  suffix = "_pyaudio"
elif config.read("PLATFORM") == "rpi":
  suffix = "_alsaaudio"

proc = subprocess.Popen(['python', '-u', 
  'modules/audio_input/subprocess{}.py'.format(suffix)],
  stdout=subprocess.PIPE,
  stderr=subprocess.STDOUT)

t = threading.Thread(target=output_reader, args=(proc,))
t.start()

def thread_ender():
  proc.terminate()
  try:
    proc.wait(timeout=0.2)
    print('== audio input subprocess exited with return code ', proc.returncode)
  except subprocess.TimeoutExpired:
    print('subprocess did not terminate in time')

  t.join()

def get_energy():
  return energy_modified[0]

# returns a float 0-1 for how strong we want the audio visualization effect to be
def get_visual_strength():
  return as_float(get_energy())

def as_float(energy):
  return min( 1, energy / config.read("max_energy") )

def float_to_color(val):
  val = min(1, max(val, 0))
  return [
    255 * val,
    255 * (1 - val),
    0
  ]

def as_texture(energies):
  return np.array( list(map(lambda x: float_to_color(as_float(x)), energies)), dtype=np.uint8 )

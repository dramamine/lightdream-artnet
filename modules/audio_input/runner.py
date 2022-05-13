from collections import deque
from math import e
from util.config import config
import subprocess, threading
from itertools import repeat

# what is the highest energy we can expect?
max_energy = 10

# i.e. length of the array; this should be high enough so that 'decay' works,
# and long enough so that the debug display works.
ENERGY_TAIL_LENGTH = 200

energy_original = deque(maxlen=ENERGY_TAIL_LENGTH)
energy_original.extend(list(repeat(0,ENERGY_TAIL_LENGTH)))
energy_modified = deque(maxlen=ENERGY_TAIL_LENGTH)
energy_modified.extend(list(repeat(0,ENERGY_TAIL_LENGTH)))

# range: -0.1 is a really sharp decay (10% per frame)
#        -0.01 is weaker (1% per frame)
decay_constant = -0.1

def update_energy(value):
  energy_original.appendleft(value)

  # see if a decayed value would be higher
  decayed = energy_modified[0] * e ** decay_constant
  energy_modified.appendleft( max(value, decayed) )



def output_reader(proc):
    global freq, energy
    for line in iter(proc.stdout.readline, b''):
        # [freq, energy] = line.decode('utf-8').strip().split()
        values = line.decode('utf-8').strip().split()
        # freq = values[0]
        update_energy( float(values[1]) )


is_mock = "" if config['PLATFORM'] == "rpi" else "_mock"

proc = subprocess.Popen(['python', '-u', 
  'modules/audio_input/subprocess{}.py'.format(is_mock)],
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
  return max( 1, get_energy() / max_energy )

def update_max_energy(val):
  assert(val > 0)
  max_energy = val

def update_decay_constant(val):
  decay_constant = val

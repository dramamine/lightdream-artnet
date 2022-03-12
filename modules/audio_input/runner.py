from util.config import config
import subprocess, threading
from util.periodicrun import periodicrun
from time import time

freq = 0.0
energy = 0.0

def output_reader(proc):
    global freq, energy
    for line in iter(proc.stdout.readline, b''):
        # [freq, energy] = line.decode('utf-8').strip().split()
        values = line.decode('utf-8').strip().split()
        freq = values[0]
        energy = values[1]


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
  return energy

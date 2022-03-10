import pyaudio
import wave
import sys
import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt

p = None
stream = None


CHANNELS = 1
RATE = 44100

def init():
    global p
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt8,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=128,
                output=False,
                input=True,
                input_device_index=2)

def get_a_read():
    frames = stream.read(128, False)
    print(len(frames))
    pass



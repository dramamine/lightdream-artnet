#! /usr/bin/env python

import alsaaudio
import numpy as np
import aubio


# constants
samplerate = 44100
win_s = 2048
hop_s = win_s // 2
framesize = hop_s

# set up audio input
recorder = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE, mode=alsaaudio.PCM_NONBLOCK, rate=samplerate,
    channels=1, format=alsaaudio.PCM_FORMAT_FLOAT_LE)
recorder.setperiodsize(framesize)

# create aubio pitch detection (first argument is method, "default" is
# "yinfft", can also be "yin", "mcomb", fcomb", "schmitt").
pitcher = aubio.pitch("default", win_s, hop_s, samplerate)
# set output unit (can be 'midi', 'cent', 'Hz', ...)
pitcher.set_unit("Hz")
# ignore frames under this level (dB)
pitcher.set_silence(-40)

def get_energy():
    # read data from audio input
    _, data = recorder.read()
    # convert data to aubio float samples
    samples = np.fromstring(data, dtype=aubio.float_type)
    # pitch of current frame
    freq = pitcher(samples)[0]
    # compute energy of current block
    energy = np.sum(samples**2)/len(samples)
    # do something with the results
    print("{:10.4f} {:10.4f}".format(freq,energy))
    return energy

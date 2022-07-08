#! /usr/bin/env python

# Use pyaudio to open the microphone and run aubio.pitch on the stream of
# incoming samples. If a filename is given as the first argument, it will
# record 5 seconds of audio to this location. Otherwise, the script will
# run until Ctrl+C is pressed.

# Examples:
#    $ ./python/demos/demo_pyaudio.py
#    $ ./python/demos/demo_pyaudio.py /tmp/recording.wav

import pyaudio
import sys
import numpy as np
import aubio

# initialise pyaudio
p = pyaudio.PyAudio()

# constants
samplerate = 44100
win_s = 2048
hop_s = win_s // 2
framesize = hop_s

# open stream
buffer_size = 1024
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)

if len(sys.argv) > 1:
    # record 5 seconds
    output_filename = sys.argv[1]
    record_duration = 5 # exit 1
    outputsink = aubio.sink(sys.argv[1], samplerate)
    total_frames = 0
else:
    # run forever
    outputsink = None
    record_duration = None

# create aubio pitch detection (first argument is method, "default" is
# "yinfft", can also be "yin", "mcomb", fcomb", "schmitt").
pitcher = aubio.pitch("default", win_s, hop_s, samplerate)
# set output unit (can be 'midi', 'cent', 'Hz', ...)
pitcher.set_unit("Hz")
# ignore frames under this level (dB)
pitcher.set_silence(-40)


print("*** starting recording")
while True:
    try:
        audiobuffer = stream.read(buffer_size)
        # signal = np.fromstring(audiobuffer, dtype=np.float32)
        # convert data to aubio float samples
        samples = np.frombuffer(audiobuffer, dtype=aubio.float_type)
        # pitch of current frame
        freq = pitcher(samples)[0]
        # compute energy of current block
        energy = np.sum(samples**2)/len(samples)
        # do something with the results
        print("{:10.4f} {:10.4f}".format(freq,1000*energy))

        # pitch = pitch_o(signal)[0]
        # confidence = pitch_o.get_confidence()

        # print("{} / {}".format(pitch,confidence))

        # if outputsink:
        #     outputsink(signal, len(signal))

        # if record_duration:
        #     total_frames += len(signal)
        #     if record_duration * samplerate < total_frames:
        #         break
    except KeyboardInterrupt:
        print("*** Ctrl+C pressed, exiting")
        break

print("*** done recording")
stream.stop_stream()
stream.close()
p.terminate()
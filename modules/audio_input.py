import pyaudio
import wave
import sys
import numpy as np
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt

p = pyaudio.PyAudio()
print(p.get_device_count())

for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))

CHANNELS = 1
RATE = 44100

fulldata = np.array([])
dry_data = np.array([])

def callback(in_data, frame_count, time_info, flag):
    global b,a,fulldata,dry_data,frames 
    audio_data = np.frombuffer(in_data, dtype=np.int8)
    # dry_data = np.append(dry_data,audio_data)
    #do processing here
    # ulldata = np.append(fulldata,audio_data)
    max_signal = np.max(audio_data)
    signals_over_x = sum(1 for i in audio_data if i > 1)
    # fft_data = ifft(audio_data)
    partial = np.abs(audio_data)[8:40]
    # print(partial)
    sum_partial = np.sum(partial)
    
    if sum_partial > 1500:
        print(sum_partial)
    #print("frames: {}. {} {}. {}".format(frame_count, max_signal, signals_over_x, sum_partial))
    
    
    
    # exit()
    # print(audio_data)
    
    return (audio_data, pyaudio.paContinue)

def graph(audio_data):
    
    # sampling rate
    sr = 128
    # sampling interval
    ts = 1.0/sr

    N = len(audio_data)
    n = np.arange(N)
    T = N/sr
    freq = n/T
    print(np.abs(audio_data))
    
    t = np.arange(0,1,ts)
    plt.style.use('seaborn-poster')
    plt.stem(freq, np.abs(audio_data), 'b', \
         markerfmt=" ", basefmt="-b")
    plt.xlabel('Freq (Hz)')
    plt.ylabel('FFT Amplitude |X(freq)|')
    plt.xlim(0, 10)
    # plt.figure(figsize = (8, 6))
    # plt.plot(t, audio_data, 'r')
    # plt.show()

def open_stream():
    stream = p.open(format=pyaudio.paInt8,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=128,
                output=False,
                input=True,
                input_device_index=2,
                stream_callback=callback)


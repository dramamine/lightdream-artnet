## Lightdream Artnet

Project to run lightdream-scripts code on an rpi instead.



```


# Windows
pip install -r requirements.txt

# RPi: you also need these:
pip install gstreamer-player PyGObject pycairo

# RPi: not sure how many of these are necessary but hey why not
sudo apt-get install gstreamer1.0-tools gstreamer1.0-pulseaudio \
  libgirepository1.0-dev libcairo2-dev gir1.2-gstreamer-1.0

# check audio output device and make sure it's not HDMI


```

Features:

- sends out artnet data
- autoplay mode
- sequenced audio mode
- metronome / calibration mode
- filter system to modify frame data in realtime

@TODO features:

- touchscreen interface that works on rpi
- calibration settings (order of artnet ip's)
- respond to keyboard / touchscreen events

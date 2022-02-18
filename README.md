## Lightdream Artnet

Project to run lightdream-scripts code on an rpi instead.



```
# not sure how many of these are necessary but hey why not
sudo apt-get install gstreamer1.0-tools gstreamer1.0-pulseaudio \
  libgirepository1.0-dev libcairo2-dev gir1.2-gstreamer-1.0

# @TODO this doesn't work great but you need all these packages
pip install -r requirements.txt

# check audio output device and make sure it's not HDMI


```

@TODO features

- make file paths OS-agnostic
- touchscreen interface that works on rpi
- send out artnet data
- calibration settings (order of artnet ip's)
- modify frame data by combining with other frames

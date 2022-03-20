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

### Touchscreen Interface

Milestone 0: debug menu
- ability to toggle autoplay(DJ mode) vs. sequenced songs mode
- ability to add song to queue
  - ex. `audio_player.queue(id: string)`
- ability to toggle calibration on/off
  - marten to figure this out

Milestone 1: simple on/off effects
- call fn's ex. `toggle(id: string, on: boolean)`
- "mask" style: blobs, nuclear, spiral, radiant lines
- "replace" style: lightning bolts

Milestone 2: position-based effects
- call fn's ex. `finger(fingerid: int, action: int (0=on, 1=off, 2=motion), x, y)`
  - which are part of some finger manager class
- each effect calls the finger class to ask which fingers are currently touching it
- "mask" style: rings, wedges
- "theta" style: colorwheel 
- complex "mask" style: rainbow spotlight

Milestone 3: new effects?
- color inverter
- turn some auto clips into simple on/off effects

Milestone 4: finalize arrangement

### Other Stuff

- DJ mode: use FFT to listen for bass
  + "get energy" cmd
  - create filters based on that energy
- calibration settings (order of artnet ip's)
  + it exists
  - need a way to toggle metronome
- respond to keyboard / touchscreen events
- using alsaaudio for input but pyglet for output. is that OK or bad?
+ add envs so that we're not importing bad things. prod vs dev? or platform-specific?

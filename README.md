## Lightdream Artnet

Project to run lightdream-scripts code on an rpi instead.

```


# Windows
pip install -r requirements.txt

For audio listener, you need
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl
then `pip install PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl`


# RPi: you also need these:
pip install gstreamer-player PyGObject pycairo mesa-utils

# RPi: not sure how many of these are necessary but hey why not
sudo apt-get install gstreamer1.0-tools gstreamer1.0-pulseaudio \
  libgirepository1.0-dev libcairo2-dev gir1.2-gstreamer-1.0

# check audio output device and make sure it's not HDMI
https://www.alsa-project.org/main/index.php/Setting_the_default_device

cat /proc/asound/cards
echo -e "defaults.pcm.card 1\ndefaults.ctl.card 1" > /etc/asound.conf


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

- "mask" style: blobs, nuclear, spiral, radiant lines
- "replace" style: lightning bolts
- parameters: boolean

Milestone 2: position-based effects

- "mask" style
  - rings:
    - parameters: distance from center (0.0 - 1.0)
    - animation: scale a rainbow ring so that there's a ring where the fingers are
  - wedges:
    - parameters: theta (0.0 at top, to 1.0, going clockwise)
    - animation: show a wedge where the fingers are
- "filter" style

  - huewheel:
    - parameters: theta (0.0 at top, to 1.0, going clockwise)
    - animation: ??

- complex "mask" style
  - rainbow spotlight
    - parameters: (x,y) values where x and y are 0.0 - 1.0
    - animation: rainbow wheel where the fingers are?

Milestone 3: new effects?

- color inverter
- turn some auto clips into simple on/off effects

Milestone 4: finalize arrangement

## Fit N Finish

- Spotlight effect on the spotlight circle

### Other Stuff

- DJ mode: use FFT to listen for bass
  - "get energy" cmd
  * create filters based on that energy
- calibration settings (order of artnet ip's)
  - it exists
  * need a way to toggle metronome
- respond to keyboard / touchscreen events
- using alsaaudio for input but pyglet for output. is that OK or bad?

* add envs so that we're not importing bad things. prod vs dev? or platform-specific?

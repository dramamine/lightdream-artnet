## Lightdream Artnet

Project to run lightdream-scripts code on an rpi instead.

```


# Windows
pip install -r requirements.txt

# RPi: you also need these:
pip install gstreamer-player PyGObject pycairo mesa-utils

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



If you run Kivy from the console and not from a desktop environment, you need to compile SDL2 from source, as the one bundled with Buster is not compiled with the kmsdrm backend, so it only works under X11.

Install requirements:

sudo apt-get install libfreetype6-dev libgl1-mesa-dev libgles2-mesa-dev libdrm-dev libgbm-dev libudev-dev libasound2-dev liblzma-dev libjpeg-dev libtiff-dev libwebp-dev git build-essential
sudo apt-get install gir1.2-ibus-1.0 libdbus-1-dev libegl1-mesa-dev libibus-1.0-5 libibus-1.0-dev libice-dev libsm-dev libsndio-dev libwayland-bin libwayland-dev libxi-dev libxinerama-dev libxkbcommon-dev libxrandr-dev libxss-dev libxt-dev libxv-dev x11proto-randr-dev x11proto-scrnsaver-dev x11proto-video-dev x11proto-xinerama-dev
Install SDL2:

wget https://libsdl.org/release/SDL2-2.0.10.tar.gz
tar -zxvf SDL2-2.0.10.tar.gz
pushd SDL2-2.0.10
./configure --enable-video-kmsdrm --disable-video-opengl --disable-video-x11 --disable-video-rpi
make -j$(nproc)
sudo make install
popd
Install SDL2_image:

wget https://libsdl.org/projects/SDL_image/release/SDL2_image-2.0.5.tar.gz
tar -zxvf SDL2_image-2.0.5.tar.gz
pushd SDL2_image-2.0.5
./configure
make -j$(nproc)
sudo make install
popd
Install SDL2_mixer:

wget https://libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.4.tar.gz
tar -zxvf SDL2_mixer-2.0.4.tar.gz
pushd SDL2_mixer-2.0.4
./configure
make -j$(nproc)
sudo make install
popd
Install SDL2_ttf:

wget https://libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.0.15.tar.gz
tar -zxvf SDL2_ttf-2.0.15.tar.gz
pushd SDL2_ttf-2.0.15
./configure
make -j$(nproc)
sudo make install
popd
Make sure the dynamic libraries cache is updated:

sudo ldconfig -v
If you are getting output similar to this when running your app:

[INFO   ] GL: OpenGL vendor <b'VMware, Inc.'>
[INFO   ] GL: OpenGL renderer <b'llvmpipe (LLVM 9.0.1, 128 bits)'>
Then it means that the renderer is NOT hardware accelerated. This can be fixed by adding your user to the render group:

sudo adduser "$USER" render
You will then see an output similar to this:

[INFO   ] GL: OpenGL vendor <b'Broadcom'>
[INFO   ] GL: OpenGL renderer <b'V3D 4.2'>



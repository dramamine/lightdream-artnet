## Lightdream Artnet

Project to run lightdream-scripts code on an rpi instead.

[What is Lightdream?](https://metal-heart.org/lightdream/)

![lightdream](https://github.com/dramamine/lightdream-artnet/assets/1554498/99c03f33-8a08-4cee-a13f-3e7469932f20)

[Click here for more info.](https://metal-heart.org/lightdream/)

Lightdream takes sequences of Artnet data, encoded as video files, and plays them back to your network. This allows me to pre-record light shows for songs and coordinate playback of the audio and visuals. This has two modes so that I can play sequenced songs or generate a light show on-the-fly using premade clips and audio detection algorithms.

This currently supports about 40 uniiverses @ 40 fps, but you can push this farther before you hit hardware performance limits.

This is not a general purpose library, but it's intended for a workflow where you already have created Artnet data video files by using [Lightjams Recorder](https://www.lightjams.com/recorder.html) or equivalent.

## Features

- sends out artnet data
- autoplay mode
- sequenced audio mode
- metronome / calibration mode
- filter system to modify frame data in realtime
- Playlist Mode: Sync music files and video files.
  - Add the track info to util/track_metadata.yml and then add `key.ogg` to the `audio` folder and `key.mp4` to `video\sequences`
- Autoplay Mode: Play clips at random.
  - Add these clips to `video\autoclips`. Any `.mp4` files should get picked up.

## Setup

After running once, you'll have a `config.yml` file to work with. Check `util/config.py` for descriptions of the settings.

## Installation Scripts

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

How to run at startup:

cat ~/.config/lxsession/LXDE-pi/autostart 

@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash

cat /etc/xdg/autostart/lightdream.desktop
[Desktop Entry]
Exec=lxterminal -e "cd ~/lightdream-artnet && python main.py; bash"


``



Helpful commands for running on Rpi:

```bash
# you want to run with X11 running. it's possible to use from the command-line
# with Kivy as your touchscreen and keyboard input. but, with pynput for
# your keyboard, it's easier to just open X11.
sudo vi /etc/xdg/lxsession/LXDE-pi/autostart

# the file should look like this:
# https://forums.raspberrypi.com/viewtopic.php?t=294014
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@lxterminal

# switch between desktop/CLI
sudo raspi-config
```

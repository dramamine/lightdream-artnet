import yaml

config_file = 'config.yml'
defaults = {
  # mac | win | rpi
  "PLATFORM": "mac",
  "MODE": "autoplay",
  "AUDIO_DEBUG": False,

  # if true, set volume to 0
  "DISABLE_AUDIO": False,

  # if true, only use the 3 songs committed to the repo.
  # this gets disabled in production.
  "DEBUG_TRACKLIST": True,

  # if there's a screen, do we show LED output?
  "LED_VIEWER": False,
  # if there's a screen, do we show audio viewer?
  "AUDIO_VIEWER": False,

  # if true, fullscreen touchscreen
  "FULLSCREEN_MODE": False,

  # if true, send LED data over the network
  "SEND_LED_DATA": False,

  # if true, use a timer around the loop function
  "USE_PERFORMANCE_TIMING": True,

  # fps for how often we should update LED screen, audio inputs, playlist etc.
  "TOUCHSCREEN_DATA_REFRESH_RATE": 40,

  # frame delay for playlist songs i.e. show this many blank frames before
  # playing frames from video file. this helps with audio sync
  "FRAME_DELAY": 5,


  # range: -0.1 is a really sharp decay (10% per frame)
  #        -0.01 is weaker (1% per frame)
  "decay_constant": -0.05,
  # what is the highest energy we can expect?
  "max_energy": 10,
  # 1.0 is no brightness adjustment. range: 0 -> inf
  "brightness": 0.15,

  # range: 0 -> 1
  "aural_effect_strength_multiplier": 0.15,

  # circular reveal: 0 = original frame, 1 = only what's revealed by it
  "aural_effect_strength_reveal": 0.85,

  "chance_basic_effects": .5,
  "chance_wedge_effects": .2,
  "chance_ring_effects": .2,
  "chance_reveal_effects": .1,

  # seconds until changing auto-clip
  "autoplay_interval": 50,
  # seconds over which we fade from one section to the next
  "autoplay_crossfade": 5,

  # from artnet.py, how is the dome oriented? range: 0 -> 9
  "brain_position": 3,
}

class Config:
  def __init__(self):
    with open(config_file, 'r') as file:
      self.data = yaml.safe_load(file)
    
    for key,val in defaults.items():
      if key not in self.data:
        self.write(key, val, True)

  def read(self, key: str):
    return self.data[key]

  def write(self, key: str, value, shouldSave: bool = False):
    self.data[key] = value

    if (shouldSave):
        with open(config_file, 'w') as file:
          yaml.safe_dump(self.data, file)

config = Config()

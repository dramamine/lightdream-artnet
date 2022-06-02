import yaml

config_file = 'config.yml'
defaults = {
  "ENV": "dev",
  "PLATFORM": "mac",
  "MODE": "autoplay",
  "AUDIO_DEBUG": False,

  # if true, only use the 3 songs committed to the repo.
  # this gets disabled in production.
  "DEBUG_TRACKLIST": True,
  # range: -0.1 is a really sharp decay (10% per frame)
  #        -0.01 is weaker (1% per frame)
  "decay_constant": -0.05,
  # what is the highest energy we can expect?
  "max_energy": 10,
  # 1.0 is no brightness adjustment. range: 0 -> inf
  "brightness": 1.0,

  # range: 0 -> 1
  "aural_effect_strength_multiplier": 0.25,
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

from os.path import exists
import yaml

config_file = 'config.yml'
defaults = {
  "ENV": "dev",
  "PLATFORM": "mac",
  "MODE": "autoplay"
}

if not exists(config_file):
  with open(config_file, 'w') as file:
    yaml.safe_dump(defaults, file)

with open(config_file, 'r') as file:
  config = yaml.safe_load(file)

config

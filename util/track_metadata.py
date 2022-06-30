import os
import yaml
from util.config import config

with open(os.path.join("util", "track_metadata.yml"), 'r') as file:
  track_metadata_yaml = yaml.safe_load(file)

track_metadata = track_metadata_yaml

if config.read("DEBUG_TRACKLIST"):
  track_metadata = {
    'asineedyou': track_metadata_yaml['asineedyou'],
    'misty': track_metadata_yaml['misty'],
    'moses': track_metadata_yaml['moses']
  }

tracks = list(track_metadata.keys())

from pyartnet import ArtNetNode, DmxUniverse
from util.config import config

ips = [
  '169.254.18.32', 
  '169.254.18.33',
  '169.254.18.34', 
  '169.254.18.35', 
  '169.254.18.36',
]
nodes = [ArtNetNode(host=ip, max_fps=40, refresh_every=0) for ip in ips]
for node in nodes:
  node.start()

universe_lists = list(map( lambda node: [node.add_universe(uni) for uni in range(6)], nodes ))

for universe_list in universe_lists:
  [uni.add_channel(start=1, width=510) for uni in universe_list]

# how are the brains arranged? how is the touchscreen oriented to the dome?
# configs let us rearrange what data is sent to what ip
brain_positions = [
  [0,1,2,3,4],
  [1,2,3,4,0],
  [2,3,4,0,1],
  [3,4,0,1,2],
  [4,0,1,2,3],
  [0,4,3,2,1],
  [4,3,2,1,0],
  [3,2,1,0,4],
  [2,1,0,4,3],
  [1,0,4,3,2]
]

# universes: list of 6 Artnet instances
# channels: list of 6 sets of channel data
def _send_to_brain(universes: list[DmxUniverse], channels):
  for i in range(6):
    universes[i].data = bytearray(channels[i])


def show(frame):
  # assert len(frame) == 30
  positions = brain_positions[config.read("brain_position")]
  for i in range(5):
    _send_to_brain(universe_lists[positions[i]], frame[6*i:6*i+6])
  [node.update() for node in nodes]
  
from stupidArtnet import StupidArtnet
from util.config import config

ips = [
  '169.254.18.32', 
  '169.254.18.33',
  '169.254.18.34', 
  '169.254.18.35', 
  '169.254.18.36',
]

# TARGET_IP   = DEFAULT 127.0.0.1
# UNIVERSE    = DEFAULT 0
# PACKET_SIZE = DEFAULT 512
# FRAME_RATE  = DEFAULT 30
# ISBROADCAST = DEFAULT FALSE


universe_lists = list(map( lambda ip: [StupidArtnet(ip, uni, 510, 40) for uni in range(6)], ips ))

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
def _send_to_brain(universes, channels):
  for i in range(6):
    universes[i].send(bytearray(channels[i]))


def show(frame):
  positions = brain_positions[config.read("brain_position")]
  for i in range(5):
    _send_to_brain(universe_lists[positions[i]], frame[6*i:6*i+6])

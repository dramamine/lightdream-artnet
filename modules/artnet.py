from stupidArtnet import StupidArtnet
import time

def flatten(list_of_lists):
  return [val for sublist in list_of_lists for val in sublist]

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


universe_lists = list(map( lambda ip: [StupidArtnet(ip, uni, 512, 40) for uni in range(6)], ips ))

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

bp = 3

# universes: list of 6 Artnet instances
# channels: list of 6 sets of channel data
def _send_to_brain(universes, channels):
  assert len(universes) == 6
  assert len(channels) == 6

  for i in range(6):
    universes[i].send(bytearray(channels[i]))


def show(frame):
  assert len(frame) == 80
  for i in range(5):
    positions = brain_positions[bp]
    universe_lists_idx = positions[i]
    _send_to_brain(universe_lists[universe_lists_idx], frame[16*i:16*i+6])



if __name__ == "__main__":
  redframe = flatten([[255, 0, 0] for col in range(170)])

  # demo code
  packet_size = 512
  packet = bytearray(redframe)		# create packet for Artnet
  # for i in range(packet_size):			# fill packet with sequential values
  #     packet[i] = (i % 256)

  for uni in universe_lists[1]:
    print(uni)
    uni.send(packet)

  print("shown")

  time.sleep(5)

  for uni in universe_lists[1]:
    uni.blackout()
  time.sleep(2)

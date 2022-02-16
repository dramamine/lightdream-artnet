from modules.sequence_player import SequencePlayer

path = "..\\video\\rotate_gradient_red2red_12unis.mp4"

sp = SequencePlayer(path, False)

while(True):
  next(sp.read_frames())
  
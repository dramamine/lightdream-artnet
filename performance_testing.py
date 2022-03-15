from modes.playlist import Playlist
from modes.autoplay import Autoplay, numpy_mixer
from modules.artnet import show
from effects.effects import effects_manager
import modules.audio_input.runner as audio_listener
from effects.masks import nuclearEffect, spiralEffect, blobsEffect

from util.config import config

from util.periodicrun import periodicrun
import timeit

pl = Playlist()
pl.enqueue('misty')

def loop():
  frame = pl.tick()
  # testing crossfader fn
  frame = numpy_mixer(frame, frame, 0.343095)

  frame = effects_manager.apply_effects(frame)

  frame = nuclearEffect.apply(frame)
  frame = spiralEffect.apply(frame)
  frame = blobsEffect.apply(frame)
  # 4 filters & crossfader: 11.3 ms on rpi
  #                          3.3 ms on windows desktop
  
  energy = audio_listener.get_energy()
  # energy calc seems to make no difference (!)

print("avg in ms:", timeit.timeit('loop()', globals=globals(), number=5000) / 5)

audio_listener.thread_ender()

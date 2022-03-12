from modes.playlist import Playlist
from modes.autoplay import Autoplay, numpy_mixer
from modules.artnet import show
from modules.filters import Filters
import modules.audio_input.runner as audio_listener
from filters.masks import nuclearFilter, spiralFilter, blobsFilter

from util.config import config

from util.periodicrun import periodicrun
import timeit

pl = Playlist()
filters = Filters()
pl.enqueue('misty')

def loop():
  frame = pl.tick()
  # testing crossfader fn
  frame = numpy_mixer(frame, frame, 0.343095)

  frame = filters.apply_filters(frame)

  frame = nuclearFilter.apply(frame)
  frame = spiralFilter.apply(frame)
  frame = blobsFilter.apply(frame)
  # 4 filters & crossfader: 11.3 ms on rpi
  #                          2.8 ms on windows desktop
  
  energy = audio_listener.get_energy()
  # energy calc seems to make no difference (!)

print("avg in ms:", timeit.timeit('loop()', globals=globals(), number=5000) / 5)

audio_listener.thread_ender()

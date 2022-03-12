from modes.playlist import Playlist
from modes.autoplay import Autoplay, numpy_mixer
from modules.artnet import show
from modules.filters import Filters

from util.config import config

from util.periodicrun import periodicrun
import timeit

pl = Playlist()
filters = Filters()
pl.enqueue('misty')

def loop():
  frame = pl.tick()
  # testing crossfader
  frame = numpy_mixer(frame, frame, 0.343095)

  frame = filters.apply_filters(frame)

print("avg in ms:", timeit.timeit('loop()', globals=globals(), number=5000) / 5)
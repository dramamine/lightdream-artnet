from modes.playlist import Playlist
from modes.autoplay import Autoplay
from modules.artnet import show
from effects.effects import effects_manager

from util.config import config
from time import time

from modules.fingers import finger_manager

from kivy.clock import Clock
import modules.audio_input.runner as audio_listener
from touchscreen_view import MainApp

app = MainApp()

fps = 40

# "playlist" | "autoplay" | "metronome"
mode = config.read("MODE")

pl = Playlist()
ap = Autoplay()
# pl.test_metronome()
# audio_input.init()
# audio_input.open_stream()

if mode == "metronome":
  pl.test_metronome()
elif mode == "autoplay":
  ap.start()
elif mode == "playlist":
  pl.start()

def loop(dt):
  mode = config.read("MODE")
  
  if mode == "autoplay":
    frame = ap.tick()
  else:
    frame = pl.tick()

  frame = effects_manager.apply_effects(frame, finger_manager)

  # if debug menu is open, the audio viewer components need updating
  app.update_audio_viewer(
    audio_listener.as_texture( audio_listener.energy_original ), 
    audio_listener.as_texture( audio_listener.energy_modified ),
  )

  if config.read("LED_VIEWER") == True:
    app.update_frame(frame)

  if config.read("ENV") == "prod":
    show(frame)

def set_mode(next_mode):
  global mode
  if mode == next_mode:
    return
  mode = next_mode
  if mode == "autoplay":
    pl.stop()
    config.write("MODE", "autoplay")
    ap.start()
  elif mode == "playlist":
    config.write("MODE", "playlist")
    pl.clear()
    pl.start()
  elif mode == "metronome":
    config.write("MODE", "metronome")
    pl.test_metronome()
  

start_time = time()
last_time = 0
frame_counter = 0

# for debugging. can swap out for 'loop' for final build
def loop_timer(dt):
  global frame_counter, start_time, last_time
  frame_counter = frame_counter + 1
  loop_timer = time()

  loop(dt)

  # this should look pretty consistently as a multiple of 1
  if frame_counter % 40 == 0:
    diff = time() - start_time
    print(f'{diff:.3f} ({40 / (diff - last_time):.3f}) fps')
    last_time = diff

  loop_time = time() - loop_timer
  if loop_time > 0.020:
    print("warning: loop took too long (needs to be < 0.025):", loop_time)

app.add_touchscreen_api({
  'enqueue': pl.enqueue,
  'dequeue': pl.dequeue,
  'skip_track': pl.skip_track,
  'set_mode': set_mode,
  # it's a singleton, but might as well include it here
  'config': config
})
pl.subscribe_to_playlist_updates(app.stupid_updated_queue_callback)

Clock.schedule_interval(loop_timer, 1/fps)
try:
  app.run()
finally:
  audio_listener.thread_ender()

import sys
from modes.playlist import Playlist
from modes.autoplay import Autoplay
from modules.artnet import show
from effects.effects import effects_manager

from util.config import config
from util.util import nullframe
from time import sleep, time

from modules.fingers import finger_manager

from kivy.clock import Clock
import modules.audio_input.runner as audio_listener
from touchscreen_view import MainApp
from util.periodicrun import periodicrun
from threading import Condition

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

frame = nullframe
frame_condition = Condition()

def get_frame():
  global frame
  return frame

def show_frame():
  global frame

  if config.read("ENV") == "prod":
    show(frame)

def queue_next_frame():
  global frame
  mode = config.read("MODE")
  
  if mode == "autoplay":
    frame = ap.tick()
  else:
    frame = pl.tick()

  frame = effects_manager.apply_effects(frame, finger_manager)
  # print("queued frame:", frame)

  # if debug menu is open, the audio viewer components need updating
  # TODO cancelling for async
  # app.update_audio_viewer(
  #   audio_listener.as_texture( audio_listener.energy_original ), 
  #   audio_listener.as_texture( audio_listener.energy_modified ),
  # )

# def loop(dt):
#   mode = config.read("MODE")
  
#   if mode == "autoplay":
#     frame = ap.tick()
#   else:
#     frame = pl.tick()

#   frame = effects_manager.apply_effects(frame, finger_manager)

#   if config.read("ENV") == "prod":
#     show(frame)

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
last_time = time()
frame_counter = 0

# for debugging. can swap out for 'loop' for final build
def loop_timer(dt=0):
  global frame_counter, start_time, last_time
  frame_counter = frame_counter + 1
  loop_start_time = time()

  # consider waiting
  time_since = loop_start_time - last_time
  time_to_wait = 0.025 - time_since
  if (time_to_wait > 0):
    print("sleeping for:", time_to_wait)
    sleep(time_to_wait)
    loop_start_time = time()
  # if (time_to_wait < -0.025 and config.read("MODE") == "playlist"):
  #   # need to skip a frame
  #   print("falling behind so im skipping a frame")
  #   queue_next_frame()

  
  # loop(dt)
  show_frame()

  with frame_condition:
    queue_next_frame()
    frame_condition.notify()

  # if debug menu is open, the audio viewer components need updating
  # TODO cancelling for async
  # app.update_audio_viewer(
  #   audio_listener.as_texture( audio_listener.energy_original ), 
  #   audio_listener.as_texture( audio_listener.energy_modified ),
  # )
  # # TODO cancelling for async
  # if config.read("LED_VIEWER") == True:
  #   app.update_frame(frame)


  # this should look pretty consistently as a multiple of 1
  if frame_counter % 40 == 0:
    diff = time() - start_time
    print(f'{diff:.3f} ({40 / (diff - last_time):.3f}) fps')
    last_time = diff

  loop_time = time() - loop_start_time
  if loop_time > 0.020:
    print("warning: loop took too long (needs to be < 0.025):", loop_time)

app.add_touchscreen_api({
  'enqueue': pl.enqueue,
  'dequeue': pl.dequeue,
  'skip_track': pl.skip_track,
  'set_mode': set_mode,
  'frame_condition': frame_condition,
  'get_frame': get_frame,
  'audio_listener': audio_listener,
  # it's a singleton, but might as well include it here
  'config': config
})
pl.subscribe_to_playlist_updates(app.stupid_updated_queue_callback)

pr = periodicrun(1/fps, loop_timer, list(), 0, 0.025)
try:
  pr.run_thread()
  app.run()
finally:
  audio_listener.thread_ender()
  pr.interrupt()

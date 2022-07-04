
from modules.artnet import show

from util.config import config
from time import time
import modules.audio_input.runner as audio_listener
from touchscreen_view import MainApp
from util.periodicrun import periodicrun
from threading import Condition

from modules.controller import Controller

fps = 40

app = MainApp(config.read("TOUCHSCREEN_DATA_REFRESH_RATE"))


frame_condition = Condition()

controller = Controller(
  config.read("MODE")
)

should_update_mode = False
def queue_set_mode(next_mode):
  global should_update_mode
  should_update_mode = next_mode

should_skip_track = False
def queue_skip_track():
  global should_skip_track
  should_skip_track = True

def loop():
  global should_update_mode, should_skip_track, frame_condition
  with frame_condition:
    if config.read("SEND_LED_DATA"):
      show(controller.get_frame())

    if should_update_mode:
      controller.set_mode(should_update_mode)
      should_update_mode = False

    if should_skip_track:
      controller.pl.skip_track()
      should_skip_track = False

    controller.update_frame()

    frame_condition.notify()


start_time = time()
last_time = time()
frame_counter = 0
avg_loop_time = 0
is_warmup = True

# for debugging. can swap out for 'loop' for final build
def loop_timer(dt=0):
  global frame_counter, start_time, last_time, avg_loop_time, is_warmup
  frame_counter = frame_counter + 1
  loop_start_time = time()
  
  loop()
  
  if is_warmup:
    if frame_counter == 200:
      print("done warming up")
      frame_counter = 0
      is_warmup = False
    return

  # this should look pretty consistently as a multiple of 1
  if frame_counter % 40 == 0:
    diff = time() - start_time
    print(f'{diff:.3f} ({40 / (diff - last_time):.3f}) fps')
    last_time = diff

  loop_time = time() - loop_start_time
  if loop_time > 0.020:
    print("warning: loop took too long (needs to be < 0.025):", loop_time)
    
  avg_loop_time = avg_loop_time + (loop_time - avg_loop_time) / frame_counter

app.add_touchscreen_api({
  'playlist': controller.pl,
  'get_frame': controller.get_frame,
  'skip_track': queue_skip_track,
  'set_mode': queue_set_mode,
  'audio_listener': audio_listener,
  'frame_condition': frame_condition,
  'audio_condition': audio_listener.audio_condition
})

# TODO try lower values on rpi
accuracy = 0.025 


if config.read("USE_PERFORMANCE_TIMING"):
  pr = periodicrun(1/fps, loop_timer, list(), 0, accuracy)
else:
  pr = periodicrun(1/fps, loop, list(), 0, accuracy)

try:
  pr.run_thread()
  app.run()
finally:
  audio_listener.thread_ender()
  pr.interrupt()
  print(f"avg loop time (ms): {1000*avg_loop_time:.1f}") 

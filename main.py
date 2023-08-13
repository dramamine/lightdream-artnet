#!/usr/bin/python
from queue import Queue
from modules.artnet import show

from util.config import config
from time import time
import modules.audio_input.runner as audio_listener
from util.periodicrun import periodicrun
from util.util import show_error_pattern, show_loading_pattern

show_loading_pattern()

# audio files loaded here
from modules.controller import Controller
import pynput.keyboard as keyboard

fps = 40

controller = Controller(
  config.read("MODE")
)

update_mode_queue = Queue()
def queue_set_mode(next_mode):
  update_mode_queue.put(next_mode, block=True, timeout=5)

skip_track_queue = Queue()
def queue_skip_track():
  skip_track_queue.put(1, block=True, timeout=5)

def loop():

    if config.read("SEND_LED_DATA"):
      show(controller.get_frame())

    if not update_mode_queue.empty():
      next_mode = update_mode_queue.get(block=True, timeout=0.5)
      controller.set_mode(next_mode)
    
    if not skip_track_queue.empty():
      skip_track_queue.get(block=True, timeout=0.5)
      controller.pl.skip_track()

    controller.update_frame()


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
  if loop_time > 0.025:
    print("warning: loop took too long (needs to be < 0.025):", loop_time)
    
  avg_loop_time = avg_loop_time + (loop_time - avg_loop_time) / frame_counter

autoplay_pressed = False # 2
metronome_pressed = False # 3
def on_press(key):
  global autoplay_pressed, metronome_pressed
  try:
    # print('alphanumeric key {0} pressed'.format(key.char))
    if autoplay_pressed:
      if key.char == '1':
        old_brightness = config.read("brightness")
        new_brightness = (old_brightness - 0.02)
        config.write("brightness", new_brightness, True)
        print(f"updated brightness to {new_brightness}")
        return True
      elif key.char == '3':
        old_brightness = config.read("brightness")
        new_brightness = (old_brightness + 0.02)
        config.write("brightness", new_brightness, True)
        print(f"updated brightness to {new_brightness}")  
        return True
      return True

    if metronome_pressed:
      if key.char == '1':
        old_brain_position = config.read("brain_position")
        new_brain_position = (old_brain_position - 1) % 10
        config.write("brain_position", new_brain_position, True)
        print(f"updated brain_position to {new_brain_position}")
        return True
      elif key.char == '2':
        old_brain_position = config.read("brain_position")
        new_brain_position = (old_brain_position + 1) % 10
        config.write("brain_position", new_brain_position, True)
        print(f"updated brain_position to {new_brain_position}")      
        return True
      return True

    if key.char == '1':
        if config.read("MODE") == "playlist":
            print("skipping track")
            queue_skip_track()
            return True
        print("setting mode to playlist")
        queue_set_mode("playlist")
    elif key.char == '2':
        print("setting mode to autoplay")
        queue_set_mode("autoplay")
        autoplay_pressed = True
    elif key.char == '3':
        print("setting mode to metronome")
        queue_set_mode("metronome")
        metronome_pressed = True
  except AttributeError:
    print('special key {0} pressed'.format(
      key))

def on_release(key):
  global autoplay_pressed, metronome_pressed
  # print('{0} released'.format(key))
  try:
    if key == keyboard.Key.esc:
      # Stop listener
      return False
    elif key.char == '2':
      autoplay_pressed = False
    elif key.char == '3':
      metronome_pressed = False
  except AttributeError:
    pass

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

# TODO try lower values on rpi
accuracy = 0.025 

if config.read("USE_PERFORMANCE_TIMING"):
  pr = periodicrun(1/fps, loop_timer, list(), 0, accuracy)
else:
  pr = periodicrun(1/fps, loop, list(), 0, accuracy)

try:
  pr.run()
except:
  print("some exception occurred.")
  show_error_pattern()
finally:
  audio_listener.thread_ender()
  # pr.interrupt()
  if config.read("USE_PERFORMANCE_TIMING"):
    print(f"avg loop time (ms): {1000*avg_loop_time:.1f}") 

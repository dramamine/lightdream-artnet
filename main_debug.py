from modes.playlist import Playlist
from modes.autoplay import Autoplay
from modules.artnet import show
from effects.effects import effects_manager
from util.config import config
from time import time
import modules.audio_input.runner as audio_listener
import pyglet
from modules.debug_view import update_pixels

event_loop = pyglet.app.EventLoop()
pyglet.options['debug_gl'] = False

@event_loop.event
def on_window_close(window):
    event_loop.exit()

fps = 40.0

# "playlist" | "autoplay" | "metronome"
mode = config['MODE']

pl = Playlist()
ap = Autoplay()

effects_manager.set_brightness(1.0)

if mode == "metronome":
  pl.test_metronome()
elif mode == "autoplay":
  ap.start()
elif mode == "playlist":
  pl.start()

def loop():
  if mode == "autoplay":
    frame = ap.tick()
    # @TODO apply fun filters based on song energy
    energy = audio_listener.get_energy()
    # print(energy)
  else:
    frame = pl.tick()

  frame = effects_manager.apply_effects(frame)

  update_pixels(frame)
    

  
def toggle_mode():
  if mode == "playlist":
    mode = "autoplay"
    ap.start()
  else:
    mode = "playlist"
    pl.restart()


start_time = time()
frame_counter = 0

# for debugging. can swap out for 'loop' for final build
def loop_timer(x):
  global frame_counter, start_time
  frame_counter = frame_counter + 1
  loop_timer = time()

  loop()

  # this should look pretty consistently as a multiple of 1
  if frame_counter % 40 == 0:
    print(time() - start_time)

  loop_time = time() - loop_timer
  if loop_time > 0.020:
    print("warning: loop took too long (needs to be < 0.025):", loop_time)

# WARNING: timing seems broken on Windows, runs too slow
pyglet.clock.schedule_interval(loop_timer, 1.0/fps)


try:
  pyglet.app.run()
finally:
  audio_listener.thread_ender()


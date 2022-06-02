import pyglet
import numpy as np
import os
from util.config import config
from modules.audio_input.runner import max_energy

WIDTH = 680
HEIGHT = 360
try:
  if config['AUDIO_DEBUG'] == True:
    HEIGHT = HEIGHT + 40
except:
  pass

win = pyglet.window.Window(width=WIDTH, height=HEIGHT)

ledscreen = pyglet.image.create(width=170, height=30)
leds = pyglet.sprite.Sprite(img=ledscreen, x=0, y=0)

red_image = pyglet.image.load(os.path.join("images", "debug", "red.png"))
green_image = pyglet.image.load(os.path.join("images", "debug", "green.png"))
audio_batch = pyglet.graphics.Batch()



# raw_sprite = pyglet.sprite.Sprite(img=green_image, x=0, y=0)

@win.event
def on_draw():
  leds.draw()
  audio_batch.draw()
  pass

###
### AUDIO DEBUGGER DISPLAY BELOW
###

FRAMES_TO_DISPLAY = int(WIDTH/20)

energy_original_images_bg = []
energy_original_images_fg = []

energy_modified_images_bg = []
energy_modified_images_fg = []

for i in range(0,FRAMES_TO_DISPLAY):
  energy_original_images_bg.append(pyglet.sprite.Sprite(img=green_image, x=20*i, y=360, batch=audio_batch))
  energy_original_images_fg.append(pyglet.sprite.Sprite(img=red_image, x=20*i, y=360, batch=audio_batch))
  energy_modified_images_bg.append(pyglet.sprite.Sprite(img=green_image, x=20*i, y=380, batch=audio_batch))
  energy_modified_images_fg.append(pyglet.sprite.Sprite(img=red_image, x=20*i, y=380, batch=audio_batch))


def energy_value_to_opacity(energy):
  percent = min(energy / max_energy, 1)
  return int(255 * percent)
  

def update_pixels(frame):
  global ledscreen, leds, raw_sprite
  # array is size 15300
  # 170 * 30 * 3
  # width * height * color data length
  data = np.reshape(frame, (170*30, 3))

  # add alpha channel
  data = np.insert(data, 3, 255, axis=1)

  ledscreen.set_data('RGBA', 170*4, data.tobytes())

  leds = pyglet.sprite.Sprite(img=ledscreen, x=0, y=0)
  leds.scale_x = 4
  leds.scale_y = 12


def update_audio_viewer(energy_original, energy_modified):
  for i in range(0,FRAMES_TO_DISPLAY):

    o = energy_value_to_opacity(energy_original[i])
    energy_original_images_fg[i].opacity = o
    energy_original_images_bg[i].opacity = 255-o

    p = energy_value_to_opacity(energy_modified[i])
    energy_modified_images_fg[i].opacity = p
    energy_modified_images_bg[i].opacity = 255-p
  pass
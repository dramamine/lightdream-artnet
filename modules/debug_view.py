import pyglet
import numpy as np

win = pyglet.window.Window(width=680, height=360)

ledscreen = pyglet.image.create(width=170, height=30)
leds = pyglet.sprite.Sprite(img=ledscreen, x=0, y=0)

@win.event
def on_draw():
  leds.draw()
  pass


def update_pixels(frame):
  global ledscreen, leds
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

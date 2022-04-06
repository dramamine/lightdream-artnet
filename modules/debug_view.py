import pyglet
import numpy as np

win = pyglet.window.Window(width=680, height=360)

ledscreen = pyglet.image.create(width=170, height=30)
print(type(ledscreen))
data = ledscreen.get_image_data().get_data()
print("image data:")
print(len(data))

# ledscreen.set_data('RGBA', 5*4, bytes(all_reds))

print(type(ledscreen))

leds = pyglet.sprite.Sprite(img=ledscreen, x=0, y=0)
# leds.scale = 4
# print(type(sprite))

@win.event
def on_draw():
  # ledscreen.blit(50, 50, 0)
  # win.clear()
  leds.draw()
  pass
    # ... drawing code ...


def update_pixels(frame):
  global ledscreen, leds
  data = np.delete(frame, (510,511), axis=1)
  # array is size 15300
  # 170 * 30 * 3
  # width * height * color data length
  data = np.reshape(data, (170*30, 3))

  # add alpha channel
  data = np.insert(data, 3, 255, axis=1)

  # print(data[0])
  # print( data[0].tobytes() )
  ledscreen.set_data('RGBA', 170*4, data.tobytes())

  leds = pyglet.sprite.Sprite(img=ledscreen, x=0, y=0)
  leds.scale_x = 4
  leds.scale_y = 12

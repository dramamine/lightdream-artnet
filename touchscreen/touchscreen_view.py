# https://github.com/pyglet/pyglet/blob/master/examples/input/tablet.py

# importing pyglet module
import pyglet

FULLSCREEN = False

# Scale factor is irrelevant if FULLSCREEN=True
SCALE_FACTOR = 0.5

# width of window
width = 2405 * SCALE_FACTOR

# height of window
height = 1367 * SCALE_FACTOR

# creating a window
window = pyglet.window.Window(width, height, 'lightdream', fullscreen=FULLSCREEN)

# render the layout
image = pyglet.image.load('../images/!touchscreen layout 3.png')
sprite = pyglet.sprite.Sprite(image, x=0, y=0)
sprite.scale = SCALE_FACTOR

# on draw event
@window.event
def on_draw():

    # clear the window
    window.clear()

    # draw the image on screen
    sprite.draw()

# TODO
# The tablets interface unavailable on OS X, per the pyglet docs
#   http://pyglet-current.readthedocs.io/en/latest/api/pyglet/input/pyglet.input.get_tablets.html
#
# For now, let's model some single-finger press/release/drag via the mouse events UI
#
# # # # # # # # # # # # # # # # # # # # # # # #
#
# tablet = pyglet.input.get_tablets()[0]  # ... there can be only one
#
# canvas = tablet.open(window)
#
# @canvas.event
# def on_enter(cursor):
#     print('%s: on_enter(%r)' % (name, cursor))
# @canvas.event
# def on_leave(cursor):
#     print('%s: on_leave(%r)' % (name, cursor))
# @canvas.event
# def on_motion(cursor, x, y, pressure, tilt_x, tilt_y):
#     print('%s: on_motion(%r, %r, %r, %r, %r, %r)' % (name, cursor, x, y, pressure, tilt_x, tilt_y))
#
# # # # # # # # # # # # # # # # # # # # # # # #

@window.event
def on_mouse_press(x, y, button, modifiers):
    print('mouse_press', x, y)

@window.event
def on_mouse_release(x, y, button, modifiers):
    print('mouse_release', x, y)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    print('mouse_drag', x, y, dx, dy, buttons, modifiers)

# start running the application
pyglet.app.run()
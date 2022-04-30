import pyglet

from touchscreen_circles import HUESHIFT
from touchscreen_circles import KALEIDOSCOPE
from touchscreen_circles import TUNNEL
from touchscreen_circles import LIGHTNING
from touchscreen_circles import NUCLEAR
from touchscreen_circles import SPIRAL
from touchscreen_circles import RADIANTLINES

from touchscreen_input import InputCoordinateMapper


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# TODO
# <0> Add touch events
# <1> Possibly fix filter / circle naming convention
# <2> Add RIGHT side circles
# <3> Implement other controls
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Set this to true to render the full layout png
# This is useful for testing the input_mapper
LAYOUT_TEST = False

# Set this to true when running in production
FULLSCREEN = False

# Scale factor is irrelevant if FULLSCREEN=True
SCALE_FACTOR = 0.5

# The full image dimensions of the layout
FULL_WIDTH = 2405
FULL_HEIGHT = 1357

# width of window
width = FULL_WIDTH * SCALE_FACTOR

# height of window
height = FULL_HEIGHT * SCALE_FACTOR

# creating a window
window = pyglet.window.Window(width, height, 'lightdream', fullscreen=FULLSCREEN)

# keep the real WxH for scaling
(REAL_WIDTH, REAL_HEIGHT) = window.get_size()


# tells the FingerManager which circles have active coordinates
input_mapper = InputCoordinateMapper(FULL_WIDTH)


def scale_image_coordinates(x, y):
    scaled_x = round((x / REAL_WIDTH) * FULL_WIDTH)
    scaled_y = round((y / REAL_HEIGHT) * FULL_HEIGHT)
    return (scaled_x, scaled_y)


def unscale_image_coordinates(x, y):
    scaled_x = round((x / FULL_WIDTH) * REAL_WIDTH)
    scaled_y = round((y / FULL_HEIGHT) * REAL_HEIGHT)
    return (scaled_x, scaled_y)


# test layout sprite
def get_layout_sprite():
    image = pyglet.image.load('./images/!touchscreen layout 3.png')
    sprite = pyglet.sprite.Sprite(image, x=0, y=0)
    sprite.scale = SCALE_FACTOR
    return sprite


def get_circle_sprite(circle, active=False):
    path = circle.path
    if active:
        path = path.replace('.png', '-active.png')
    image = pyglet.image.load(path)
    lower_right = unscale_image_coordinates(circle.X, circle.Y)
    sprite = pyglet.sprite.Sprite(image, x=lower_right[0], y=lower_right[1])
    sprite.scale = circle.SCALE
    return sprite


def draw_circle(key, sprite, sprite_active):
    if input_mapper.is_active(key):
        sprite_active.draw()
    else:
        sprite.draw()


# layout test sprite
sprite_layout = get_layout_sprite()

# circle sprites - inactive
sprite_hueshift = get_circle_sprite(HUESHIFT)
sprite_kaleidoscope = get_circle_sprite(KALEIDOSCOPE)
sprite_tunnel = get_circle_sprite(TUNNEL)
sprite_lightning = get_circle_sprite(LIGHTNING)
sprite_nuclear = get_circle_sprite(NUCLEAR)
sprite_spiral = get_circle_sprite(SPIRAL)
sprite_radiantlines = get_circle_sprite(RADIANTLINES)

# circle sprites - active
sprite_hueshift_active = get_circle_sprite(HUESHIFT, active=True)
sprite_kaleidoscope_active = get_circle_sprite(KALEIDOSCOPE, active=True)
sprite_tunnel_active = get_circle_sprite(TUNNEL, active=True)
sprite_lightning_active = get_circle_sprite(LIGHTNING, active=True)
sprite_nuclear_active = get_circle_sprite(NUCLEAR, active=True)
sprite_spiral_active = get_circle_sprite(SPIRAL, active=True)
sprite_radiantlines_active = get_circle_sprite(RADIANTLINES, active=True)


# on draw event
@window.event
def on_draw():

    # clear the window
    window.clear()

    if LAYOUT_TEST:
        sprite_layout.draw()
        return

    draw_circle(HUESHIFT.key, sprite_hueshift, sprite_hueshift_active)
    draw_circle(KALEIDOSCOPE.key, sprite_kaleidoscope, sprite_kaleidoscope_active)
    draw_circle(TUNNEL.key, sprite_tunnel, sprite_tunnel_active)
    draw_circle(LIGHTNING.key, sprite_lightning, sprite_lightning_active)
    draw_circle(NUCLEAR.key, sprite_nuclear, sprite_nuclear_active)
    draw_circle(SPIRAL.key, sprite_spiral, sprite_spiral_active)
    draw_circle(RADIANTLINES.key, sprite_radiantlines, sprite_radiantlines_active)


@window.event
def on_mouse_press(x, y, button, modifiers):
    point = scale_image_coordinates(x,y)
    print("point", point)
    input_mapper.process_mouse_down(point)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    point = scale_image_coordinates(x,y)
    input_mapper.process_mouse_down(point)


@window.event
def on_mouse_release(x, y, button, modifiers):
    point = scale_image_coordinates(x,y)
    input_mapper.process_mouse_up()


# TODO - Tablet event listeners
#
# https://github.com/pyglet/pyglet/blob/master/examples/input/tablet.py
#
# The tablets interface unavailable on OS X, per the pyglet docs
#   http://pyglet-current.readthedocs.io/en/latest/api/pyglet/input/pyglet.input.get_tablets.html
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


pyglet.app.run()



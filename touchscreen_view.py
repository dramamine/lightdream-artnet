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

# The full image dimensions of the layout image
LAYOUT_IMAGE_WIDTH = 2405
LAYOUT_IMAGE_HEIGHT = 1357

# Scale factor is irrelevant if FULLSCREEN=True
LAYOUT_TEST_SCALE_FACTOR = 0.5

# width of window
width = LAYOUT_IMAGE_WIDTH * LAYOUT_TEST_SCALE_FACTOR

# height of window
height = LAYOUT_IMAGE_HEIGHT * LAYOUT_TEST_SCALE_FACTOR

# creating a window
window = pyglet.window.Window(width, height, 'lightdream', fullscreen=FULLSCREEN)

# keep the real WxH for scaling
(WINDOW_WIDTH, WINDOW_HEIGHT) = window.get_size()


# tells the FingerManager which circles have active coordinates
input_mapper = InputCoordinateMapper(LAYOUT_IMAGE_WIDTH)


# when detecting circles, use coordinates scaled to the layout image
def layout_image_coordinates(x, y):
    scaled_x = round((x / WINDOW_WIDTH) * LAYOUT_IMAGE_WIDTH)
    scaled_y = round((y / WINDOW_HEIGHT) * LAYOUT_IMAGE_HEIGHT)
    return (scaled_x, scaled_y)


# when placing sprites, use coordinates scaled to the window
def window_coordinates(x, y):
    scaled_x = round((x / LAYOUT_IMAGE_WIDTH) * WINDOW_WIDTH)
    scaled_y = round((y / LAYOUT_IMAGE_HEIGHT) * WINDOW_HEIGHT)
    return (scaled_x, scaled_y)


def get_layout_test_sprite():
    image = pyglet.image.load('./images/!touchscreen layout 3.png')
    sprite = pyglet.sprite.Sprite(image, x=0, y=0)
    sprite.scale = LAYOUT_TEST_SCALE_FACTOR
    return sprite


def get_circle_sprite(circle, active=False):
    path = circle.path
    if active:
        path = path.replace('.png', '-active.png')
    image = pyglet.image.load(path)

    # use window coords, instead of layout image coords, for image placement
    lower_left = window_coordinates(circle.X, circle.Y)

    # sprites are placed from the lower left corner
    sprite = pyglet.sprite.Sprite(image, x=lower_left[0], y=lower_left[1])

    # scales the image down to the right size for the layout
    sprite.scale = circle.SCALE

    return sprite


def draw_circle(key, sprite_pair):
    if input_mapper.is_active(key):
        sprite_pair[1].draw()
    else:
        sprite_pair[0].draw()


sprite_pair_hueshift = [
    get_circle_sprite(HUESHIFT),
    get_circle_sprite(HUESHIFT, active=True)
]
sprite_pair_kaleidoscope = [
    get_circle_sprite(KALEIDOSCOPE),
    get_circle_sprite(KALEIDOSCOPE, active=True)
]
sprite_pair_tunnel = [
    get_circle_sprite(TUNNEL),
    get_circle_sprite(TUNNEL, active=True)
]
sprite_pair_lightning = [
    get_circle_sprite(LIGHTNING),
    get_circle_sprite(LIGHTNING, active=True)
]
sprite_pair_nuclear = [
    get_circle_sprite(NUCLEAR),
    get_circle_sprite(NUCLEAR, active=True)
]
sprite_pair_spiral = [
    get_circle_sprite(SPIRAL),
    get_circle_sprite(SPIRAL, active=True)
]
sprite_pair_radiantlines = [
    get_circle_sprite(RADIANTLINES),
    get_circle_sprite(RADIANTLINES, active=True)
]


# layout test sprite - for coordinate testing purposes only
sprite_layout = get_layout_test_sprite()


# on draw event
@window.event
def on_draw():

    # clear the window
    window.clear()

    if LAYOUT_TEST:
        sprite_layout.draw()
        return

    draw_circle(HUESHIFT.key, sprite_pair_hueshift)
    draw_circle(KALEIDOSCOPE.key, sprite_pair_kaleidoscope)
    draw_circle(TUNNEL.key, sprite_pair_tunnel)
    draw_circle(LIGHTNING.key, sprite_pair_lightning)
    draw_circle(NUCLEAR.key, sprite_pair_nuclear)
    draw_circle(SPIRAL.key, sprite_pair_spiral)
    draw_circle(RADIANTLINES.key, sprite_pair_radiantlines)


@window.event
def on_mouse_press(x, y, button, modifiers):
    point = layout_image_coordinates(x,y)
    print("point", point)
    input_mapper.process_mouse_down(point)


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    point = layout_image_coordinates(x,y)
    input_mapper.process_mouse_down(point)


@window.event
def on_mouse_release(x, y, button, modifiers):
    point = layout_image_coordinates(x,y)
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

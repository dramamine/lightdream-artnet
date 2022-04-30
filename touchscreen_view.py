# https://github.com/pyglet/pyglet/blob/master/examples/input/tablet.py

import math
import pyglet

from modules.fingers import finger_manager

# Set this to true when running in production
FULLSCREEN = False

# Scale factor is irrelevant if FULLSCREEN=True
SCALE_FACTOR = 0.5

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

# render the layout
image = pyglet.image.load('./images/!touchscreen layout 3.png')
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

def scale_image_coordinates(x, y):
    scaled_x = round(x / REAL_WIDTH * FULL_WIDTH)
    scaled_y = round(y / REAL_HEIGHT * FULL_HEIGHT)
    return (scaled_x, scaled_y)


# TODO
# <0> Find centerpoint for each circle
# <1> Render the layout as a black background with the other sprites on top of it
# <2> on touch events, add the touches to the finger manager
# <3> during render, render the sprites as active or inactive by checking finger manager


class TouchscreenCircle:
    def __init__(self, key, center, radius):
        self.key = key
        self.center = center
        self.radius = radius

    # we can use this to place the image sprites
    def upper_left_corner(self):
        x = center[0] - radius
        y = center[1] + radius
        return (x, y)


class InputCoordinateMapper:
    open_cursors = {}

    def __init__(self):
        # order by radius, to check the biggest circles first
        self.CIRCLES = [
            # TODO - replace hardcoded key names with Filter.key values
            TouchscreenCircle('hueshift', (312, 683), 262),
            TouchscreenCircle('lightning', (414, 146), 106),
            TouchscreenCircle('nuclear', (166, 260), 106),
            TouchscreenCircle('spiral', (160, 1095), 106),
            TouchscreenCircle('radiant-lines', (416, 1205), 106),
        ]

    def get_touchscreen_circle_key(self, point):
        for circle in self.CIRCLES:
            if self.circle_contains_point(circle, point):
                return circle.key
        return None

    # triangles!
    def circle_contains_point(self, circle, point):
        side_a = point[0] - circle.center[0]
        side_b = point[1] - circle.center[1]
        side_c = math.sqrt(side_a**2 + side_b**2)
        return side_c < circle.radius

    def update_fingers(self):
        # clear everything
        finger_manager.clear_all_values()
        # for each cursor
        for _, cursor_key in enumerate(self.open_cursors):
            cursor = self.open_cursors[cursor_key]
            circle_key = self.get_touchscreen_circle_key(cursor)
            # if it is in a circle, update that circle
            if circle_key:
                finger_manager.append(circle_key, cursor)

    def process_mouse_down(self, point):
        self.open_cursors['mouse'] = point
        self.update_fingers()

    def process_mouse_up(self):
        del self.open_cursors['mouse']
        self.update_fingers()

    def process_touch_enter(self, cursor, point):
        self.open_cursors[cursor] = point
        self.update_fingers()

    def process_touch_motion(self, cursor, point):
        self.open_cursors[cursor] = point
        self.update_fingers()

    def process_touch_leave(self, cursor):
        del self.open_cursors[cursor]
        self.update_fingers()


input_mapper = InputCoordinateMapper()


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


pyglet.app.run()



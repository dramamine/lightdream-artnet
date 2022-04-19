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
    scaled_x = round(x / width * FULL_WIDTH)
    scaled_y = round(y / height * FULL_HEIGHT)
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
        # Replace hardcoded key names with Filter.key values
        self.NUCLEAR = TouchscreenCircle('nuclear', (166, 260), 66)

    # triangles!
    def circle_contains_point(self, circle, point):
        side_a = point[0] - circle.center[0]
        side_b = point[1] - circle.center[1]
        side_c = math.sqrt(side_a**2 + side_b**2)
        return side_c < circle.radius

    def get_touchscreen_circle_key(self, point):
        # TODO - check the biggest circles first
        if self.circle_contains_point(self.NUCLEAR, point):
            # return as soon as we've found a circle
            return self.NUCLEAR.key
        return None

    def process_mouse_down(self, point):
        self.open_cursors['mouse'] = point

        finger_manager.clear_values(self.NUCLEAR.key)
        for index, cursor_key in enumerate(self.open_cursors):
            cursor = self.open_cursors[cursor_key]
            if self.get_touchscreen_circle_key(cursor) == self.NUCLEAR.key:
                finger_manager.append(self.NUCLEAR.key, cursor)

    def process_mouse_up(self):
        del self.open_cursors['mouse']
        # Clear all values from the finger manager.  NO TOUCHING
        finger_manager.clear_values(self.NUCLEAR.key)

    def process_touch_enter(self, cursor, point):
        # register the cursor with the input mapper
        pass

    def process_touch_motion(self, cursor, point):
        # update the values for the cursor
        # get all cursor values and send to finger_manager
        pass

    def process_touch_leave(self, cursor):
        # remove the cursor from the input mapper
        pass


input_mapper = InputCoordinateMapper()


@window.event
def on_mouse_press(x, y, button, modifiers):
    point = scale_image_coordinates(x,y)
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



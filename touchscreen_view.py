# https://github.com/pyglet/pyglet/blob/master/examples/input/tablet.py

import math
import pyglet

from modules.fingers import finger_manager
from effects.filters import FilterNames

# Set this to true when running in production
FULLSCREEN = True

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


def scale_image_coordinates(x, y):
    scaled_x = round((x / REAL_WIDTH) * FULL_WIDTH)
    scaled_y = round((y / REAL_HEIGHT) * FULL_HEIGHT)
    return (scaled_x, scaled_y)


def unscale_image_coordinates(x, y):
    scaled_x = round((x / FULL_WIDTH) * REAL_WIDTH)
    scaled_y = round((y / FULL_HEIGHT) * REAL_HEIGHT)
    return (scaled_x, scaled_y)


# TODO
# <0> Add touch events
# <1> Possibly fix filter / circle naming convention
# <2> Add right side circles
# <3> Implement other controls


class TouchscreenCircle:
    def __init__(self, path='', key='', center=None, radius=0, full_image_radius=0):
        self.path = path
        self.key = key
        self.center = center
        self.radius = radius
        self.full_image_radius = full_image_radius

    # we can use this to place the image sprites
    def lower_right_corner(self):
        x = self.center[0] - self.radius
        y = self.center[1] - self.radius
        return (x, y)

    @property
    def X(self):
        return self.lower_right_corner()[0]

    @property
    def Y(self):
        return self.lower_right_corner()[1]

    @property
    def SCALE(self):
        return self.radius / self.full_image_radius


# LEFT bigger circles
HUESHIFT = TouchscreenCircle(
    path='./images/colorwheel-dithered.png',
    key=FilterNames.HUESHIFT,
    center=(312, 683),
    radius=262,
    full_image_radius=739
)
KALEIDOSCOPE = TouchscreenCircle(
    path='./images/kaleidoscope.png',
    key=FilterNames.KALEIDOSCOPE,
    center=(850, 1015),
    radius=262,
    full_image_radius=799
)
TUNNEL = TouchscreenCircle(
    path='./images/tunnel.png',
    key=FilterNames.TUNNEL,
    center=(850, 288),
    radius=262,
    full_image_radius=763
)
# LEFT smaller circles
LIGHTNING = TouchscreenCircle(
    path='./images/lightning.png',
    key=FilterNames.LIGHTNING,
    center=(414, 146),
    radius=106,
    full_image_radius=482
)
NUCLEAR = TouchscreenCircle(
    path='./images/nuclear.png',
    key=FilterNames.NUCLEAR,
    center=(166, 260),
    radius=106,
    full_image_radius=498
)
SPIRAL = TouchscreenCircle(
    path='./images/spiral.png',
    key=FilterNames.SPIRAL,
    center=(160, 1095),
    radius=106,
    full_image_radius=498
)
RADIANTLINES = TouchscreenCircle(
    path='./images/radiant-lines.png',
    key=FilterNames.RADIANTLINES,
    center=(416, 1205),
    radius=106,
    full_image_radius=498
)


class InputCoordinateMapper:
    open_cursors = {}

    def __init__(self):
        # order by radius, to check the biggest circles first
        self.LEFT_CIRCLES = [
            # big circles
            HUESHIFT,
            KALEIDOSCOPE,
            TUNNEL,
            # small circles
            LIGHTNING,
            NUCLEAR,
            SPIRAL,
            RADIANTLINES,
        ]
        self.RIGHT_CIRCLES = []

    def get_touchscreen_circle_key(self, point):
        # divide circles into LEFT and RIGHT for half as many compares
        if point[0] < FULL_WIDTH / 2:
            for circle in self.LEFT_CIRCLES:
                if self.circle_contains_point(circle, point):
                    return circle.key
        else:
            for circle in self.RIGHT_CIRCLES:
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


# TODO
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


# test layout sprite
LAYOUT_TEST = False
image_layout = pyglet.image.load('./images/!touchscreen layout 3.png')
sprite_layout = pyglet.sprite.Sprite(image_layout, x=0, y=0)
sprite_layout.scale = SCALE_FACTOR


def get_circle_sprite(circle, active=False):
    path = circle.path
    if active:
        path = path.replace('.png', '-active.png')
    image = pyglet.image.load(path)
    lower_right = unscale_image_coordinates(circle.X, circle.Y)
    sprite = pyglet.sprite.Sprite(image, x=lower_right[0], y=lower_right[1])
    sprite.scale = circle.SCALE
    return sprite


# circle sprites - inactive
sprite_hueshift = get_circle_sprite(HUESHIFT)
sprite_kaleidoscope = get_circle_sprite(KALEIDOSCOPE)
sprite_tunnel = get_circle_sprite(TUNNEL)
sprite_lightning = get_circle_sprite(LIGHTNING)
sprite_nuclear = get_circle_sprite(NUCLEAR)
sprite_spiral = get_circle_sprite(SPIRAL)
sprite_radiantlines = get_circle_sprite(RADIANTLINES)

sprite_hueshift_active = get_circle_sprite(HUESHIFT, active=True)
sprite_kaleidoscope_active = get_circle_sprite(KALEIDOSCOPE, active=True)
sprite_tunnel_active = get_circle_sprite(TUNNEL, active=True)
sprite_lightning_active = get_circle_sprite(LIGHTNING, active=True)
sprite_nuclear_active = get_circle_sprite(NUCLEAR, active=True)
sprite_spiral_active = get_circle_sprite(SPIRAL, active=True)
sprite_radiantlines_active = get_circle_sprite(RADIANTLINES, active=True)


def draw_circle(key, sprite, sprite_active, finger_manager):
    if bool(finger_manager.get_values(key)):
        sprite_active.draw()
    else:
        sprite.draw()


# on draw event
@window.event
def on_draw():

    # clear the window
    window.clear()

    if LAYOUT_TEST:
        sprite_layout.draw()
        return

    draw_circle(HUESHIFT.key, sprite_hueshift, sprite_hueshift_active, finger_manager)
    draw_circle(KALEIDOSCOPE.key, sprite_kaleidoscope, sprite_kaleidoscope_active, finger_manager)
    draw_circle(TUNNEL.key, sprite_tunnel, sprite_tunnel_active, finger_manager)
    draw_circle(LIGHTNING.key, sprite_lightning, sprite_lightning_active, finger_manager)
    draw_circle(NUCLEAR.key, sprite_nuclear, sprite_nuclear_active, finger_manager)
    draw_circle(SPIRAL.key, sprite_spiral, sprite_spiral_active, finger_manager)
    draw_circle(RADIANTLINES.key, sprite_radiantlines, sprite_radiantlines_active, finger_manager)


pyglet.app.run()



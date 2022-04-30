import math

from modules.fingers import finger_manager

from touchscreen_circles import HUESHIFT
from touchscreen_circles import KALEIDOSCOPE
from touchscreen_circles import TUNNEL
from touchscreen_circles import LIGHTNING
from touchscreen_circles import NUCLEAR
from touchscreen_circles import SPIRAL
from touchscreen_circles import RADIANTLINES


class InputCoordinateMapper:
    """
    Provides the following mouse and touch bindings:

        process_mouse_down
        process_mouse_up

        process_touch_enter
        process_touch_motion
        process_touch_leave

    When one of these methods is called with (x,y) coordinates, InputCoordinateMapper
    finds out which circle that point falls in (if any), and updates that circle's
    entry in the FingerManager.
    """
    open_cursors = {}

    def __init__(self, full_width):
        self.FULL_WIDTH = full_width

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
        self.RIGHT_CIRCLES = [
            # TODO
        ]

    def get_touchscreen_circle_key(self, point):
        # divide circles into LEFT and RIGHT for half as many compares
        if point[0] < self.FULL_WIDTH / 2:
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
                # TODO - probably we'll want radians instead of scaled x,y coords here
                finger_manager.append(circle_key, cursor)

    # Mouse Bindings

    def process_mouse_down(self, point):
        self.open_cursors['mouse'] = point
        self.update_fingers()

    def process_mouse_up(self):
        del self.open_cursors['mouse']
        self.update_fingers()

    # Touch Bindings

    def process_touch_enter(self, cursor, point):
        self.open_cursors[cursor] = point
        self.update_fingers()

    def process_touch_motion(self, cursor, point):
        self.open_cursors[cursor] = point
        self.update_fingers()

    def process_touch_leave(self, cursor):
        del self.open_cursors[cursor]
        self.update_fingers()

    def is_active(self, key):
        return bool(finger_manager.get_values(key))


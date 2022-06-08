from kivy.app import App
from kivy.config import Config
from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen

from touchscreen_circles import HUESHIFT
from touchscreen_circles import KALEIDOSCOPE
from touchscreen_circles import TUNNEL
from touchscreen_circles import LIGHTNING
from touchscreen_circles import NUCLEAR
from touchscreen_circles import SPIRAL
from touchscreen_circles import RADIANTLINES

from touchscreen_input import InputCoordinateMapper


LAYOUT_IMAGE_WIDTH = 2405
LAYOUT_IMAGE_HEIGHT = 1357


# TODO - get this from real window if necessary
WINDOW_WIDTH, WINDOW_HEIGHT = LAYOUT_IMAGE_WIDTH, LAYOUT_IMAGE_HEIGHT


input_mapper = InputCoordinateMapper(LAYOUT_IMAGE_WIDTH)


Config.set('graphics', 'width', LAYOUT_IMAGE_WIDTH)
Config.set('graphics', 'height', LAYOUT_IMAGE_HEIGHT)


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


class Touchable(Screen):
    def on_touch_down(self, touch):
        point = layout_image_coordinates(touch.x, touch.y)
        # print("point", point)
        input_mapper.process_touch_enter(touch.id, point)

    def on_touch_move(self, touch):
        point = layout_image_coordinates(touch.x, touch.y)
        input_mapper.process_touch_motion(touch.id, point)

    def on_touch_up(self, touch):
        point = layout_image_coordinates(touch.x, touch.y)
        input_mapper.process_touch_leave(touch.id)


class LightdreamTouchScreen(Touchable):
    CIRCLES = {
        'HUESHIFT': HUESHIFT,
        'KALEIDOSCOPE': KALEIDOSCOPE,
        'TUNNEL': TUNNEL,
        'LIGHTNING': LIGHTNING,
        'NUCLEAR': NUCLEAR,
        'SPIRAL': SPIRAL,
        'RADIANTLINES': RADIANTLINES,
    }
    def __init__(self):
        super().__init__()
        for circle in self.CIRCLES.keys():
            self.ids[circle].source = self.CIRCLES[circle].path

    def update_active(self):
        for circle in self.CIRCLES.keys():
            circle_config = self.CIRCLES[circle]
            if input_mapper.is_active(circle_config.key):
                self.ids[circle].source = circle_config.path.replace('.png', '-active.png')
            else:
                self.ids[circle].source = circle_config.path

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        self.update_active()

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        self.update_active()

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        self.update_active()


class LayoutTestScreen(Touchable):
    pass


class MainApp(App):
    def build(self):
        # return LayoutTestScreen()
        return LightdreamTouchScreen()


if __name__ == '__main__':
    MainApp().run()

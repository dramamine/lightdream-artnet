from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.core.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty

from touchscreen_circles import HUESHIFT
from touchscreen_circles import NUCLEAR

from touchscreen_input import InputCoordinateMapper


LAYOUT_IMAGE_WIDTH = 2405
LAYOUT_IMAGE_HEIGHT = 1357


# TODO - get this from real window if necessary
WINDOW_WIDTH, WINDOW_HEIGHT = LAYOUT_IMAGE_WIDTH, LAYOUT_IMAGE_HEIGHT


input_mapper = InputCoordinateMapper(LAYOUT_IMAGE_WIDTH)


from kivy.config import Config
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
        input_mapper.process_touch_enter("TODO", point)

    def on_touch_move(self, touch):
        point = layout_image_coordinates(touch.x, touch.y)
        # print("point", point)
        input_mapper.process_touch_motion("TODO", point)

    def on_touch_up(self, touch):
        point = layout_image_coordinates(touch.x, touch.y)
        # print("point", point)
        input_mapper.process_touch_leave("TODO")


class LightdreamTouchScreen(Touchable):
    CIRCLE_IDS = [
        'HUESHIFT',
    ]
    def __init__(self):
        super().__init__()
        self.ids.HUESHIFT.source = HUESHIFT.path

    def update_active(self):
        for circle in self.CIRCLE_IDS:
            if input_mapper.is_active(HUESHIFT.key):
                self.ids['HUESHIFT'].source = HUESHIFT.path.replace('.png', '-active.png')
            else:
                self.ids['HUESHIFT'].source = HUESHIFT.path

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

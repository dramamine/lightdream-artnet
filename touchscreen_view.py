from kivy.app import App
from kivy.config import Config
from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

from touch_circles import HUESHIFT
from touch_circles import KALEIDOSCOPE
from touch_circles import TUNNEL
from touch_circles import LIGHTNING
from touch_circles import NUCLEAR
from touch_circles import SPIRAL
from touch_circles import RADIANTLINES

from touch_input import InputCoordinateMapper


LAYOUT_IMAGE_WIDTH = 1920
LAYOUT_IMAGE_HEIGHT = 1080


Config.set('graphics', 'width', LAYOUT_IMAGE_WIDTH)
Config.set('graphics', 'height', LAYOUT_IMAGE_HEIGHT)


input_mapper = InputCoordinateMapper(LAYOUT_IMAGE_WIDTH)


class TouchableScreen(Screen):
    def on_touch_down(self, touch):
        point = (touch.x, touch.y)
        # print("============================>point", point)
        input_mapper.process_touch_enter(touch.id, point)

        # Annoying: touch bindings on the TouchableScreens override all button
        # press bindings.  DebugMenu screen has working on_press() bindings,
        # and shouldn't need to check for button collisions in the touch handler.
        if self.ids.NEXT_SCREEN_BUTTON.collide_point(*touch.pos):
            self.next_screen_callback(touch)

        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        point = (touch.x, touch.y)
        input_mapper.process_touch_motion(touch.id, point)
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        point = (touch.x, touch.y)
        input_mapper.process_touch_leave(touch.id)
        return super().on_touch_up(touch)

    def next_screen_callback(self):
        pass


class LightdreamTouchScreen(TouchableScreen):
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
            self.ids[circle].center_x = self.CIRCLES[circle].center[0]
            self.ids[circle].center_y = self.CIRCLES[circle].center[1]

    def update_active(self):
        for circle in self.CIRCLES.keys():
            circle_config = self.CIRCLES[circle]
            if input_mapper.is_active(circle_config.key):
                self.ids[circle].source = circle_config.active_path
            else:
                self.ids[circle].source = circle_config.path

    def on_touch_down(self, touch):
        self.update_active()
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        self.update_active()
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        self.update_active()
        return super().on_touch_up(touch)

    def next_screen_callback(self, touch):
        self.manager.current = 'debug_menu'
        self.manager.title = 'Debug Menu'


class DebugMenuScreen(Screen):
    def next_screen_callback(self, touch):
        self.manager.current = 'layout_test'
        self.manager.title = 'Layout Test'


class LayoutTestScreen(TouchableScreen):
    def next_screen_callback(self, touch):
        self.manager.current = 'lightdream'
        self.manager.title = 'Lightdream'


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LightdreamTouchScreen(), name='lightdream')
        sm.add_widget(DebugMenuScreen(), name='debug_menu')
        sm.add_widget(LayoutTestScreen(), name='layout_test')
        return sm


if __name__ == '__main__':
    MainApp().run()

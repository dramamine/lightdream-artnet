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

from util.track_metadata import track_metadata


LAYOUT_IMAGE_WIDTH = 1920
LAYOUT_IMAGE_HEIGHT = 1080


Config.set('graphics', 'width', LAYOUT_IMAGE_WIDTH)
Config.set('graphics', 'height', LAYOUT_IMAGE_HEIGHT)


input_mapper = InputCoordinateMapper(LAYOUT_IMAGE_WIDTH)

touchscreen_api = {
  'enqueue': lambda track_name: None,
  'dequeue': lambda track_name: None,
  'skip_track': lambda x: None,
  'set_mode': lambda mode: None,
  'config': {}
}

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


def enqueue(evt):
    touchscreen_api['enqueue'](evt.value)

def dequeue(evt):
    touchscreen_api['dequeue'](evt.value)

def skip_track(evt):
    touchscreen_api['skip_track']()

class DebugMenuScreen(Screen):
    def __init__(self):
        super().__init__()

        for id, track in track_metadata.items():
            artist_name = track['artist_name']
            track_name = track['track_name']
            display_name = f'{artist_name} - {track_name}'
            btn = Button(
                text=display_name,
                font_size="15sp"
            )
            btn.value = id # @TODO could we use 'name' here instead
            btn.bind(on_press=enqueue)
            self.ids['track_grid'].add_widget(btn)

    def next_screen_callback(self, touch):
        self.manager.current = 'layout_test'
        self.manager.title = 'Layout Test'
    
    def update_track_queue(self, now_playing, queue):
        print("OMG got my message:", now_playing, queue)
        track_queue_layout = self.ids['track_queue']
        track_queue_layout.clear_widgets()

        # now playing
        track_name = track_metadata[now_playing]['track_name']
        btn = Button(
            text=f'NOW PLAYING: {track_name}',
            font_size="15sp",
            size_hint_y = None
        )
        btn.bind(on_press=skip_track)
        track_queue_layout.add_widget(btn)
        
        # upcoming
        for track_id in queue:
            track_name = track_metadata[track_id]['track_name']
            btn = Button(
                text=track_name,
                font_size="15sp",
                size_hint_y = None
            )
            btn.value = track_id
            btn.bind(on_press=dequeue)
            track_queue_layout.add_widget(btn)




class LayoutTestScreen(TouchableScreen):
    def next_screen_callback(self, touch):
        self.manager.current = 'lightdream'
        self.manager.title = 'Lightdream'


class MainApp(App):
    def build(self):
        print("hello from build")
        sm = ScreenManager()
        self.debug_menu = DebugMenuScreen()
        sm.add_widget(self.debug_menu, name='debug_menu')
        sm.add_widget(LightdreamTouchScreen(), name='lightdream')
        sm.add_widget(LayoutTestScreen(), name='layout_test')
        return sm

    def stupid_updated_queue_callback(self, now_playing, queue):
        if self.debug_menu:
            self.debug_menu.update_track_queue(now_playing, queue)

    def add_touchscreen_api(self, api):
        global touchscreen_api
        touchscreen_api = api
        # print("on the right track?", self.debug_menu)


if __name__ == '__main__':
    MainApp().run()

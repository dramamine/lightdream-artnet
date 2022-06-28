from kivy.app import App
from kivy.config import Config
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, ObjectProperty

from touch_circles import HUESHIFT
from touch_circles import KALEIDOSCOPE
from touch_circles import TUNNEL
from touch_circles import LIGHTNING
from touch_circles import NUCLEAR
from touch_circles import SPIRAL
from touch_circles import RADIANTLINES
from touch_circles import RINGS
from touch_circles import SPOTLIGHT
from touch_circles import WEDGES
from touch_circles import TRIFORCE
from touch_circles import BLOBS


from touch_input import InputCoordinateMapper

from util.track_metadata import track_metadata
from util.config import config


LAYOUT_IMAGE_WIDTH = 1920
LAYOUT_IMAGE_HEIGHT = 1080


Config.set('graphics', 'width', LAYOUT_IMAGE_WIDTH)
Config.set('graphics', 'height', LAYOUT_IMAGE_HEIGHT)


FULLSCREEN_MODE = False


if FULLSCREEN_MODE:
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'window_state', 'maximized')


input_mapper = InputCoordinateMapper(LAYOUT_IMAGE_WIDTH)


CURRENTLY_ENABLED_SCREENS = [
    'lightdream',
    'debug_menu',
    # 'layout_test',
]


def get_next_screen(this_screen):
    screens = CURRENTLY_ENABLED_SCREENS
    return screens[screens.index(this_screen) + 1 - len(screens)]


touchscreen_api = {
  'enqueue': lambda track_name: None,
  'dequeue': lambda track_name: None,
  'skip_track': lambda x: None,
  'set_mode': lambda mode: None,
  # 'config': {}
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
            # Only go to next screen on double tap
            if touch.is_double_tap:
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

    def next_screen_callback(self, touch):
        self.manager.current = get_next_screen(self.manager.current)


class LayoutTestScreen(TouchableScreen):
    pass


class LightdreamTouchScreen(TouchableScreen):
    led_output_texture = ObjectProperty()
    CIRCLES = {
        'HUESHIFT': HUESHIFT,
        'KALEIDOSCOPE': KALEIDOSCOPE,
        'TUNNEL': TUNNEL,
        'LIGHTNING': LIGHTNING,
        'NUCLEAR': NUCLEAR,
        'SPIRAL': SPIRAL,
        'RADIANTLINES': RADIANTLINES,
        'RINGS': RINGS,
        'SPOTLIGHT': SPOTLIGHT,
        'WEDGES': WEDGES,
        'TRIFORCE': TRIFORCE,
        'BLOBS': BLOBS,
    }
    def __init__(self):
        super().__init__()
        for circle in self.CIRCLES.keys():
            self.ids[circle].source = self.CIRCLES[circle].path
            self.ids[circle].center_x = self.CIRCLES[circle].center[0]
            self.ids[circle].center_y = self.CIRCLES[circle].center[1]

        if config.read("LED_VIEWER") == True:
            self.led_output_texture = Texture.create(size=(170,30))
            with self.canvas:
                Rectangle(
                    size=(340,60),
                    pos=(0,1020),
                    texture=self.led_output_texture)

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



def enqueue(evt):
    touchscreen_api['enqueue'](evt.value)

def dequeue(evt):
    touchscreen_api['dequeue'](evt.value)

def skip_track(evt):
    touchscreen_api['skip_track']()


class DebugMenuScreen(Screen):
    led_output_texture = ObjectProperty()
    energy_original_texture = ObjectProperty()
    energy_modified_texture = ObjectProperty()
    def __init__(self):
        super().__init__()

        # create buttons for each track
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

        # read slider values from config
        slider_ids = [
            'decay_constant',
            'max_energy',
            'aural_effect_strength_multiplier',
            'autoplay_interval',
            'autoplay_crossfade',
            'brain_position'
        ]
        for slider_id in slider_ids:
            value = config.read(slider_id)
            self.ids[slider_id].value = value
            self.ids[f'{slider_id}_value'].text = str(value)

        self.set_mode(config.read("MODE"))

        if config.read("LED_VIEWER") == True:
            self.led_output_texture = Texture.create(size=(170,30))
            with self.canvas:
                Rectangle(
                    size=(340,60),
                    pos=(0,1020),
                    texture=self.led_output_texture)

        self.energy_original_texture = Texture.create(size=(20,1))
        self.energy_modified_texture = Texture.create(size=(20,1))

    def next_screen_callback(self, touch):
        self.manager.current = get_next_screen(self.manager.current)

    # set MODE and update controls appropriately
    def set_mode(self, mode):
        config.write("MODE", mode)
        touchscreen_api['set_mode'](mode)

        # crappy code to show only the mode controller we want
        controllers = ['playlist_controller', 'autoplay_controller', 'metronome_controller']
        for controller in controllers:
            self.update_visibility(controller, False)
        self.update_visibility(f'{mode}_controller', True)

    # toggle visibility of Layouts
    def update_visibility(self, id, is_visible):
        widget = self.ids[id]
        widget.opacity = 1 if is_visible else 0
        widget.disabled = False if is_visible else True
        widget.height = 1 if is_visible else '0dp'
        widget.size_hint_y = 1 if is_visible else 0

    # update config and update the displayed value
    def update_config_value(self, slider_id, slider_value):
        print(slider_id, slider_value)
        config.write(slider_id, slider_value)
        self.ids[f'{slider_id}_value'].text = f'{slider_value:.3f}'

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
                size_hint_y=None
            )
            btn.value = track_id
            btn.bind(on_press=dequeue)
            track_queue_layout.add_widget(btn)

    def update_audio_viewer(self, energy_original, energy_modified):
        self.energy_original_texture.blit_buffer(bytes(energy_original), colorfmt='rgb', bufferfmt='ubyte')
        self.energy_modified_texture.blit_buffer(bytes(energy_modified), colorfmt='rgb', bufferfmt='ubyte')

class MainApp(App):
    def build(self):
        print("hello from build")
        sm = ScreenManager()
        self.touchscreen = LightdreamTouchScreen()
        sm.add_widget(self.touchscreen, name='lightdream')
        self.debug_menu = DebugMenuScreen()
        sm.add_widget(self.debug_menu, name='debug_menu')
        if 'layout_test' in CURRENTLY_ENABLED_SCREENS:
            sm.add_widget(LayoutTestScreen(), name='layout_test')
        return sm

    def stupid_updated_queue_callback(self, now_playing, queue):
        if self.debug_menu:
            self.debug_menu.update_track_queue(now_playing, queue)

    def update_audio_viewer(self, energy_original, energy_modified):

        if self.debug_menu and config.read("MODE") == "autoplay":
            self.debug_menu.update_audio_viewer(energy_original, energy_modified)

    def add_touchscreen_api(self, api):
        global touchscreen_api
        touchscreen_api = api
        # print("on the right track?", self.debug_menu)

    def update_frame(self, frame):
        # TODO probably don't need to call both of these
        if self.touchscreen:
            self.touchscreen.led_output_texture.blit_buffer(bytes(frame), colorfmt='rgb', bufferfmt='ubyte')
            with self.touchscreen.canvas:
                self.touchscreen.canvas.ask_update()
        if self.debug_menu:
            self.debug_menu.led_output_texture.blit_buffer(bytes(frame), colorfmt='rgb', bufferfmt='ubyte')
            with self.debug_menu.canvas:
                self.debug_menu.canvas.ask_update()
if __name__ == '__main__':
    MainApp().run()

from kivy.app import App

from kivy.config import Config
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, ObjectProperty
from kivy.clock import Clock

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

FULLSCREEN_MODE = config.read("FULLSCREEN_MODE")

if FULLSCREEN_MODE:
    Config.set('graphics', 'borderless', 1)
    Config.set('graphics', 'top', 0)
    Config.set('graphics', 'left', 0)
    Config.set('graphics', 'width', 1920)
    Config.set('graphics', 'height', 1080)
    pass

# this needs to be imported after configuration
from kivy.core.window import Window

input_mapper = InputCoordinateMapper(LAYOUT_IMAGE_WIDTH, LAYOUT_IMAGE_HEIGHT)

CURRENTLY_ENABLED_SCREENS = [
    'lightdream',
    'debug_menu',
    # 'layout_test',
]

def get_next_screen(this_screen):
    screens = CURRENTLY_ENABLED_SCREENS
    return screens[screens.index(this_screen) + 1 - len(screens)]

touchscreen_api = {}

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

        self.spotlight_image.source = SPOTLIGHT.active_path
        self.spotlight_image.pos = (
            SPOTLIGHT.center[0] - SPOTLIGHT.radius,
            SPOTLIGHT.center[1] - SPOTLIGHT.radius
        )
        self.spotlight_mask.pos = (-500, -500)

        if config.read("LED_VIEWER") == True:
            print("creating led output texture.")
            self.led_output_texture = Texture.create(size=(170, 30))
            with self.canvas:
                Rectangle(
                    size=(340,60),
                    pos=(0,1020),
                    texture=self.led_output_texture)

    @property
    def spotlight_image(self):
        return self.canvas.after.get_group('spotlight-image')[0]

    @property
    def spotlight_mask(self):
        return self.canvas.after.get_group('spotlight-mask')[0]

    def activate_circle(self, circle, touch):
        if circle == 'SPOTLIGHT':
            # show the spotlight (positioned from bottom left)
            self.spotlight_mask.pos = (touch.x - 50, touch.y - 50)
        else:
            # set the image path to the brighter, 'active' image
            self.ids[circle].source = self.CIRCLES[circle].active_path

    def deactivate_circle(self, circle, touch):
        if circle == 'SPOTLIGHT':
            # hide the spotlight by dumping it offscreen
            self.spotlight_mask.pos = (-500, -500)
        else:
            # set the image path to the dim / regular image
            self.ids[circle].source = self.CIRCLES[circle].path

    def update_active(self, touch):
        # loop through all circles, check active, and update display
        for circle in self.CIRCLES.keys():
            circle_config = self.CIRCLES[circle]
            if input_mapper.is_active(circle_config.key):
                self.activate_circle(circle, touch)
            else:
                self.deactivate_circle(circle, touch)

    def on_touch_down(self, touch):
        super().on_touch_down(touch)
        self.update_active(touch)
        return

    def on_touch_move(self, touch):
        super().on_touch_move(touch)
        self.update_active(touch)
        return

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        self.update_active(touch)
        return



def enqueue(evt):
    touchscreen_api['playlist'].enqueue(evt.value)

def dequeue(evt):
    touchscreen_api['playlist'].dequeue(evt.value)

def skip_track(evt):
    touchscreen_api['skip_track']()


class DebugMenuScreen(Screen):
    energy_orig_list = ListProperty([0,0,0,0,0,0,0,0,0,0])
    energy_mod_list = ListProperty([0,0,0,0,0,0,0,0,0,0])
    led_output_texture = ObjectProperty()
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
            'brain_position',
            'brightness'
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
        if slider_id == 'decay_constant':
            self.ids[f'{slider_id}_value'].text = f'{slider_value:.3f}'
        elif slider_id == 'aural_effect_strength_multiplier' or slider_id == "brightness":
            self.ids[f'{slider_id}_value'].text = f'{slider_value:.2f}'
        else:
            self.ids[f'{slider_id}_value'].text = f'{slider_value:.0f}'

    def update_track_queue(self, now_playing, queue):
        if now_playing == None:
            return

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
        max_energy = config.read("max_energy")
        self.energy_orig_list = list(map(lambda x: x / max_energy, energy_original))[:10]
        self.energy_mod_list = list(map(lambda x: x / max_energy, energy_modified))[:10]

class MainApp(App):
    def __init__(self, fps):
        super().__init__()
        self.fps = fps
        self.sm = None
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)        

    def build(self):
        sm = ScreenManager()
        self.touchscreen = LightdreamTouchScreen()
        sm.add_widget(self.touchscreen, name='lightdream')
        self.debug_menu = DebugMenuScreen()
        sm.add_widget(self.debug_menu, name='debug_menu')
        if 'layout_test' in CURRENTLY_ENABLED_SCREENS:
            sm.add_widget(LayoutTestScreen(), name='layout_test')

        Clock.schedule_interval(self.update_data_from_main_thread, 1/self.fps)
        self.sm = sm
        return sm

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     print('The key', keycode, 'have been pressed')
    #     print(' - text is %r' % text)
    #     print(' - modifiers are %r' % modifiers)

        try:
            if keycode[0] == 49:
                if config.read("MODE") == "playlist":
                    return touchscreen_api['skip_track']()
                return touchscreen_api['set_mode']("playlist")
            elif keycode[0] == 50:
                touchscreen_api['set_mode']("autoplay")
            elif keycode[0] == 51:
                touchscreen_api['set_mode']("metronome")
        except:
            print("ERROR: some error with _on_keyboard_down that we're ignoring")
        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def update_playlist_status(self, playlist):
        if playlist.dirty:
            self.debug_menu.update_track_queue(playlist.now_playing, playlist.queue)
            playlist.dirty = False

    def update_audio_viewer(self, energy_original, energy_modified):
        pass
        if config.read("MODE") == "autoplay":
            self.debug_menu.update_audio_viewer(energy_original, energy_modified)

    def add_touchscreen_api(self, api):
        global touchscreen_api
        touchscreen_api = api

    def update_frame(self, frame):
        if self.touchscreen and self.sm.current == "lightdream":
            self.touchscreen.led_output_texture.blit_buffer(bytes(frame), colorfmt='rgb', bufferfmt='ubyte')
            with self.touchscreen.canvas:
                self.touchscreen.canvas.ask_update()
        if self.debug_menu and self.sm.current == "debug_menu":
            self.debug_menu.led_output_texture.blit_buffer(bytes(frame), colorfmt='rgb', bufferfmt='ubyte')
            with self.debug_menu.canvas:
                self.debug_menu.canvas.ask_update()

    def update_data_from_main_thread(self, dt):
        global touchscreen_api
        try:
            with touchscreen_api['frame_condition']:
                if config.read("LED_VIEWER"):
                    self.update_frame(touchscreen_api['get_frame']())

                if (self.sm.current == "debug_menu"):
                    with touchscreen_api['audio_condition']:
                        al = touchscreen_api['audio_listener']
                        self.update_audio_viewer(
                            al.energy_original,
                            al.energy_modified,
                        )

                    self.update_playlist_status(
                        touchscreen_api['playlist']
                    )
        except AttributeError:
            print("missing attribute when reloading data.")
            pass


if __name__ == '__main__':
    MainApp().run()

# pyright: ignore
# pylint: disable=all
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from src.widgets.icon_button import IconButton # type: ignore
from src.widgets.circle_image import CircleImage # type: ignore
from src.widgets.midground_float import MidGroundFloat # type: ignore
from src.widgets.background_video import BackgroundVideo # type: ignore
from kivy.properties import NumericProperty # type: ignore
from kivy.app import App
from src.widgets.create_player_form import CreatePlayerForm # type: ignore
Builder.load_file("src/kv/screens/setup.kv") # type: ignore


class SetupScreen(Screen):
    custom_padding = NumericProperty(80) # type: ignore
    def on_enter(self): # type: ignore
        # fetch necessary data
        print("Home loaded")

    def do_something(self):
        print("Button pressed")
    
    def on_kv_post(self, base_widget): # type: ignore
        self.ids.form.bind(on_form_submit=self.handle_submit) # type: ignore
    
    def handle_submit(self,form, data): # type: ignore
        print("handle_submit")
        app=App.get_running_app() # type: ignore

        app.status_controller.create_player(data.get("name")) # type: ignore
        app.on_pre_enter() # type: ignore
        self.manager.current = "home" # type: ignore


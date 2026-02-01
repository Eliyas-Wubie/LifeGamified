from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from src.widgets.icon_button import IconButton # type: ignore
from src.widgets.circle_image import CircleImage # type: ignore
from src.widgets.midground_float import MidGroundFloat # type: ignore
from src.widgets.background_box import BackgroundBox # type: ignore

Builder.load_file("src/kv/screens/test.kv") # type: ignore

class TestScreen(Screen):
    def on_enter(self): # type: ignore
        # fetch necessary data
        print("Home loaded")

    def do_something(self):
        print("Button pressed")
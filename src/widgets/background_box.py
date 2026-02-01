from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty # type: ignore
from kivy.lang import Builder

Builder.load_file("src/kv/widgets/background_box.kv") # type: ignore

class BackgroundBox(BoxLayout):
    bg_image = StringProperty("src/assets/bg.jpg") # type: ignore
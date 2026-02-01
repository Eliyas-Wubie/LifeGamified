from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty  # type: ignore

Builder.load_file("src/kv/widgets/icon_button.kv") # type: ignore

class IconButton(Button):
    image_path = StringProperty("src/myicon.png") # type: ignore
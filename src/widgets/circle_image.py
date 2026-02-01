from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.properties import StringProperty # type: ignore
Builder.load_file("src/kv/widgets/circle_image.kv") # type: ignore

class CircleImage(Widget):
    image_path= StringProperty("src/assets/bg.jpg") # type: ignore
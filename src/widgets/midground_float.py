from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder
from src.widgets.content_area import ContentArea # type: ignore
from src.widgets.nav import Nav  # type: ignore
from src.widgets.floating_buttons import FloatingButtons # type: ignore

from kivy.properties import NumericProperty # type: ignore

Builder.load_file("src/kv/widgets/midground_float.kv") # type: ignore
class MidGroundFloat(FloatLayout):
    offset=NumericProperty(0) # type: ignore
    def test(self):
        print("test")


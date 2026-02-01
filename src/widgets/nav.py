from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty # type: ignore

Builder.load_file("src/kv/widgets/nav.kv") # type: ignore
class Nav(BoxLayout):
    # offset=NumericProperty(0) # type: ignore
    def test(self):
        print("test")
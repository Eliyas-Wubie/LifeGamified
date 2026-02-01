from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

Builder.load_file("src/kv/widgets/floating_buttons.kv") # type: ignore
class FloatingButtons(BoxLayout):
    def test(self):
        print("test")
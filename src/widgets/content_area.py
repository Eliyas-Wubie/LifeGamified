from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty, StringProperty # type: ignore

Builder.load_file("src/kv/widgets/content_area.kv") # type: ignore
class ContentArea(BoxLayout):
    offset=NumericProperty(0) # type: ignore
    control_display = StringProperty("") # type: ignore

    def set_control_display(self, display): # type: ignore
        self.control_display = display # type: ignore
    def test(self):
        print("test")
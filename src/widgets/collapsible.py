from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import BooleanProperty

Builder.load_file("src/kv/widgets/collapsible.kv")

class Collapsible(BoxLayout):
    # control and target
    expanded = BooleanProperty(False)
    
    def on_expanded(self, *args):
        print("This is bull shit")
    
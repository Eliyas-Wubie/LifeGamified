from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, NumericProperty  # type: ignore
from kivy.core.window import Window # type: ignore

Builder.load_file("src/kv/widgets/icon_button.kv") # type: ignore

class IconButton(Button):
    image_path = StringProperty("src/myicon.png") # type: ignore
    hover = BooleanProperty(False) # type: ignore
    hover_enabled = BooleanProperty(True) # type: ignore
    
    base_width= NumericProperty(40)  # type: ignore
    base_height= NumericProperty(40) # type: ignore

    def __init__(self, **kwargs): # type: ignore
        super().__init__(**kwargs) # type: ignore
        Window.bind(mouse_pos=self.on_mouse_pos) # type: ignore
    
    def on_mouse_pos(self, window, pos): # type: ignore
        is_hovering = self.collide_point(*pos) # type: ignore
        if self.hover != is_hovering: # type: ignore
            self.hover = is_hovering # type: ignore
            self.width = self.base_width + (10 if self.hover and self.hover_enabled else 0) # type: ignore
            self.height = self.base_height + (10 if self.hover and self.hover_enabled else 0) # type: ignore

    
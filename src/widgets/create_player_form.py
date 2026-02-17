from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import StringProperty # type: ignore

Builder.load_file("src/kv/widgets/create_player_form.kv") # type: ignore
class CreatePlayerForm(BoxLayout):
    __events__ = ("on_form_submit",)
    
    def submit_form(self):
        data ={ # type: ignore
            "name": self.ids.name.text # type: ignore
        }
        self.dispatch("on_form_submit", data) # type: ignore
    def on_form_submit(self, data): # type: ignore
        pass


        
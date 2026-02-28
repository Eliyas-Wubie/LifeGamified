from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty # type: ignore
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.app import App
from src.widgets.profession_list import ProfessionList


Builder.load_file("src/kv/widgets/professions_content_area.kv") # type: ignore

class ProfessionsContentArea(BoxLayout):
    offset=NumericProperty(0) # type: ignore
    control_display = StringProperty("") # type: ignore
    content= ListProperty([]) # type: ignore
    visible= BooleanProperty(False)
    professions = ListProperty([])

    def on_visible(self, *_):
        Clock.schedule_once(self._load_data)
    def _load_data(self, *_):
        app = App.get_running_app()
        self.professions = app.daily_report_controller.get_professions() 
        
    def test(self):
        print("test")
    def on_content(self,): # type: ignore
        pass

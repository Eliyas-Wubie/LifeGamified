from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty # type: ignore
from kivy.app import App
from typing import TYPE_CHECKING
from datetime import datetime
if TYPE_CHECKING:
    from src.app import MyApp

Builder.load_file("src/kv/widgets/nav.kv") # type: ignore
class Nav(BoxLayout):
    # offset=NumericProperty(0) # type: ignore
    def set_control(self, data): # type: ignore
        app: MyApp = App.get_running_app() # type: ignore
        local_list=app.report_controller.get_reports()
        # local_list=[{"date":datetime.now()}]
        
        self.control(data, local_list) # type: ignore
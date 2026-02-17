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

    # def on_parent(self, widget, parent):
    #     if parent:
    #         # schedule binding after widget is fully initialized
    #         Clock.schedule_once(self.bind_scroll, 0)

    # def bind_scroll(self, dt):
    #     # bind once
    #     Window.bind(on_scroll=self.on_scroll)

    # def on_scroll(self, window, x, y, scroll_x, scroll_y):
    #     scatter = self.ids.scatter
    #     factor = 1.1 if scroll_y > 0 else 0.9
    #     scatter.scale *= factor
    #     scatter.scale = max(0.5, min(scatter.scale, 3))
    #     print(f"Scrolled: {scroll_y}, new scale: {scatter.scale}")

    # def _set_visible(self):
    #     print("is the setter called 🌟🌟🌟🌟🌟🌟🌟")
    #     Clock.schedule_once(lambda dt: setattr(self, "visible", True), 0)


    # def on_scroll(self, window, x, y, scroll_x, scroll_y):
    #     print("binding scroll 🚩🚩🚩🚩🚩")
    #     scatter = self.ids.scatter  # your scatter id
    #     factor = 1.1 if scroll_y > 0 else 0.9
    #     scatter.scale *= factor
    #     # Optional: keep it within min/max
    #     scatter.scale = max(0.5, min(scatter.scale, 3))
    # def on_visible(self, *_): # type: ignore
    #     print("binding scroll 🚧🖐")
        

    #     Window.bind(on_scroll=self.on_scroll)

    def on_visible(self, *_):
        print("____________about tao call clock")
        Clock.schedule_once(self._load_data)
    def _load_data(self, *_):
        app = App.get_running_app()
        self.professions = app.daily_report_controller.get_professions() 
        print("___________________ _load_data professions 🐱‍🐉🐱‍🐉🐱‍🐉", self.professions)
        
    def test(self):
        print("test")
    def on_content(self,): # type: ignore
        pass

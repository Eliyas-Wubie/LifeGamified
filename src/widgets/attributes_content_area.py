from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty, StringProperty, ListProperty, BooleanProperty # type: ignore
from kivy.app import App
from kivy.clock import Clock

Builder.load_file("src/kv/widgets/attributes_content_area.kv") # type: ignore
class AttributesContentArea(BoxLayout):
    offset=NumericProperty(0) # type: ignore
    control_display = StringProperty("") # type: ignore
    attributes = ListProperty([]) # type: ignore
    visible_attributes = ListProperty([]) # type: ignore
    visible=BooleanProperty(False)


    def set_control_display(self, display): # type: ignore
        self.control_display = display # type: ignore
    def test(self):
        print("test")
    def on_visible(self, *_):
        print("____________about tao call clock")
        Clock.schedule_once(self._load_data)
    def _load_data(self, *_):
        app = App.get_running_app()
        self.attributes = app.daily_report_controller.get_attributes() 
        print("___________________ _load_data 🐱‍🐉🐱‍🐉🐱‍🐉", self.attributes)
    def switch_to_selector(self):
        print("hey")
        self.ids.sm.current = "selector"
    def switch_to_detail(self, area):
        # filter the attributes by the part only. rename part (mind, spirit, body)
        self.visible_attributes=[]
        print("switched to detail")
        for item in self.attributes:
            print("working with attribute", item.name, area)
            if item.area == area:
                self.visible_attributes.append(item)
        self.ids.sm.current = "detail"
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty, ObjectProperty # type: ignore
from src.widgets.report_form import ReportForm # type: ignore
from src.widgets.mission_center import MissionCenter 
from src.widgets.compound_activity_center import CompoundActivityCenter
from kivy.app import App


Builder.load_file("src/kv/widgets/stats_content_area.kv") # type: ignore
class StatsContentArea(BoxLayout):
    offset=NumericProperty(0) # type: ignore
    control_display = StringProperty("") # type: ignore
    is_desktop = BooleanProperty(True) # type: ignore
    create_form = BooleanProperty(True) # type: ignore
    report_widget = ReportForm() # type: ignore
    mission_center = MissionCenter() 
    compound_activity_center = CompoundActivityCenter()

    def on_size(self, *_):
        self.is_desktop = self.width > 800 # type: ignore
        print(self.is_desktop) # type: ignore
    def set_control_display(self, display): # type: ignore
        print("changing control 🌟🙌", display) # type: ignore
        self.control_display = display # type: ignore
        if display=="report":
            self.report_widget.visible = True
            print("mounting report 🎶🎶🎶")
            self.ids.report.add_widget(self.report_widget)
            print("🤳🤳🤳🤳🤳", self.ids.report.children)
            
        elif display=="mission":
            self.mission_center.visible = True
            self.ids.mission.add_widget(self.mission_center)
        elif display=="compound_activity":
            self.compound_activity_center.visible = True
            self.ids.compound_activity.add_widget(self.compound_activity_center)
        else:
            print("removing current display ----")
            if self.report_widget in self.ids.report.children:
                print("removing report")
                self.ids.report.remove_widget(self.report_widget)
            elif self.mission_center in self.ids.mission.children:
                print("removing mission")
                self.ids.mission.remove_widget(self.mission_center)
            elif self.compound_activity_center in self.ids.compound_activity.children:
                print("removing compound activity")
                self.ids.compound_activity.remove_widget(self.compound_activity_center)
    def test(self):
        print("test")
    def on_is_desktop(self, *args): # type: ignore
        self.ids.controls_sm.current = "desktop" if self.is_desktop else "mobile" # type: ignore
    def on_kv_post(self, base_widget): # type: ignore
        self.report_widget.bind(on_form_submit=self.handle_report_submit) # type: ignore
        self.mission_center.bind(on_mission_form_submit=self.handle_mission_submit) # type: ignore
        self.compound_activity_center.bind(on_compound_activity_form_submit=self.handle_compound_activity_submit) # type: ignore
        
        
    def handle_report_submit(self,form, data): # type: ignore
        print("handle_report_submit")
        app=App.get_running_app() # type: ignore
        app.daily_report_controller.make_a_report(data) # type: ignore
    def handle_mission_submit(self,form, data): # type: ignore
        print("handle_mission_submit")
        app=App.get_running_app() # type: ignore
        app.daily_report_controller.create_mission(data) # type: ignore
    def handle_compound_activity_submit(self,form, data): # type: ignore
        print("handle_mission_submit")
        app=App.get_running_app() # type: ignore
        app.daily_report_controller.create_compound_activity(data) # type: ignore
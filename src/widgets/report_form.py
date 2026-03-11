from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty # type: ignore
from src.widgets.collapsible import Collapsible # type: ignore
from src.widgets.list import ListWidget # type: ignore
from kivy.app import App
from kivy.clock import Clock

Builder.load_file("src/kv/widgets/report_form.kv") # type: ignore
class ReportForm(BoxLayout):
    __events__ = ("on_form_submit",)
    visible=BooleanProperty(False) # type: ignore

    # mission_container = ObjectProperty(None) # type: ignore
    # daily_activity_container = ObjectProperty(None) # type: ignore
    # uncomfortable_activity_container = ObjectProperty(None) # type: ignore
    # generic_activity_container = ObjectProperty(None) # type: ignore
    # accomplishment_container = ObjectProperty(None) # type: ignore
    
    completed_missions=ListProperty([]) # type: ignore
    done_daily_activities=ListProperty([]) # type: ignore
    done_uncomfortable_activities=ListProperty([]) # type: ignore
    done_generic_activities=ListProperty([]) # type: ignore
    todays_accomplishments=ListProperty([]) # type: ignore
    
    missions=ListProperty([]) # type: ignore
    daily_activities=ListProperty([]) # type: ignore
    uncomfortable_activities=ListProperty([]) # type: ignore
    generic_activities=ListProperty([]) # type: ignore
    accomplishments=ListProperty([]) # type: ignore
    
    def on_completed_missions(self, *_):
        print("mission apdated", self.completed_missions)

    def mission_control(self, action, item):
        if action == "add":
            self.completed_missions.append(item)
        elif action == "remove":
            self.completed_missions.remove(item)

    def daily_activities_control(self, action, item):
        if action == "add":
            self.done_daily_activities.append(item)
        elif action == "remove":
            self.done_daily_activities.remove(item)

    def uncomfortable_activities_control(self, action, item):
        if action == "add":
            self.done_uncomfortable_activities.append(item)
        elif action == "remove":
            self.done_uncomfortable_activities.remove(item)

    def generic_activities_control(self, action, item):
        if action == "add":
            self.done_generic_activities.append(item)
        elif action == "remove":
            self.done_generic_activities.remove(item)

    def accomplishments_control(self, action, item):
        if action == "add":
            self.todays_accomplishments.append(item)
        elif action == "remove":
            self.todays_accomplishments.remove(item)

    def on_visible(self, *_):
        Clock.schedule_once(self._load_data)
    def _load_data(self, *_):
        app = App.get_running_app()
        self.missions = app.mission_controller.get_missions()
        self.daily_activities = app.activity_controller.get_daily_activities()
        self.uncomfortable_activities = app.activity_controller.get_uncomfortable_activities()
        self.generic_activities = app.activity_controller.get_generic_activities()
        self.accomplishments = app.accomplishment_controller.get_accomplishments()

    
    def submit_form(self):
        data ={ # type: ignore
            "completed_missions": self.completed_missions,
            "done_daily_activities":self.done_daily_activities,
            "done_uncomfortable_activities":self.done_uncomfortable_activities,
            "done_generic_activities":self.done_generic_activities,
            "todays_accomplishments":self.todays_accomplishments
        }
        self.dispatch("on_form_submit", data) # type: ignore

    # def on_missions(self, instance, value): # type: ignore
    #     container = self.mission_container # type: ignore
    #     for item in self.missions: # type: ignore
    #         container.add_widget(Label(text=str(item.get("date")))) # type: ignore
    # def on_daily_activities(self, instance, value): # type: ignore
    #     container = self.daily_activity_container # type: ignore
    #     for item in self.daily_activities: # type: ignore
    #         container.add_widget(Label(text=str(item.get("date")))) # type: ignore
    # def on_uncomfortable_activities(self, instance, value): # type: ignore
    #     container = self.uncomfortable_activity_container # type: ignore
    #     for item in self.uncomfortable_activities: # type: ignore
    #         container.add_widget(Label(text=str(item.get("date")))) # type: ignore
    # def on_generic_activities(self, instance, value): # type: ignore
    #     container = self.generic_activity_container # type: ignore
    #     for item in self.generic_activities: # type: ignore
    #         container.add_widget(Label(text=str(item.get("date")))) # type: ignore
    # def on_accomplishments(self, instance, value): # type: ignore
    #     container = self.accomplishment_container # type: ignore
    #     for item in self.accomplishments: # type: ignore
    #         container.add_widget(Label(text=str(item.get("date")))) # type: ignore


    def on_form_submit(self, data): # type: ignore
        pass


        

from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty # type: ignore
from src.widgets.collapsible import Collapsible # type: ignore
from src.widgets.list import ListWidget # type: ignore
from src.widgets.scrollable_list import ScrollableList # type: ignore
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock

Builder.load_file("src/kv/widgets/mission_center.kv") # type: ignore
class MissionCenter(BoxLayout):
    __events__ = ("on_mission_form_submit",)
    visible=BooleanProperty(False) # type: ignore
    add_form=BooleanProperty(False) # type: ignore
    missions=ListProperty([]) # type: ignore
    def on_add_form(self, *_):
        print("switching form ", self.add_form)
        self.ids.sm.current = "form" if self.add_form else "list"
    def search(self, search_string):
        print("searching", search_string)
        if search_string == "":
            self.ids.list.items = self.missions
            return
        new_mission=[]
        for mission in self.missions:
            print(mission.name, mission.description)
            if search_string in mission.name or (mission.description and search_string in mission.description):
                new_mission.append(mission)
        self.ids.list.items = new_mission
    def delete(self, item):
        app = App.get_running_app()
        print("___________________ deleting")
        app.daily_report_controller.delete_mission(item) 
        new_mission=[]
        for mission in self.missions:
            if mission.name != item.name:
                new_mission.append(mission)
        self.ids.list.items = new_mission
        self.missions = new_mission
    def on_missions(self, *_):
        print("mission updated", self.missions)
    def mission_control(self, action, item):
        if action == "add":
            self.completed_missions.append(item)
        elif action == "remove":
            self.completed_missions.remove(item)
    def on_visible(self, *_):
        print("____________about tao call clock")
        Clock.schedule_once(self._load_data)
    def _load_data(self, *_):
        app = App.get_running_app()
        print("___________________ _load_data")
        self.missions = app.daily_report_controller.get_missions() 
    
    
    # may not be used   
    def submit(self):
        name = self.ids.name.text
        description = self.ids.description.text
        difficulty = self.ids.difficulty.value
        year= self.ids.year.text
        month= self.ids.month.text
        day= self.ids.day.text
        deadline= None
        if year == "Year" and month == "Month" and day=="Day": 
            pass
        else:
            if year == "Year":
                year=datetime.now().year
            if month == "Month":
                month=datetime.now().month
            if day == "Day":
                day=datetime.now().day
            date_str = f"{year}-{month}-{day}"
            print(date_str)
            deadline = datetime.strptime(date_str, "%Y-%m-%d")
        data = {
            "name":name,
            "description": description,
            "difficulty": difficulty,
            "deadline": deadline
        }
        print("submit called", data)
        self.dispatch("on_mission_form_submit", data) # type: ignore

 

    def on_mission_form_submit(self, data): # type: ignore
        pass


        
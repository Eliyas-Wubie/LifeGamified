from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty, NumericProperty # type: ignore
from src.widgets.collapsible import Collapsible # type: ignore
from src.widgets.list import ListWidget # type: ignore
from src.widgets.scrollable_list import ScrollableList # type: ignore

from kivy.app import App
from kivy.clock import Clock

Builder.load_file("src/kv/widgets/compound_activity_center.kv") # type: ignore
class CompoundActivityCenter(BoxLayout):
    __events__ = ("on_compound_activity_form_submit",)
    visible=BooleanProperty(False) # type: ignore
    add_form=BooleanProperty(False) # type: ignore
    compound_activities=ListProperty([]) # type: ignore
    form_name = StringProperty(None)
    form_xp = NumericProperty(None)
    
    def on_add_form(self, *_):
        self.ids.sm.current = "form" if self.add_form else "list"
    def search(self, search_string):
        if search_string == "":
            self.ids.list.items = self.compound_activities
            return
        new_compound_activities=[]
        for compound_activities in self.compound_activities:
            if search_string in compound_activities.name:
                new_compound_activities.append(compound_activities)
        self.ids.list.items = new_compound_activities
    def delete(self, item):
        app = App.get_running_app()
        app.activity_controller.delete_compound_activity(item) 
        new_compound_activities=[]
        for compound_activity in self.compound_activities:
            if compound_activity.name != item.name:
                new_compound_activities.append(compound_activity)
        self.ids.list.items = new_compound_activities
        self.compound_activities = new_compound_activities
    def on_compound_activities(self, *_):
        print("mission updated", self.compound_activities)
    def mission_control(self, action, item):
        if action == "add":
            self.completed_compound_activities.append(item)
        elif action == "remove":
            self.completed_compound_activities.remove(item)
    def on_visible(self, *_):
        Clock.schedule_once(self._load_data)
    def _load_data(self, *_):
        app = App.get_running_app()
        self.compound_activities = app.activity_controller.get_compound_activities() 
    
    
    # may not be used   
    def submit(self):
        data ={ # type: ignore
            "name": self.form_name,
            "xp":self.form_xp,
        }
        self.dispatch("on_compound_activity_form_submit", data) # type: ignore
    def on_compound_activity_form_submit(self, data): # type: ignore
        pass


        

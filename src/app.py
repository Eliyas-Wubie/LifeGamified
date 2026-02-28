import os
os.environ["KIVY_VIDEO"] = "ffpyplayer"
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window # type: ignore
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty # type: ignore
from src.controllers import report
from src.controllers import status
from src.controllers import daily_report
from kivy.uix.screenmanager import NoTransition 

# import screens so Kivy knows the classes
from src.screens.home import HomeScreen
from src.screens.setup import SetupScreen
# from src.screens.test import TestScreen
Window.maximize() # type: ignore
Window.clearcolor = (0, 0, 0, 1)
Window.minimum_width = 300  
Window.minimum_height = 300
class MyApp(App):
    # Global state defined here and can be accessed anywhere
    name = StringProperty("eliyas") # type: ignore
    xp = NumericProperty(0) # type: ignore
    xp_rate = NumericProperty(10) # type: ignore
    level = NumericProperty(1) # type: ignore
    titles = ListProperty([]) # type: ignore
    detail = StringProperty("") # type: ignore
    report_controller = report
    status_controller = status
    daily_report_controller = daily_report
    profile =  ObjectProperty(None) # type: ignore
    def get_titles(self): # type: ignore
        res=""
        for item in self.titles: # type: ignore
            res=res+" "+item # type: ignore
        return res if res!="" else "[b][color=#555555ff]you have no titles[/color][/b]" # type: ignore
    def build(self):
        self.title = "Life Gamified"
        self.icon = "myicon.png"
        self.on_pre_enter()
        sm = ScreenManager()
        sm.transition = NoTransition()
        sm.add_widget(HomeScreen(name="home")) # type: ignore
        sm.add_widget(SetupScreen(name="setup")) # type: ignore
        profile = self.status_controller.get_profile()
        if profile:
            sm.current = "home"
        else:
            sm.current = "setup"
        
        return sm
    def on_pre_enter(self): # type: ignore
        # fetch necessary data
        self.profile = self.status_controller.get_profile()



if __name__ == "__main__":
    MyApp().run()
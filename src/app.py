from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window # type: ignore
from kivy.properties import StringProperty, NumericProperty # type: ignore

# import screens so Kivy knows the classes
from src.screens.home import HomeScreen
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
    titles = ["test", "test2", "test3"]
    detail = StringProperty("") # type: ignore
    def get_titles(self):
        res=""
        for item in self.titles:
            res=res+item+ " "
        return res
    def set_detail(self, data): # type: ignore
        print("hgafafaf")
        self.detail = data # type: ignore
    # Configurations cam also be made
    def build(self):
        self.title = "Life Gamified"
        self.icon = "myicon.png"
        
    
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="test")) # type: ignore
        return sm


if __name__ == "__main__":
    MyApp().run()
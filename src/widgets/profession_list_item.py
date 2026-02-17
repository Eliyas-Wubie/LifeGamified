from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.lang.builder import Builder


Builder.load_file("src/kv/widgets/profession_list_item.kv")
class ProfessionListItem(BoxLayout):
    title = StringProperty("")
    
    def on_title(self, *_):
        Title = Label(text=self.title)
        self.orientation = "vertical"
        self.add_widget(Title)
        Container=BoxLayout()
        self.add_widget(Container)
    
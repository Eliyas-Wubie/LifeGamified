from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.lang import Builder
from kivy.graphics import Color, RoundedRectangle # type: ignore
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty, ObjectProperty  # type: ignore

Builder.load_file("src/kv/widgets/list_item.kv") # type: ignore

class ListItem(BoxLayout):
    item=ObjectProperty(None)
    control_list = ObjectProperty(None)
    
    def on_item(self, *_):
        item_dict = self.item.__dict__
        print("hhhhhhhhhh")
        # iterate and display the keys and values
        cb = CheckBox(
            size_hint=(None, None),
            size=(30, 30),
            pos_hint={"center_y":0.5}
        )
        def on_checkbox_active(checkbox, value):
            print("Checked:", value)
            if value:
                self.control_list("add", self.item)
            else:
                self.control_list("remove", self.item)

        cb.bind(active=on_checkbox_active)
        self.add_widget(cb)
        for key, value in item_dict.items():
            if type(value) == list or key=="_id" or key=="_load":
                continue
            c=BoxLayout(orientation= "horizontal")
            c.add_widget(Label(text=f'{key[1:]} : {value}'))
            
            self.add_widget(c)
        
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from src.widgets.icon_button import IconButton
from kivy.lang import Builder
from kivy.graphics import Color, RoundedRectangle # type: ignore
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty, ObjectProperty  # type: ignore

Builder.load_file("src/kv/widgets/attr_list_item.kv") # type: ignore

class AttributeListItem(BoxLayout):
    item=ObjectProperty(None)
    control = ObjectProperty(None)
    include_button = BooleanProperty(True)
    def on_item(self, *_):
        item_dict = self.item.__dict__
        button = IconButton(image_path="src/assets/activity.png", size_hint=(None, None), base_width=20, base_height=20)
        def control(self):
            self.parent.control(self.parent.item)
        button.bind(on_press = control)
        
        # for key, value in item_dict.items():
        #     if type(value) == list or key=="_id" or key=="_load":
        #         continue
        print(item_dict)
        c=BoxLayout(orientation= "horizontal")
        c.add_widget(Label(text=f'{item_dict.get("_name")} : {item_dict.get("_current_value")}'))

        self.add_widget(c)
        print("i am going to include a button", self.include_button)
        if self.include_button:
            self.add_widget(button)
        
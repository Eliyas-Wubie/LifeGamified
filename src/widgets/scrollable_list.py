from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty, ObjectProperty  # type: ignore
from kivy.graphics import Color, RoundedRectangle
from src.widgets.mc_list_item import MCListItem
from src.widgets.report_list_item import ReportListItem
from src.widgets.attr_list_item import AttributeListItem
Builder.load_file("src/kv/widgets/scrollable_list.kv") # type: ignore

class ScrollableList(ScrollView):
    items: list=ListProperty([])
    control=ObjectProperty(None)
    container=ObjectProperty(None)
    include_button=BooleanProperty(True)
    def on_kv_post(self, *_):
        print("this is on kv post on list")
        # self.add_widget(self.container)
        # self.height = 300
        self.do_scroll_x = False
        self.do_scroll_y = True
    def on_include_button(self, *_):
        print("include button set to 🌟🌟🌟🌟", self.include_button)
        
    def on_items(self, *_):
        print("on items executing", self.items)
        if not self.container:
            self.container = BoxLayout(orientation="vertical", size_hint_y=None)        
            self.container.bind(minimum_height=self.container.setter("height"))
            self.add_widget(self.container)
            self.container.add_widget(Label(text="hahaha"))
        self.container.clear_widgets()
        for item in self.items:
            if self.item_widget == "report":
                i = ReportListItem()
            elif self.item_widget == "attr":
                i = AttributeListItem()
            else:
                i= MCListItem()
            i.size_hint_y = None
            i.height = 60  # or compute based on content
            i.include_button = self.include_button
            i.item = item
            i.control = self.control
            # i.padding = 30
    
            # i.control_list=self.control
            self.container.add_widget(i)
            self.container.add_widget(Widget(size_hint_y=None, height=10))
            
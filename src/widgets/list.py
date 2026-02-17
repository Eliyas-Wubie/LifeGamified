from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty, ObjectProperty  # type: ignore
from kivy.graphics import Color, RoundedRectangle
from src.widgets.list_item import ListItem
Builder.load_file("src/kv/widgets/list.kv") # type: ignore

class ListWidget(BoxLayout):
    items: list=ListProperty([])
    control: list=ObjectProperty(None)
    
    def on_kv_post(self, *_):
        print("this is on kv post on list")
    
    def on_items(self, *_):
        print("on items executing", self.items)
        for item in self.items:
            i=ListItem()
            i.size_hint_y = None
            i.height = 60  # or compute based on content
            # with i.canvas.before:
            #     Color(0.2, 0.6, 0.9, 1)  # RGBA (0–1)
            #     rect = RoundedRectangle(
            #         pos=i.pos,
            #         size=i.size,
            #         radius=[20]
            #     )
            # def update_rect(*args):
            #     rect.pos = i.pos
            #     rect.size = i.size
            # i.bind(pos=update_rect, size=update_rect)
            i.item = item
            i.control_list=self.control
            self.add_widget(i)


            # # bind AFTER adding to parent
            
            # update_rect()
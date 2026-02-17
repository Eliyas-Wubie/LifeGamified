from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, ListProperty
from src.widgets.profession_list_item import ProfessionListItem

class ProfessionList(BoxLayout):
    professions = ListProperty(None)
    visible = BooleanProperty(None)

    def recursive_push(self, children_list, item):
        for children in children_list:
            for i in range(len(children.children)):
                if isinstance(children.children[i], Label) and children.children[i].text == item.parent.name:
                    print("parent match")
                    item_widget = ProfessionListItem()
                    item_widget.title = item.name
                    for c in children.children:
                        if isinstance(c, BoxLayout):
                            c.add_widget(item_widget)
                    return
                elif isinstance(children.children[i], BoxLayout):
                    self.recursive_push(children.children[i].children, item)

    def on_professions(self, *_):
        print("💈💈🌟🌟💈💈", self.professions)
        for item in self.professions:
            if not item.parent:
                item_widget = ProfessionListItem()
                item_widget.title = item.name
                self.add_widget(item_widget)
            else:
                print("🚒🚒🚒🚒", self.children) # Perfect now make this recursive
                self.recursive_push(self.children, item)
                # for children in self.children:
                #     for i in range(len(children.children)):
                #         if isinstance(children.children[i], Label) and children.children[i].text == item.parent.name:
                #             print("parent match")
                #             item_widget = ProfessionListItem()
                #             item_widget.title = item.name
                #             for c in children.children:
                #                 if isinstance(c, BoxLayout):
                #                     c.add_widget(item_widget)
                #         else:
                #             print("nop no parent match")
        
    
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, BooleanProperty, ListProperty, ObjectProperty, NumericProperty # type: ignore
from src.widgets.collapsible import Collapsible # type: ignore
from src.widgets.list import ListWidget # type: ignore
from src.widgets.scrollable_list import ScrollableList # type: ignore
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock

Builder.load_file("src/kv/widgets/reports_content_area.kv") # type: ignore
class ReportsContentArea(BoxLayout):
    offset=NumericProperty(0) # type: ignore

    visible=BooleanProperty(False) # type: ignore
    add_form=BooleanProperty(False) # type: ignore
    daily_reports=ListProperty([]) # type: ignore
    detail_item=ObjectProperty(None)
    
    def search(self, time_frame,  search_string):
        print("searching", time_frame, search_string)
        if search_string == "":
            self.ids.list.items = self.daily_reports
            return
        new_daily_report=[]
    
        for daily_report in self.daily_reports:
            if time_frame =="year":
                print(str(daily_report.date.year) == search_string)
                if str(daily_report.date.year)  == search_string:
                    new_daily_report.append(daily_report)
            if time_frame =="month":
                if str(daily_report.date.month)  == search_string:
                    new_daily_report.append(daily_report)
            if time_frame =="day":
                if str(daily_report.date.day)  == search_string:
                    new_daily_report.append(daily_report)
            print("🐱‍🏍🐱‍🏍", daily_report.date)
        self.ids.list.items = new_daily_report
        
    def show_detail(self, data):
        self.ids.sm.current="detail"
        print(data)
        self.detail_item=data
    def back_to_list(self):
        self.ids.sm.current="list"
    def on_visible(self, *_):
        print("____________about tao call clock")
        Clock.schedule_once(self._load_data)
    def _load_data(self, *_):
        app = App.get_running_app()
        print("___________________ _load_data")
        self.daily_reports = app.daily_report_controller.get_daily_reports() 
    

        
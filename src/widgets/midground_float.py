from kivy.uix.floatlayout import FloatLayout
from kivy.lang.builder import Builder
from src.widgets.stats_content_area import StatsContentArea # type: ignore
from src.widgets.reports_content_area import ReportsContentArea # type: ignore
from src.widgets.attributes_content_area import AttributesContentArea # type: ignore
from src.widgets.professions_content_area import ProfessionsContentArea # type: ignore
from src.widgets.settings_content_area import SettingsContentArea

from src.widgets.nav import Nav  # type: ignore
from src.widgets.floating_buttons import FloatingButtons # type: ignore

from kivy.properties import NumericProperty, StringProperty, ListProperty  # type: ignore

Builder.load_file("src/kv/widgets/midground_float.kv") # type: ignore
class MidGroundFloat(FloatLayout):
    offset=NumericProperty(0) # type: ignore
    current_content=StringProperty("stats") # type: ignore
    local_list = ListProperty([]) # type: ignore
    def set_current_content(self, data, local_list): # type: ignore
        # self.current_content = data # type: ignore
        # self.local_list=local_list # type: ignore
        self.ids.sm.current = data


from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder # type: ignore
from kivy.properties import StringProperty, NumericProperty # type: ignore

Builder.load_file("src/kv/widgets/background_video.kv") # type: ignore
class BackgroundVideo(BoxLayout):
    video_path=StringProperty("src/assets/15076327_1920_1080_24fps.mp4") # type: ignore
    overlay_opacity=NumericProperty(0) # type: ignore
from manim import *

import datetime


class VideoCover(Scene):
    def __init__(self,
                 renderer=None,
                 camera_class=Camera,
                 always_update_mobjects=False,
                 random_seed=None,
                 skip_animations=False):
        super().__init__(
            renderer,
            camera_class,
            always_update_mobjects,
            random_seed,
            skip_animations)
        self.video_title: str = input("Please input the video title: ")
        self.author: str = "src_resources"
        self.date: str = datetime.datetime.now().strftime('%Y/%m/%d')

    def construct(self):
        print("Video title:", self.video_title)
        print("Author:", self.author)
        print("Date:", self.date)

        video_title_text = Text(self.video_title, color=YELLOW, font_size=50)
        author_text = Text(self.author, color=WHITE, font_size=20)
        date_text = Text(self.date, color=WHITE, font_size=20)
        author_text.next_to(video_title_text, DOWN)
        date_text.next_to(author_text, DOWN)

        self.play(Write(video_title_text, run_time=1))
        self.play(Write(author_text, run_time=1))
        self.play(Write(date_text, run_time=1))
        self.wait(1)

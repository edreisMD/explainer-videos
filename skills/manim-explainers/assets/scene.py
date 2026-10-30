"""Editable, silent illustrative queue explainer. Manim Community 0.19.0."""

import os
from manim import (
    Scene, Text, RoundedRectangle, Circle, VGroup, Arrow,
    FadeIn, FadeOut, Create, Transform, config,
    LEFT, RIGHT, UP, DOWN,
)

THEME = os.environ.get("EXPLAINER_THEME", "dark")
FORMAT = os.environ.get("EXPLAINER_FORMAT", "vertical")
PREVIEW = os.environ.get("EXPLAINER_PREVIEW") == "1"
if THEME not in ("dark", "light") or FORMAT not in ("vertical", "landscape"):
    raise ValueError("Choose dark/light theme and vertical/landscape format")

VERTICAL = FORMAT == "vertical"
config.pixel_width, config.pixel_height = ((360, 640) if VERTICAL else (640, 360)) if PREVIEW else ((1080, 1920) if VERTICAL else (1920, 1080))
config.frame_height = 14.22 if VERTICAL else 8
config.frame_width = 8 if VERTICAL else 14.22
config.frame_rate = 15 if PREVIEW else 30
config.background_color = "#111827" if THEME == "dark" else "#FAFAF7"
FG = "#F3F4F6" if THEME == "dark" else "#18212F"
MUTED = "#AEB9CC" if THEME == "dark" else "#536177"
BLUE, AMBER, GREEN = "#4798EE", "#E5A83D", "#30AD7A"


def fit_text(text, size=32, color=FG, width=6.5):
    label = Text(text, font="sans-serif", font_size=size, color=color, line_spacing=1.15)
    if label.width > width:
        label.scale_to_fit_width(width)
    return label


class ExplainerScene(Scene):
    def construct(self):
        top = config.frame_height / 2
        title = fit_text("What happens when\nthe worker is busy?", size=36)
        title.move_to(UP * (top - 1.65))
        note = fit_text("Illustrative example · no benchmark", size=17, color=MUTED)
        note.move_to(DOWN * (top - 0.6))

        queue_box = RoundedRectangle(width=3.0, height=1.65, corner_radius=.18, color=BLUE)
        worker_box = RoundedRectangle(width=1.55, height=1.65, corner_radius=.18, color=AMBER)
        queue_box.move_to(LEFT * 1.5)
        worker_box.move_to(RIGHT * 2.1)
        queue_label = fit_text("Queue", size=25).next_to(queue_box, UP, buff=.25)
        worker_label = fit_text("Worker", size=25).next_to(worker_box, UP, buff=.25)
        arrow = Arrow(queue_box.get_right(), worker_box.get_left(), buff=.12, color=MUTED)
        tokens = VGroup(*[
            Circle(radius=.23, color=BLUE, fill_color=BLUE, fill_opacity=1)
            for _ in range(3)
        ]).arrange(RIGHT, buff=.3).move_to(queue_box)
        first_task, next_task = tokens[0], tokens[1]
        diagram = VGroup(queue_box, worker_box, queue_label, worker_label, arrow, tokens)
        diagram.move_to(DOWN * .05)

        captions = fit_text("Tasks arrive before\nthe worker is ready.", size=29)
        captions.move_to(DOWN * (2.2 if VERTICAL else 2.5))
        self.play(FadeIn(title), FadeIn(note), run_time=.8)
        self.play(Create(queue_box), Create(worker_box), FadeIn(queue_label), FadeIn(worker_label), Create(arrow), run_time=1)
        self.play(FadeIn(tokens), FadeIn(captions), run_time=.7)
        self.wait(2)

        next_title = fit_text("The queue holds\nwhat comes next.", size=36).move_to(title)
        next_caption = fit_text("The next task starts\nwhen the worker is free.", size=29).move_to(captions)
        self.play(Transform(title, next_title), Transform(captions, next_caption), run_time=.7)
        self.play(first_task.animate.move_to(worker_box.get_center()).set_color(AMBER), run_time=1.4)
        self.wait(.8)
        self.play(first_task.animate.set_color(GREEN), worker_box.animate.set_color(GREEN), run_time=.6)
        self.wait(.8)
        final_title = fit_text("Separate intake\nfrom execution.", size=36).move_to(title)
        final_caption = fit_text("Accept the work now.\nProcess it when ready.", size=29).move_to(captions)
        self.play(Transform(title, final_title), Transform(captions, final_caption), FadeOut(first_task), run_time=.7)
        self.play(next_task.animate.move_to(worker_box.get_center()).set_color(AMBER), worker_box.animate.set_color(AMBER), run_time=1.2)
        self.wait(2)

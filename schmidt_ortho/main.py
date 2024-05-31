from manim import *

import numpy as np
import random


class SchmidtOrtho2D(Scene):
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
        self.vec_a_1 = np.array([random.randint(-3, 3), random.randint(-3, 3)], dtype=np.float32)
        self.vec_a_2 = np.array([random.randint(-3, 3), random.randint(-3, 3)], dtype=np.float32)

        print("Vector a1: ", self.vec_a_1)
        print("Vector a2: ", self.vec_a_2)

    def construct(self):
        number_plane = NumberPlane(
            x_length=8,
            y_length=8,
            x_range=(-5, 5),
            y_range=(-5, 5)
        )
        self.play(Create(number_plane, run_time=2))

        vec_a_1_arrow = Arrow(
            start=number_plane.coords_to_point(0, 0),
            end=number_plane.coords_to_point(self.vec_a_1[0], self.vec_a_1[1]),
            color=RED,
            buff=0
        )
        vec_a_2_arrow = Arrow(
            start=number_plane.coords_to_point(0, 0),
            end=number_plane.coords_to_point(self.vec_a_2[0], self.vec_a_2[1]),
            color=RED,
            buff=0
        )
        vec_a_1_tex = MathTex(r"\vec a_1 =", "({}, {})".format(self.vec_a_1[0], self.vec_a_1[1]), color=RED)
        vec_a_2_tex = MathTex(r"\vec a_2 =", "({}, {})".format(self.vec_a_2[0], self.vec_a_2[1]), color=RED)
        vec_a_1_tex.to_corner(UP + LEFT)
        vec_a_2_tex.next_to(vec_a_1_tex, DOWN)
        self.play(
            Create(vec_a_1_arrow, run_time=2),
            Create(vec_a_2_arrow, run_time=2),
            Write(vec_a_1_tex, run_time=2),
            Write(vec_a_2_tex, run_time=2)
        )
        self.wait(1)

        vec_b_1 = self.vec_a_1.copy()
        vec_b_1_arrow = vec_a_1_arrow.copy().set_color(YELLOW)
        vec_b_1_tex = MathTex(r"\vec b_1 = \vec a_1", color=YELLOW)
        vec_b_1_tex.next_to(vec_a_2_tex, DOWN)
        self.play(
            Create(vec_b_1_arrow, run_time=2),
            Write(vec_b_1_tex, run_time=2)
        )
        self.wait(1)

        vec_b_2_tex = MathTex(r"\vec b_2 = \vec a_2 - \frac{(\vec a_2, \vec b_1)}{(\vec b_1, \vec b_1)}\vec b_1", color=YELLOW)
        vec_b_2_tex.next_to(vec_b_1_tex, DOWN)
        vec_b_2_tex.align_on_border(LEFT)
        self.play(Write(vec_b_2_tex, run_time=2))

        vec_b_1_tmp = (np.vdot(self.vec_a_2, vec_b_1) / np.vdot(vec_b_1, vec_b_1)) * vec_b_1
        vec_b_1_tmp_arrow = Arrow(
            start=number_plane.coords_to_point(0, 0),
            end=number_plane.coords_to_point(vec_b_1_tmp[0], vec_b_1_tmp[1]),
            color=GREEN,
            buff=0
        )
        vec_b_1_tmp_tip = MathTex(r"\frac{(\vec a_2, \vec b_1)}{(\vec b_1, \vec b_1)}\vec b_1", color=GREEN)
        vec_b_1_tmp_tip.next_to(vec_b_1_tmp_arrow, RIGHT)
        self.play(
            Create(vec_b_1_tmp_arrow, run_time=2),
            Write(vec_b_1_tmp_tip, run_time=2)
        )

        vec_b_2 = self.vec_a_2 - vec_b_1_tmp
        vec_b_2_arrow_old = Arrow(
            start=number_plane.coords_to_point(vec_b_1_tmp[0], vec_b_1_tmp[1]),
            end=number_plane.coords_to_point(self.vec_a_2[0], self.vec_a_2[1]),
            color=YELLOW,
            buff=0
        )
        vec_b_2_arrow_tip = MathTex(r"\vec b_2", color=YELLOW)
        vec_b_2_arrow_tip.next_to(vec_b_2_arrow_old, RIGHT)
        self.play(
            Create(vec_b_2_arrow_old, run_time=2),
            Write(vec_b_2_arrow_tip, run_time=2)
        )
        self.wait(1)

        self.play(
            Uncreate(vec_b_1_tmp_arrow, run_time=2),
            Unwrite(vec_b_1_tmp_tip, run_time=2),
            Unwrite(vec_b_2_arrow_tip, run_time=2)
        )
        vec_b_2_arrow = Arrow(
            start=number_plane.coords_to_point(0, 0),
            end=number_plane.coords_to_point(vec_b_2[0], vec_b_2[1]),
            color = YELLOW,
            buff = 0
        )
        self.play(Transform(vec_b_2_arrow_old, vec_b_2_arrow, replace_mobject_with_target_in_scene=True, run_time=2))
        self.wait(1)

        vec_xi_1 = vec_b_1 / np.linalg.norm(vec_b_1)
        vec_xi_1_arrow = Arrow(
            start=number_plane.coords_to_point(0, 0),
            end=number_plane.coords_to_point(vec_xi_1[0], vec_xi_1[1]),
            color = BLUE,
            buff = 0
        )
        vec_xi_1_tex = MathTex(r"\vec \xi_1 = \frac{1}{||\vec b_1||}\vec b_1", color=BLUE)
        vec_xi_1_tex.next_to(vec_b_2_tex, DOWN)
        vec_b_1_arrow_copy = vec_b_1_arrow.copy()
        self.play(
            Transform(vec_b_1_arrow_copy, vec_xi_1_arrow, replace_mobject_with_target_in_scene=False, run_time=2),
            Write(vec_xi_1_tex, run_time=2)
        )
        vec_xi_1_arrow = vec_b_1_arrow_copy
        self.wait(1)

        vec_xi_2 = vec_b_2 / np.linalg.norm(vec_b_2)
        vec_xi_2_arrow = Arrow(
            start=number_plane.coords_to_point(0, 0),
            end=number_plane.coords_to_point(vec_xi_2[0], vec_xi_2[1]),
            color=BLUE,
            buff=0
        )
        vec_xi_2_tex = MathTex(r"\vec \xi_2 = \frac{1}{||\vec b_2||}\vec b_2", color=BLUE)
        vec_xi_2_tex.next_to(vec_xi_1_tex, DOWN)
        vec_b_2_arrow_copy = vec_b_2_arrow.copy()
        self.play(
            Transform(vec_b_2_arrow_copy, vec_xi_2_arrow, replace_mobject_with_target_in_scene=False, run_time=2),
            Write(vec_xi_2_tex, run_time=2)
        )
        vec_xi_2_arrow = vec_b_2_arrow_copy
        self.wait(1)

        vec_xi_2_tex.add_updater(lambda it: it.next_to(vec_xi_1_tex, DOWN))
        self.play(
            Uncreate(vec_a_1_arrow, run_time=2),
            Uncreate(vec_a_2_arrow, run_time=2),
            Uncreate(vec_b_1_arrow, run_time=2),
            Uncreate(vec_b_2_arrow, run_time=2),
            Unwrite(vec_a_1_tex, run_time=2),
            Unwrite(vec_a_2_tex, run_time=2),
            Unwrite(vec_b_1_tex, run_time=2),
            Unwrite(vec_b_2_tex, run_time=2),
            vec_xi_1_tex.animate(run_time=2).to_corner(LEFT + UP)
        )
        self.wait(4)

        self.play(
            FadeOut(number_plane, run_time=2),
            FadeOut(vec_xi_1_tex, run_time=2),
            FadeOut(vec_xi_2_tex, run_time=2),
            FadeOut(vec_xi_1_arrow, run_time=2),
            FadeOut(vec_xi_2_arrow, run_time=2)
        )

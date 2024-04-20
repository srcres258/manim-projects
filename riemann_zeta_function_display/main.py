from lib import *


def new_zeta_func_val_latex_str(x: complex, fv: complex) -> str:
    return r"\zeta(%.04f+%.04f\mathrm{i})=%.04f+%.04f\mathrm{i}" % (x.real, x.imag, fv.real, fv.imag)


class RiemannZetaFunctionDisplay(BaseScene):
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
        self.zeta_func_val_latex = None
        self.zeta_func_x = complex(0.5, 0)
        self.zeta_func_x_inc_rate = complex(0, 0.5)
        self.zeta_func_val = zeta(self.zeta_func_x)
        self.zeta_func_val_dot = None
        self.zeta_func_val_dot_path = None
        self.complex_plane = None
        self.zeta_func_val_latex = None

    def construct(self):
        super().construct()

        self.complex_plane = ComplexPlane(
            axis_config={
                "include_tip": False
            }
        ).add_coordinates()
        self.zeta_func_val_latex = self.__new_zeta_func_val_latex()
        self.play(Write(self.complex_plane, run_time=2))
        self.wait(1)

        self.zeta_func_val_dot = Dot(self.complex_plane.n2p(self.zeta_func_val), color=YELLOW)
        self.zeta_func_val_dot_path = VMobject(color=RED, stroke_width=4)
        self.zeta_func_val_dot_path.set_points_as_corners(
            [self.zeta_func_val_dot.get_center(), self.zeta_func_val_dot.get_center()])
        self.play(Write(self.zeta_func_val_latex, run_time=2),
                  Create(self.zeta_func_val_dot, run_time=2))
        self.add(self.zeta_func_val_dot_path)
        self.wait(1)

        def update_zeta_func_x_dot_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([self.zeta_func_val_dot.get_center()])
            path.become(previous_path)

        def update_zeta_func_x_dot(dot, dt: float):
            self.zeta_func_x += dt * self.zeta_func_x_inc_rate
            self.zeta_func_val = zeta(self.zeta_func_x)
            new_dot = Dot(self.complex_plane.n2p(self.zeta_func_val), color=YELLOW)
            dot.become(new_dot)

        self.zeta_func_val_dot_path.add_updater(update_zeta_func_x_dot_path)
        self.zeta_func_val_dot.add_updater(update_zeta_func_x_dot)
        self.wait(120)

    def __new_zeta_func_val_latex(self) -> Mobject:
        tex = always_redraw(
            lambda: MathTex(new_zeta_func_val_latex_str(
                self.zeta_func_x, self.zeta_func_val), color=YELLOW)
            .to_corner(UP + LEFT)
        )
        return tex

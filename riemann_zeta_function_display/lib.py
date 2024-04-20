from manim import *
from textwrap3 import *

# error amount used to control the degree of accuracy of the Riemann zeta function.
E = 1e-8


def __zeta(real, imag) -> (float, float):
    s = complex(real, imag)

    '''
    |             1        ∞     1       n              n
    |  ζ(s) = --------- *  Σ   ------- *  Σ   (-1)^k * (   ) * (k+1)^(-s)
    |         1-2^(1-s)   n=0  2^(n+1)   k=0             k
    '''

    res = 0 + 0j

    n = -1
    while True:
        n += 1

        step = 0 + 0j

        comb = 1
        for k in range(n + 1):
            step += comb * (k + 1) ** -s
            comb *= (k - n) / (k + 1)

        step *= 2 ** - (n + 1)
        res += step

        if abs(step) < E: break
    return res / (1 - 2 ** (1 - s))


# From: https://github.com/nyasyamorina/trash-bin/blob/main/render_zeta.py
# Definition of Riemann zeta function when the real part of s is within
# the closed interval from 0 to 1.
def zeta(s: complex) -> complex:
    """The Riemann zeta function."""
    print("Calculating zeta value for:", s)
    result = __zeta(s.real, s.imag)
    print("Result:", result)
    return result


class BaseScene(Scene):
    def __init__(
            self,
            renderer=None,
            camera_class=Camera,
            always_update_mobjects=False,
            random_seed=None,
            skip_animations=False,
    ):
        super().__init__(renderer, camera_class, always_update_mobjects, random_seed, skip_animations)
        self.zeta_func_latex_str = dedent(
            r"""\zeta(s) \equiv \begin{cases}
            \sum_{k=1}^{\infty} \frac{1}{k^2} & \Re(s) > 1 \\
            \frac{1}{1-2^{1-s}} \sum_{k=1}^{\infty} \frac{(-1)^{k+1}}{k^s} & 0 \le \Re(s) \le 1 \\
            2^s \pi^{s-1} \sin\frac{\pi s}{2} \Gamma(1-s) \zeta(1-s) & \Re(s) < 0
            \end{cases}"""
        )
        self.zeta_func_latex = None

    def construct(self):
        intro_text = Tex(r"Riemann $\zeta$ 函数的定义",
                         tex_template=TexTemplateLibrary.ctex, font_size=48)
        intro_text.to_corner(UP)
        self.zeta_func_latex = MathTex(self.zeta_func_latex_str,
                                       font_size=48)
        self.play(Write(intro_text), Write(self.zeta_func_latex, run_time=3))
        self.wait(1)

        self.play(FadeOut(intro_text),
                  FadeOut(self.zeta_func_latex))

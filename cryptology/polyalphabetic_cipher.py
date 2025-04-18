from manim import *
import numpy as np
from typing import List, Tuple


# 给定矩阵 A 和列向量 B。
A = np.matrix([
    [  3, 13, 21,  9 ],
    [ 15, 10,  6, 25 ],
    [ 10, 17,  4,  8 ],
    [  1, 23,  7,  2 ]
])
B = np.array([
    [  1 ],
    [ 21 ],
    [  8 ],
    [ 17 ]
])
A_inv = np.matrix([
    [ 23, 13, 20,  5 ],
    [  0, 10, 11, 26 ],
    [  9, 11, 15, 22 ],
    [  9, 22,  6, 25 ]
])


def letter_order(letter: str) -> int:
    """
    获取字母序号，用于加密或解密。
    :param letter:
    :return:
    """

    if ord('A') <= ord(letter) <= ord('Z'):
        return ord(letter) - ord('A')
    elif ord('a') <= ord(letter) <= ord('z'):
        return ord(letter) - ord('a')
    else:
        return -1


def matrix_latex(matrix: np.ndarray) -> str:
    """
    根据给定的矩阵，生成 LaTeX 代码。
    """

    result = r"\begin{bmatrix}"
    result += '\n'
    rows = matrix.tolist()
    for row in rows:
        row_len = len(row)
        for i, col in enumerate(row):
            result += ' '
            result += str(col)
            result += ' '
            if i < row_len - 1:
                result += '&'
        result += r"\\"
        result += '\n'
    result += r"\end{bmatrix}"
    return result


def list_vgroup(l: List[str], elem_color: ManimColor = RED) -> Tuple[VGroup, List[Text]]:
    """
    根据给定的列表，生成一个 VGroup。
    """

    result = [Text('[')]
    for i, s in enumerate(l):
        text = Text(s)
        text.set_color(elem_color)
        result.append(text.next_to(result[-1], RIGHT))
        if i < len(l) - 1:
            result.append(Text(',').next_to(result[-1], RIGHT))
    result.append(Text(']').next_to(result[-1], RIGHT))
    return VGroup(*result).center(), result


class PolyalphabeticCipherEncryption(Scene):
    """
    多表代换密码加密演示
    """

    def construct(self):
        # 给定明文。
        raw_text = "PLEASE SEND ME THE BOOK"
        raw_text_mobj = Text(raw_text)
        self.play(Write(raw_text_mobj))
        self.wait(2)

        # 对明文进行处理，仅保留字母。
        text = ''.join(filter(str.isalpha, raw_text))
        text_mobj = Text(text)
        self.play(Transform(raw_text_mobj, text_mobj, replace_mobject_with_target_in_scene=True))
        self.wait(2)

        # 将明文分组，4 个字母一组。
        text_blocks = [text[i:i+4] for i in range(0, len(text), 4)]
        text_blocks_mobj, text_blocks_texts = list_vgroup(text_blocks)
        self.play(Transform(text_mobj, text_blocks_mobj, replace_mobject_with_target_in_scene=True))
        self.wait(2)

        # 检查最后一组明文是否是 4 个字母的长度，长度不足则用 'A' 补齐到 4 个字母。
        if len(text_blocks[-1]) < 4:
            text_blocks[-1] = text_blocks[-1].ljust(4, 'A')
        text_blocks_mobj_1, text_blocks_texts = list_vgroup(text_blocks)
        self.play(Transform(text_blocks_mobj, text_blocks_mobj_1))
        self.wait(2)

        # 将各组字母转换为序号列向量的形式，得到一系列明文 Mi。
        Mi = [
            np.array([[letter_order(ch)] for ch in text_block])
            for text_block in text_blocks
        ]
        Mi_mobj = [MathTex(matrix_latex(M)).set_color(RED) for M in Mi]
        for i in range(1, len(Mi_mobj)):
            Mi_mobj[i].next_to(Mi_mobj[i - 1], RIGHT)
        Mi_vgroup = VGroup(*Mi_mobj)
        Mi_vgroup.center()
        Mi_vgroup.next_to(text_blocks_mobj, UP)
        for i, Mm in enumerate(Mi_mobj):
            text = text_blocks_texts[2 * i + 1].copy()
            self.add(text)
            text.target = Mm
            self.play(MoveToTarget(text))
            self.wait(2)
            self.add(Mm)
            self.remove(text)
        self.play(Mi_vgroup.animate.center(), FadeOut(text_blocks_mobj))
        self.wait(2)

        # 给定矩阵 A 和列向量 B。
        self.play(Mi_vgroup.animate.to_edge(LEFT + UP).scale(0.5))
        A_mobj = MathTex("A=", matrix_latex(A)).center()
        A_mobj.submobjects[1].set_color(BLUE)
        self.play(Write(A_mobj))
        self.wait(2)
        self.play(A_mobj.animate.scale(0.5).next_to(Mi_vgroup, RIGHT))
        B_mobj = MathTex("B=", matrix_latex(B)).center()
        B_mobj.submobjects[1].set_color(YELLOW)
        self.play(Write(B_mobj))
        self.wait(2)
        self.play(B_mobj.animate.scale(0.5).next_to(A_mobj, RIGHT))
        self.wait(2)

from manim import *
from Game import Gameboard


class Test(Scene):
    def construct(self):
        paragraph = TextGroup("სალამი, ასე ძალიან",
                              "სწრაფად ვწერ", "და კაია მოკლედ რა")
        self.play(Write(paragraph))
        self.play(ApplyMethod(paragraph.to_edge, UP))
        self.play(ApplyMethod(paragraph.scale, 0.5))
        self.wait(2)


class TextGroup(VGroup):
    def __init__(self, *args, **kwargs):
        self.lines = []
        for arg in args:
            print(arg)
            self.lines.append(Text(arg))
        for i, line in enumerate(self.lines):
            line.shift(0.8 * DOWN * i)
        VGroup.__init__(self, *self.lines, **kwargs)


class Main(Scene):
    def construct(self):
        self.set_background()

        # Board's public methods are animated by deafault
        # We can still use VGroup's methods on it
        # Some unexpected things still may happen, the world is a scary place
        board = Board(5, self)
        board.center()
        board.to_edge(DOWN)

        # self.play(DrawBorderThenFill(board, run_time=2))
        # self.play(ApplyMethod(board.rescale_to_fit,
        #                       4, 0, {"about_edge": DOWN}))

        board.rescale_to_fit(4, 0, about_edge=DOWN)
        self.add(board)

        #board.highlight((0, 0), (1, 0), (0, 1))

        cursor = Cursor(board, self)
        cursor.next_to(board, RIGHT)
        self.play(ShowCreation(cursor), run_time=0.5)
        cursor.move_and_click(2, 1)
        cursor.move_and_click(0, 0)
        cursor.move_and_click(3, 4)
        cursor.move_and_click(0, 1)
        # cursor.push_cell(2, 1)
        # cursor.move_to_cell(1, 3)
        # cursor.move_to_cell(0, 3)
        # cursor.move_to_cell(4, 4)
        # cursor.move_to_cell(0, 0)
        #cursor.push_cell(1, 3)
        #board.push((0, 0), (1, 0), (0, 1))
        #self.play(ApplyMethod(cursor.to_edge, LEFT))
        #cursor.move_to_cell(0, 3)

        self.wait(3)

    def set_background(self):
        background = Rectangle(
            width=20,
            height=10,
            stroke_width=0,
            fill_color="#3E746F",
            fill_opacity=1)
        self.add(background)


class Cursor(SVGMobject):
    def __init__(self, board, scene):
        SVGMobject.__init__(self, "cursor.svg",
                            stroke_width=1, stroke_color=BLACK)
        self._scene = scene
        self._board = board
        self.scale(0.3)

    def push(self, **kwargs):
        self._scene.play(ApplyMethod(self.scale, 0.8,
                                     rate_func=there_and_back_with_pause), **kwargs)

    def push_cell(self, x, y, **kwargs):
        self._board.play(y, x, animate=False)
        self._scene.play(ApplyMethod(self._board.scale_group, x, y, 0.85),
                         ApplyMethod(self.scale, 0.9, rate_func=there_and_back_with_pause),
                         **kwargs)
        # self._scene.play(
        #     self._board.animate.animation().scale_group(x, y, 1 / 0.85), **kwargs)
        def func(board):
            board.scale_group(x, y, 1 / 0.85)
            board.animation()
            return board
        self._scene.play(ApplyFunction(func, self._board))

    def move_to_cell(self, x, y, **kwargs):
        loc = self._board.get_cell(x, y).get_center() - 0.9 * (self.get_corner(UP + LEFT) - self.get_center())
        self._scene.play(ApplyMethod(self.move_to, loc), **kwargs)

    def move_and_click(self, x, y, move_time=1, push_time=1):
        self.move_to_cell(x, y, run_time=move_time)
        self.push_cell(x, y, run_time=push_time/2)

class Board(VGroup):
    def __init__(self, size, scene):
        np.random.seed(18)
        self._gameboard = Gameboard(size)
        self._scene = scene
        self._nrows = self._gameboard.nrows
        self._ncols = self._gameboard.ncols
        self._create_cells()

        VGroup.__init__(self, *self._cells.flatten())

    def _create_cells(self):
        self._cells = np.empty((self._nrows, self._ncols), dtype=object)
        self._groups = np.empty((self._nrows, self._ncols), dtype=object)
        for i in range(self._nrows):
            for j in range(self._ncols):
                self._cells[i, j] = Cell()
                self._cells[i, j].set_state(self._gameboard.get_state()[i, j])
                if j > 0:
                    self._cells[i, j].next_to(self._cells[i, j - 1])
                if i > 0:
                    self._cells[i, j].next_to(self._cells[i - 1, j], DOWN)

    def get_cell(self, row, col):
        return self._cells[row, col]

    def set_state(self, matrix, **kwargs):
        self._gameboard.set_state(matrix)
        if animate:
            self._scene.play(ApplyMethod(self.animation, **kwargs))

    def animation(self):
        for i in range(self._nrows):
            for j in range(self._ncols):
                self._cells[i, j].set_state(self._gameboard.get_state()[i, j])
        return self

    def scale_group(self, x, y, scale):
        self._cells[x, y].scale(scale)
        for coord in self._gameboard.neighbours(x, y):
            self._cells[coord[0], coord[1]].scale(
                scale, about_point=self._cells[x, y].get_center())
        return self

    def restart(self, animate=True, **kwargs):
        self._gameboard.restart()
        if animate:
            self._scene.play(ApplyMethod(self.animation, **kwargs))

    def play(self, x, y, animate=True, **kwargs):
        self._gameboard.play(x, y)
        if animate:
            self._scene.play(ApplyMethod(self.animation, **kwargs))

    def highlight(self, *coords, color=WHITE, **kwargs):
        group = VGroup()
        for coord in coords:
            group += self._cells[coord[0], coord[1]]
        self._scene.play(Indicate(group, color=color,
                                  rate_func=there_and_back_with_pause), **kwargs)

    def push(self, *coords, color=WHITE, **kwargs):
        group = VGroup()
        for coord in coords:
            group += self._cells[coord[0], coord[1]]
        self._scene.play(ApplyMethod(group.scale, 0.8,
                                     rate_func=there_and_back_with_pause), **kwargs)


class Cell(RoundedRectangle):
    def __init__(self, **kwargs):
        RoundedRectangle.__init__(self, width=2, height=2,
                                  fill_opacity=1, fill_color=GREY,
                                  corner_radius=0.2, **kwargs)

    def set_state(self, state):
        if state:
            self.set_color(YELLOW)
        else:
            self.set_color(GRAY)
        return self

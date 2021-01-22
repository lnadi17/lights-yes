from manim import *
from Game import Gameboard

class TextGroup(VGroup):
    def __init__(self, *args, **kwargs):
        self.lines = []
        for arg in args:
            if type(arg) == str:
                self.lines.append(Text(arg))
            else:
                strings = arg[0].split(" ")
                colors = arg[1]
                group = VGroup()
                for text, color in zip(strings, colors):
                    group += Text(text, color=color)
                group.arrange(RIGHT)
                self.lines.append(group)
        for i, line in enumerate(self.lines):
            line.shift(0.8 * DOWN * i)
        VGroup.__init__(self, *self.lines, **kwargs)


class Main(Scene):
    def construct(self):
        #self.set_background()

        text_1 = TextGroup("დავიწყოთ თამაშის წესების აღწერით")
        text_2 = TextGroup("თამაშის კლასიკური წესების მიხედვით,",
                           "გვაქვს 5x5 ზომის, 25 უჯრიანი დაფა")
        text_3 = TextGroup("თითოეული უჯრა შეიძლება იყოს",
                           ("ანთებული ან ჩამქრალი", ("#FFC300", WHITE, "#900C3F")))
        text_4 = TextGroup("თუ რომელიმე უჯრას დავაჭერთ,",
                           "ის და მისი მეზობელი უჯრები",
                           "საპირისპიროდ შეტრიალდებიან")
        text_5 = TextGroup("თამაშს მაშინ მოვიგებთ, როცა",
                           "მოვახერხებთ ყველა უჯრის ანთებას")
        text_6 = TextGroup("თამაშის ამოხსნა საკმაოდ რთულია")
        text_7 = TextGroup("განსაკუთრებით, როცა სვლების მინიმალური",
                           "რაოდენობის გამოყენებას ვცდილობთ")
        text_8 = TextGroup("ვცადოთ გზის პოვნა, რომელიც კლასიკური",
                           "ზომის დაფას ამოგვახსნევინებს")
        text_2.to_edge(UP)
        text_3.to_edge(UP, buff=LARGE_BUFF)
        text_4.to_edge(UP)
        text_5.to_edge(UP, buff=LARGE_BUFF)
        text_6.to_edge(UP, buff=LARGE_BUFF)
        text_6.move_to(text_5.get_center())

        self.play(Write(text_1), run_time=2)
        self.wait(1)
        self.play(ReplacementTransform(text_1, text_2))
        self.create_board(np.zeros((5, 5)))
        left_brace = Brace(self.board, LEFT, buff=0.1)
        left_text = left_brace.get_text("5")
        top_brace = Brace(self.board, UP, buff=0.1)
        top_text = top_brace.get_text("5")
        self.play(GrowFromCenter(left_brace),
                  GrowFromCenter(top_brace),
                  FadeIn(top_text),
                  FadeIn(left_text))
        self.wait()
        self.play(ShrinkToCenter(left_brace),
                  ShrinkToCenter(top_brace),
                  FadeOut(top_text),
                  FadeOut(left_text))
        self.play(ReplacementTransform(text_2, text_3))
        self.wait()
        self.board.restart(run_time=1)
        self.wait()
        self.board.restart(run_time=1)
        self.wait()
        # sol: [(3, 0), (2, 1), (2, 2), (3, 2), (4, 2), (2, 3), (3, 3), (0, 4)]
        solvable = np.array([[True, True, True, False, False],
                             [True, False, True, False, False],
                             [True, False, True, True, True],
                             [False, False, False, False, True],
                             [False, False, False, False, True]])
        self.board.set_state(solvable, run_time=1)
        self.wait()
        self.play(ReplacementTransform(text_3, text_4))
        self.wait()
        self.create_cursor()
        self.cursor.move_and_click(1, 2)
        self.cursor.move_and_click(2, 4)
        self.cursor.move_and_click(0, 3)
        self.cursor.move_and_click(2, 2)
        self.cursor.move_and_click(2, 3)
        self.wait()
        self.play(ReplacementTransform(text_4, text_5))
        self.wait()
        self.cursor.move_and_click(3, 3)
        self.cursor.move_and_click(4, 0)
        self.cursor.move_and_click(3, 2)
        self.play(ApplyMethod(self.cursor.next_to,
                              self.board.get_corner(UP + RIGHT), RIGHT, 2))
        self.wait(1)
        # sol:  [(1, 0), (3, 0), (4, 0), (0, 1), (3, 1), (2, 2), (3, 2), (0, 3), (2, 3), (3, 4)]
        solvable = np.array([[True, False, True, False, True],
                             [False, True, True, False, True],
                             [True, False, False, False, False],
                             [False, True, True, False, True],
                             [False, True, True, False, False]])

        def grow(board): return board.scale(1.1).set_color(WHITE)
        def shrink(board): return board.scale(1 / 1.1).animation()

        self.board.set_state(solvable, animate=False)
        self.play(Succession(ApplyFunction(grow, self.board),
                             ApplyFunction(shrink, self.board)),
                  ReplacementTransform(text_5, text_6))
        self.bring_to_front(self.cursor)
        self.wait()
        self.cursor.move_and_click(0, 1, move_time=0.25, push_time=0.25)
        self.cursor.move_and_click(0, 3, move_time=0.25, push_time=0.25)
        self.cursor.move_and_click(0, 4, move_time=0.25, push_time=0.25)
        self.play(ApplyMethod(text_6.to_edge, UP))
        text_7.next_to(text_6, DOWN, buff=0.1)
        self.play(Write(text_7))
        self.cursor.move_and_click(1, 0, move_time=0.25, push_time=0.25)
        self.cursor.move_and_click(1, 3, move_time=0.25, push_time=0.25)
        self.cursor.move_and_click(2, 2, move_time=0.25, push_time=0.25)
        self.cursor.move_and_click(2, 3, move_time=0.25, push_time=0.25)
        self.cursor.move_and_click(3, 0, move_time=0.25, push_time=0.25)
        self.cursor.move_and_click(3, 2, move_time=0.35, push_time=0.35)
        self.cursor.move_and_click(4, 3, move_time=0.5, push_time=0.5)
        self.play(FadeOut(self.cursor))
        self.wait()
        self.play(FadeOut(self.board), ReplacementTransform(
            VGroup(text_6, text_7), text_8), run_time=2)
        self.wait(3)
        self.play(FadeOut(text_8))

    def set_background(self):
        background = Rectangle(
            width=20,
            height=10,
            stroke_width=0,
            fill_color="#3E746F",
            fill_opacity=1)
        self.add(background)

    def create_board(self, initial_state=None):
        # Board's public methods are animated by default
        # We can still use VGroup's methods on it
        # Some unexpected things still may happen, the world is a scary place
        self.board = Board(5, self)
        if initial_state is not None:
            self.board.set_state(initial_state, animate=False)
            self.board.animation()
        self.board.center()
        self.board.to_edge(DOWN)
        self.board.rescale_to_fit(4.25, 0, about_edge=DOWN)
        self.play(DrawBorderThenFill(self.board, run_time=2))

    def create_cursor(self):
        self.cursor = Cursor(self.board, self)
        self.cursor.next_to(self.board.get_corner(UP + RIGHT), RIGHT, 2)
        self.play(ShowCreation(self.cursor), run_time=1.5)


class Cursor(SVGMobject):
    def __init__(self, board, scene):
        SVGMobject.__init__(self, "cursor.svg",
                            stroke_width=1, stroke_color=BLACK)
        self._scene = scene
        self._board = board
        self.scale(0.3)

    def push(self, **kwargs):
        self._scene.play(ApplyMethod(self.scale, 0.8,
                                     rate_func=there_and_back_with_pause),
                         **kwargs)

    def push_cell(self, x, y, **kwargs):
        self._board.play(y, x, animate=False)
        self._scene.play(ApplyMethod(self._board.scale_group, x, y, 0.85),
                         ApplyMethod(self.scale, 0.9,
                                     rate_func=there_and_back_with_pause),
                         **kwargs)

        def func(board):
            board.scale_group(x, y, 1 / 0.85)
            board.animation()
            return board

        self._scene.play(ApplyFunction(func, self._board))

    def move_to_cell(self, x, y, **kwargs):
        loc = self._board.get_cell(x, y).get_center(
        ) - 0.9 * (self.get_corner(UP + LEFT) - self.get_center())
        self._scene.play(ApplyMethod(self.move_to, loc), **kwargs)

    def move_and_click(self, x, y, move_time=1, push_time=1):
        self.move_to_cell(x, y, run_time=move_time)
        self.push_cell(x, y, run_time=push_time / 2)


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

    def set_state(self, matrix, animate=True, **kwargs):
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
            self.set_color("#FFC300")
        else:
            self.set_color("#900C3F")
        return self

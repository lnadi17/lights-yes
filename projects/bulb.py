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

class Test(Scene):
    def construct(self):
        text_5 = TextGroup("შემოვიღოთ სვლების მატრიცა,",
                           "რომელშიც ეწერება თუ რამდენჯერ უნდა",
                           "დავაჭიროთ შესაბამის უჯრას მოსაგებად")
        self.play(Write(text_5.rescale_to_fit(7.3, 0).to_corner(UP+LEFT)))

class Unwrite(Write):
    def __init__(self, *args, **kwargs):
        Write.__init__(self, *args, rate_func=lambda t: 1 - t, **kwargs)

class Main(Scene):
    def construct(self):
        #self.set_background()
        text_ = TextGroup()
        text_1 = TextGroup("დავაკვირდეთ რამდენიმე დეტალს")
        text_2 = TextGroup("უჯრაზე ორჯერ დაჭერა არაფერს არ ცვლის")
        text_3 = TextGroup("რადგან ეს ერთხელ უკვე შეცვლილ ღილაკებს",
                           "ძველ პოზიციაში დააბრუნებს")
        text_4 = TextGroup("აქედან გამომდინარე, მოსაგებად ყოველ",
                           "უჯრაზე მაქსიმუმ ერთხელ დაჭერა საკმარისია")
        text_5 = TextGroup("შემოვიღოთ სვლების მატრიცა,",
                           "რომელშიც ეწერება თუ რამდენჯერ უნდა",
                           "დავაჭიროთ შესაბამის უჯრას მოსაგებად")
        #text_6 = TextGroup("სვლების მატრიცა")
        text_7 = TextGroup("რადგან 2-ჯერ დაჭერა არაფერს ცვლის,",
                           "მატრიცაში მხოლოდ 0 ან 1 ჩაიწერება")
        text_8 = TextGroup("თამაშის მოსაგებად სწორედ", 
                           "სვლების მატრიცის პოვნა დაგვჭირდება") # indicate matrix
        text_2.to_edge(UP)
        text_3.next_to(text_2, DOWN, buff=0.1)
        text_4.move_to(text_3.get_center())

        self.play(Write(text_1, run_time=2))
        self.play(FadeOut(text_1))
        self.create_board()
        self.play(Write(text_2))
        board_left = self.board.copy()
        self.play(ApplyMethod(board_left.to_edge, LEFT, 1),
                  ApplyMethod(self.board.to_edge, RIGHT, 1))
        self.create_cursor()
        self.wait()
        self.play(Write(text_3))
        self.wait()
        equal = TexMobject("=").scale(4)
        equal.move_to([equal.get_center()[0], self.board.get_center()[1], 0])
        self.play(
            Write(equal), 
            ApplyMethod(self.cursor.move_to_cell, 2, 1, {"animate": False}), 
            run_time=3)
        self.cursor.push_cell(2, 1, run_time=1/2)
        self.cursor.push_cell(2, 1, run_time=1/2)
        self.play(ApplyMethod(self.cursor.next_to, self.board.get_corner(DOWN + RIGHT), RIGHT))
        self.wait(2)

        def grow(board): return board.scale(1.05).set_color(WHITE)
        def shrink(board): return board.scale(1 / 1.05).animation()

        # sol: [(0, 0), (2, 0), (3, 0), (2, 1), (3, 1), (0, 2), (1, 2), (4, 3), (0, 4), (1, 4)]
        solvable = np.array([[False,  True, False, False, False],
                             [ True,  True, False, False, False],
                             [ True,  True,  True, False, False],
                             [ True,  True,  True, False, False],
                             [ True,  True, False,  True, False]])
        self.board.set_state(solvable, animate=False)
        board_left.set_state(self.board._gameboard.get_state(), animate=False)
        self.play(Succession(ApplyFunction(grow, self.board),
                             ApplyFunction(shrink, self.board)),
                  Succession(ApplyFunction(grow, board_left),
                             ApplyFunction(shrink, board_left)))
        self.bring_to_front(self.cursor)
        self.cursor.move_and_click(2, 1, move_time=0.5, push_time=0.5)
        self.cursor.move_and_click(3, 2, move_time=0.5, push_time=0.5)
        self.cursor.move_and_click(2, 1, move_time=0.5, push_time=0.5)
        self.cursor.move_and_click(3, 2, move_time=0.5, push_time=0.5)
        self.play(ApplyMethod(self.cursor.next_to, self.board.get_corner(DOWN + RIGHT), RIGHT))
        self.wait()
        self.play(Indicate(equal))
        self.wait()
        self.play(ReplacementTransform(text_3, text_4.scale(0.8).next_to(text_2, DOWN, 0.08)), 
                  ApplyMethod(text_2.scale, 0.8))
        self.wait(2.5)
        self.play(Unwrite(equal), run_time=2.5)
        self.play(ApplyMethod(board_left.move_to, self.board.get_center()))
        self.remove(board_left)
        self.board.generate_target()
        self.board.target.rescale_to_fit(5, 0, about_edge=RIGHT)
        self.board.target.center().to_edge(RIGHT)
        self.play(FadeOut(VGroup(text_4, text_2)))
        self.play(MoveToTarget(self.board)) 
        self.wait()
        self.play(Write(text_5.rescale_to_fit(7.7, 0).to_corner(UP+LEFT)), run_time=2)
        self.wait()
        moves_mat = np.array([[1, 0, 1, 1, 0],
                              [0, 0, 1, 1, 0],
                              [1, 1, 0, 0, 0],
                              [0, 0, 0, 0, 1],
                              [1, 1, 0, 0, 0]])
        mat = IntegerMatrix(moves_mat).next_to(text_5, DOWN)
        self.play(Write(mat), run_time=3)
        self.wait()
        self.play(Write(text_7.rescale_to_fit(7.7, 0).next_to(mat, DOWN)))
        self.play(Indicate(mat, scale_factor=1.05, color=WHITE))
        self.wait()
        mat.generate_target()
        for i in range(len(moves_mat)):
            for j in range(len(moves_mat)):
                if moves_mat[i, j] == 1:
                    mat.target.get_mob_matrix()[i, j].set_color("#0B8F14")
                    # add X's to each of the cell
                    self.board.add_x_object(i, j)
        self.play(MoveToTarget(mat))
        # self.play(*[anim for i in range(<number>])
        animations = []
        for i in range(self.board._nrows):
            for j in range(self.board._ncols):
                if moves_mat[i, j] == 1:
                        animations.append(ReplacementTransform(mat.get_mob_matrix()[i, j].copy(), self.board.get_x_objects()[i, j]))
        self.play(*animations, run_time=3)
        self.wait()
        # self.bring_to_front(self.cursor)
        # self.cursor.move_to_cell(0, 0, offset_coeff=0.25)
        self.play(ApplyMethod(self.board.get_x_objects()[0, 0].shift, UP))
        print("scene:", id(self.board))
        self.cursor.shift_down(0, 0)

    def set_background(self):
        background = Rectangle(
            width=20,
            height=10,
            stroke_width=0,
            fill_color="#3E746F",
            fill_opacity=1)
        self.add(background)

    def create_board(self, initial_state=None):
        self.board = Board(5, self)
        if initial_state is not None:
            self.board.set_state(initial_state, animate=False)
            self.board.animation()
        self.board.center()
        self.board.to_edge(DOWN)
        self.board.rescale_to_fit(4.25, 0, about_edge=DOWN)
        self.play(DrawBorderThenFill(self.board, run_time=3))

    def create_cursor(self):
        self.cursor = Cursor(self.board, self)
        self.cursor.next_to(self.board.get_corner(DOWN + RIGHT), RIGHT)
        self.play(ShowCreation(self.cursor), run_time=1.5)

class Intro(Scene):
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
        self.cursor.move_and_click(0, 1, move_time=0.5, push_time=0.25)
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

        self._scene.play(ApplyFunction(func, self._board), **kwargs)

    def shift_down(self, x, y):
        print("cursor:", id(self._board))
        self._scene.play(ApplyMethod(self._board.shift_down, 0, 0))

    def move_to_cell(self, x, y, animate=True, offset_coeff=0, **kwargs):
        loc = self._board.get_cell(x, y).get_center(
        ) - 0.9 * (self.get_corner(UP + LEFT) - self.get_center()) + offset_coeff*(DOWN+RIGHT)
        if animate:
            self._scene.play(ApplyMethod(self.move_to, loc), **kwargs)
        else:
            self.move_to(loc)

    def move_and_click(self, x, y, move_time=1, push_time=1):
        self.move_to_cell(x, y, run_time=move_time)
        self.push_cell(x, y, run_time=push_time / 2)

class Board(VGroup):
    def __init__(self, size, scene, seed=18):
        np.random.seed(seed)
        self._gameboard = Gameboard(size)
        self._scene = scene
        self._nrows = self._gameboard.nrows
        self._ncols = self._gameboard.ncols
        self._create_cells()

        VGroup.__init__(self, *self._cells.flatten())

    def _create_cells(self):
        self._cells = np.empty((self._nrows, self._ncols), dtype=object)
        self._x_objects = np.empty((self._nrows, self._ncols), dtype=object)        
        for i in range(self._nrows):
            for j in range(self._ncols):
                self._cells[i, j] = Cell()
                self._cells[i, j].set_state(self._gameboard.get_state()[i, j])
                if j > 0:
                    self._cells[i, j].next_to(self._cells[i, j - 1])
                if i > 0:
                    self._cells[i, j].next_to(self._cells[i - 1, j], DOWN)

    def add_x_objects(self, matrix):
        for row in range(self._nrows):
            for col in range(self._ncols):
                if matrix[row, col] == 1:
                    self.add_x_object(row, col)

    def shift_down(self, x, y):
        print("board:", id(self))
        self._x_objects[x, y].shift(DOWN)

    def add_x_object(self, x, y):
        self._x_objects[x, y] = Text("+").rotate(PI / 4).move_to(self._cells[x, y].get_center()).shift(RIGHT*0.01).set_color("#0B8F14")

    # def clear_x_objects(self):
    #     self._x_objects = np.empty((self._nrows, self._ncols), dtype=object)        

    def get_x_objects(self):
        return self._x_objects

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

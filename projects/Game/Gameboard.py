# import all necessary libraries
import numpy as np
import queue

# final implementation of the Gameboard class


class Gameboard:
    def __init__(self, shape):
        self.nrows, self.ncols = shape, shape
        self.col_labels, self.row_labels = [i for i in range(shape)], [
            i for i in range(shape)]

        # create board matrix
        self.board = self.fast_random_bool([self.nrows, self.ncols])

        # initialize counter
        self.bulb_count = np.sum(self.board)

    # method from stackoverflow
    def fast_random_bool(self, shape):
        n = np.prod(shape)
        nb = -(-n // 8)  # ceiling division
        b = np.frombuffer(np.random.bytes(nb), np.uint8, nb)
        return np.unpackbits(b)[:n].reshape(shape).view(np.bool)

    # triggers a single bulb
    def trigger_bulb(self, x, y):
        self.board[y, x] = not self.board[y, x]

    # makes a single move which triggers multiple bulbs
    def play(self, x, y):
        self.trigger_bulb(x, y)
        for loc in self.neighbours(x, y):
            self.trigger_bulb(loc[0], loc[1])
        self.bulb_count = np.sum(self.board)

    # takes an array of moves and plays them
    def play_multiple(self, array):
        for move in array:
            self.play(move[0], move[1])

    # restarts game
    def restart(self):
        self.board = self.fast_random_bool([self.nrows, self.ncols])
        self.bulb_count = np.sum(self.board)

    def set_state(self, matrix):
        self.board = np.flip(np.flip(matrix, 0), 0)
        self.bulb_count = np.sum(self.board)

    def get_state(self):
        return self.board

    # returns array of neighbouring locations of passed location (diagonal direction doesn't count)
    def neighbours(self, x, y):
        result = []

        if self.in_range(x, y - 1):
            result.append((x, y - 1))

        if self.in_range(x, y + 1):
            result.append((x, y + 1))

        if self.in_range(x - 1, y):
            result.append((x - 1, y))

        if self.in_range(x + 1, y):
            result.append((x + 1, y))

        return result

    # returns True if passed location is within bounds
    def in_range(self, x, y):
        if y >= 0 and y < self.nrows and x >= 0 and x < self.ncols:
            return True
        return False

    # returns True if all bulbs are on
    def is_game_over(self):
        if self.bulb_count == self.nrows * self.ncols:
            return True
        return False

    # returns number of bulbs currently on
    def get_bulb_count(self):
        return self.bulb_count

    # make a queue and do bfs for solution (this guarantees the least amount of moves but takes a long time)
    def solve_bfs(self):
        # method number 1
        q = queue.Queue()

        visited = set()
        visited.add(tuple(self.get_state().flat))
        for i in range(self.nrows):
            for j in range(self.ncols):
                # put the first elements in queue
                q.put([(i, j)])

        while True:
            # make a recorded set of moves
            moves = q.get()
            if q.empty():
                # print("answer not found")
                return None
            self.play_multiple(moves)
            # check for win
            if self.is_game_over():
                self.play_multiple(moves)
                # print("answer: ", moves)
                return moves
            # enqueue a new set of moves if this state hasn't been visited yet
            if tuple(self.get_state().flat) not in visited:
                for i in range(self.nrows):
                    for j in range(self.ncols):
                        q.put(moves + [(i, j)])
            # add the current move to the visited set
            visited.add(tuple(self.get_state().flat))
            # revert play
            self.play_multiple(moves)

    def solve_mat(self):
        a = self.get_moves_matrix((self.nrows, self.ncols))
        b = self.get_diff_matrix((self.nrows, self.ncols))
        return self.solve_linalg(a, b)

    # can solve for any board size, returns array of moves (is relatively slow)
    def solve_linalg(self, A, B):
        self.rref(A, B)
        null = self.null_space(A)
        if null == []:
            return [self.get_linalg_moves(self.exact(A, B))]
        x = self.particular(A, B)
        if x is None:
            return None
        else:
            sols = [(sum(s) + x) % 2 for s in self.powerset(null) if s != []]
            sols += [x]
        for sol in sols:
            print(self.get_linalg_moves(sol))
        return [self.get_linalg_moves(sol) for sol in sols]

    def rref(self, A, B=None):
        i, piv = 0, 0
        while i + piv < len(A):
            if A[i, i + piv] == 1:
                for k in range(len(A)):
                    if k == i:
                        continue
                    if A[k, i + piv] == 1:
                        A[k, :] += A[i, :]
                        A[k, :] %= 2
                        if B is not None:
                            B[k] = (B[k] + B[i]) % 2
            else:
                row_changed = False
                for k in range(len(A) - i - 1):
                    if A[i + k + 1, i + piv] == 1:
                        temp = A[i, :].copy()
                        A[i, :] = A[i + k + 1, :]
                        A[i + k + 1, :] = temp
                        if B is not None:
                            temp = B[i]
                            B[i] = B[i + k + 1]
                            B[i + k + 1] = temp
                        row_changed = True
                        break
                if not row_changed:
                    piv += 1
                i -= 1
            i += 1

    def null_space(self, A):
        results = []
        i, piv, col = 0, 0, 0
        to_fix = []
        while col < len(A):
            if A[i, i + piv] == 1:
                i += 1
            else:
                to_fix.append(col)
                piv += 1
            col += 1
        no_fix = np.delete(np.arange(0, len(A), 1), to_fix)
        for col_num in range(len(to_fix)):
            result = np.array([0] * len(A))
            fixed = to_fix[col_num]
            result[fixed] = 1
            for i in range(len(A)):
                if A[i, fixed] == 1:
                    result[no_fix[i]] = (result[no_fix[i]] + 1) % 2
            results.append(result)
        return results

    def particular(self, A, B):
        i, piv, col = 0, 0, 0
        to_fix = []
        while col < len(A):
            if A[i, i + piv] == 1:
                i += 1
            else:
                to_fix.append(col)
                piv += 1
            col += 1
        no_fix = np.delete(np.arange(0, len(A), 1), to_fix)

        if 1 in B[-len(to_fix):]:
            # print('no solution, sorry')
            return None

        result = [0] * len(A)
        for i in range(len(no_fix)):
            result[no_fix[i]] = B[i]
        fixed = to_fix[0]
        result[fixed] = 1
        for i in range(len(A)):
            if A[i, fixed] == 1:
                result[no_fix[i]] = (result[no_fix[i]] + 1) % 2
        return result

    # A, B must be in rref, must be used only when unique solution exists
    def exact(self, A, B):
        result = [0] * len(A)
        for row_index in range(len(A)):
            one_index = np.where(A[row_index] == 1)[0][0]
            result[one_index] = B[row_index]
        return result

    def powerset(self, seq):
        if len(seq) <= 1:
            yield seq
            yield []
        else:
            for item in self.powerset(seq[1:]):
                yield [seq[0]] + item
                yield item

    def get_moves_matrix(self, shape):
        mat = np.zeros((shape[0]**2, shape[1]**2))
        for i in range(shape[0]):
            for j in range(shape[1]):
                for n in self.neighbours(i, j) + [(i, j)]:
                    mat[i * shape[0] + j, n[0] * shape[0] + n[1]] += 1
        return mat

    def get_diff_matrix(self, shape):
        mat = np.ones(np.prod(shape))
        for i in range(shape[0]):
            for j in range(shape[1]):
                mat[i * shape[0] + j] -= self.get_state()[i, j]
        return mat

    def get_linalg_moves(self, x):
        moves = []
        for i in range(len(x)):
            if x[i] == 1:
                moves.append((i % int(np.sqrt(len(x))),
                              i // int(np.sqrt(len(x)))))
        return moves

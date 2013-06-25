import colorama
import sys
import random
from colorama import Fore, Back, Style

class Color:
    GREEN = 0
    RED = 1
    BLUE = 2
    ORANGE = 3
    WHITE = 4
    YELLOW = 5

class Side(object):
    F = 0
    R = 1
    B = 2
    L = 3
    U = 4
    D = 5

class Face(object):
    def __init__(self, side, color, *attached):
        self.side = side
        self.color = color
        self.attached = list(attached)

class Cube(object):
    def __init__(self, size=3):
        self.size = size
        self.colors = \
                [Color.GREEN] * size * size + \
                [Color.RED] * size * size + \
                [Color.BLUE] * size * size + \
                [Color.ORANGE] * size * size + \
                [Color.WHITE] * size * size + \
                [Color.YELLOW] * size * size

        self.faces = {
                Side.F: Face(
                        Side.F, Color.GREEN,
                        self.bottom_line(Side.U),
                        self.left_column(Side.R),
                        self.top_line(Side.D, True),
                        self.right_column(Side.L, True)
                    ),
                Side.R: Face(
                        Side.R, Color.RED,
                        self.right_column(Side.U, True),
                        self.left_column(Side.B),
                        self.right_column(Side.D, True),
                        self.right_column(Side.F, True)
                    ),
                Side.B: Face(
                        Side.B, Color.BLUE,
                        self.top_line(Side.U),
                        self.left_column(Side.L, True),
                        self.bottom_line(Side.D, True),
                        self.right_column(Side.R)
                    ),
                Side.L: Face(
                        Side.L, Color.ORANGE,
                        self.left_column(Side.U),
                        self.left_column(Side.F),
                        self.left_column(Side.D),
                        self.right_column(Side.B, True)
                    ),
                Side.U: Face(
                        Side.U, Color.WHITE,
                        self.top_line(Side.B),
                        self.top_line(Side.R),
                        self.top_line(Side.F),
                        self.top_line(Side.L)
                    ),
                Side.D: Face(
                        Side.D, Color.YELLOW,
                        self.bottom_line(Side.F),
                        self.bottom_line(Side.R),
                        self.bottom_line(Side.B),
                        self.bottom_line(Side.L)
                    )
                }

    def coord(self, side, line, sticker):
        return self.size * (side * self.size + line) + sticker

    def top_line(self, side, invert=False):
        if invert:
            return (self.coord(side, 0, 2), self.coord(side, 0, 1), self.coord(side, 0, 0))
        else:
            return (self.coord(side, 0, 0), self.coord(side, 0, 1), self.coord(side, 0, 2))

    def middle_line(self, side):
        return (self.coord(side, 1, 0), self.coord(side, 1, 1), self.coord(side, 1, 2))

    def bottom_line(self, side, invert=False):
        if invert:
            return (self.coord(side, 2, 2), self.coord(side, 2, 1), self.coord(side, 2, 0))
        else:
            return (self.coord(side, 2, 0), self.coord(side, 2, 1), self.coord(side, 2, 2))

    def right_column(self, side, invert=False):
        if invert:
            return (self.coord(side, 2, 2), self.coord(side, 1, 2), self.coord(side, 0, 2))
        else:
            return (self.coord(side, 0, 2), self.coord(side, 1, 2), self.coord(side, 2, 2))

    def left_column(self, side, invert=False):
        if invert:
            return (self.coord(side, 2, 0), self.coord(side, 1, 0), self.coord(side, 0, 0))
        else:
            return (self.coord(side, 0, 0), self.coord(side, 1, 0), self.coord(side, 2, 0))

    def assign_line(self, src, target, invert=False):
        for i in xrange(len(src)):
            if invert:
                self.colors[target[i]] = self.colors[src[::-1][i]]
            else:
                self.colors[target[i]] = self.colors[src[i]]

    def assign_line_values(self, values, target_coords):
        for i in xrange(len(values)):
            self.colors[target_coords[i]] = values[i]

    def get_line(self, line):
        return [self.colors[i] for i in line]

    def make_2d(self, side):
        result = []
        for i in xrange(self.size):
            result.append([])
            for j in xrange(self.size):
                result[i].append(self.colors[self.coord(side, i, j)])
        return result

    def turn(self, side):
        f = self.faces[side]
        face_array = self.make_2d(side)

        rotated = zip(*face_array[::-1])
        for i in xrange(self.size):
            for j in xrange(self.size):
                self.colors[self.coord(side, i, j)] = rotated[i][j]

        tmp = self.get_line(f.attached[0])
        self.assign_line(f.attached[3], f.attached[0])
        self.assign_line(f.attached[2], f.attached[3])
        self.assign_line(f.attached[1], f.attached[2])
        self.assign_line_values(tmp, f.attached[1])

    def is_bad_edge(self, side, line, sticker):
        if side == Side.U or side == Side.D:
            edge_ud = self.colors[self.coord(side, line, sticker)]
            if (edge_ud == self.faces[Side.R].color or
                edge_ud == self.faces[Side.L].color):
                return True
            else:
                f = self.faces[side]
                if side == Side.U or side == Side.D:
                    if line == 0:
                        edge_s = self.colors[f.attached[0][1]]
                    elif line == 1:
                        if sticker == 0:
                            edge_s = self.colors[f.attached[3][1]]
                        elif sticker == 2:
                            edge_s = self.colors[f.attached[1][1]]
                        else:
                            raise Exception("Not an edge: side = {}, line = {}, sticker = {}"
                                            .format(side, line, sticker))
                    elif line == 2:
                        edge_s = self.colors[f.attached[2][1]]
                    else:
                        raise Exception("Not an edge: side = {}, line = {}, sticker = {}"
                                        .format(side, line, sticker))
                    if (edge_s == self.faces[Side.U].color or
                        edge_s == self.faces[Side.D].color):
                        return True
                    else:
                        return False
        elif side == Side.F or side == Side.B:
            f = self.faces[side]
            if line != 1:
                raise Exception("Not an edge: side = {}, line = {}, sticker = {}"
                                .format(side, line, sticker))

            edge_fb = self.colors[self.coord(side, line, sticker)]
            if (edge_fb == self.faces[Side.R].color or
                edge_fb == self.faces[Side.L].color):
                return True
            else:
                if sticker == 0:
                    edge_s = self.colors[f.attached[3][1]]
                elif sticker == 2:
                    edge_s = self.colors[f.attached[1][1]]
                else:
                    raise Exception("Not an edge: side = {}, line = {}, sticker = {}"
                                    .format(side, line, sticker))
                if (edge_s == self.faces[Side.U].color or
                    edge_s == self.faces[Side.D].color):
                    return True
                else:
                    return False
        else:
            raise Exception("Invalid side to check (only F, B, U, D allowed)")

    def bad_edge_count(self):
        edges = [
                    (Side.U, 0, 1),
                    (Side.U, 1, 0),
                    (Side.U, 1, 2),
                    (Side.U, 2, 1),
                    (Side.D, 0, 1),
                    (Side.D, 1, 0),
                    (Side.D, 1, 2),
                    (Side.D, 2, 1),
                    (Side.F, 1, 0),
                    (Side.F, 1, 2),
                    (Side.B, 1, 0),
                    (Side.B, 1, 2),
                ]
        result = 0
        for item in edges:
            if self.is_bad_edge(*item):
                result += 1

        return result

    def turn_back(self, side):
        f = self.faces[side]
        face_array = self.make_2d(side)

        rotated = zip(*face_array)[::-1]
        for i in xrange(self.size):
            for j in xrange(self.size):
                self.colors[self.coord(side, i, j)] = rotated[i][j]

        tmp = self.get_line(f.attached[0])
        self.assign_line(f.attached[1], f.attached[0])
        self.assign_line(f.attached[2], f.attached[1])
        self.assign_line(f.attached[3], f.attached[2])
        self.assign_line_values(tmp, f.attached[3])

    def turn_double(self, side):
        #TODO: non-lazy (and more optimal) implementation
        self.turn(side)
        self.turn(side)

    def cchar(self, c):
        table = {
                    Color.GREEN: Back.GREEN,
                    Color.RED: Back.RED,
                    Color.BLUE: Back.BLUE,
                    Color.ORANGE: Back.MAGENTA,
                    Color.WHITE: Back.WHITE,
                    Color.YELLOW: Back.YELLOW
                }
        return table[c] + "  " + Back.RESET

    def display(self):
        colorama.init(autoreset=True)

        indices = self.top_line(Side.U) + self.middle_line(Side.U) + self.bottom_line(Side.U)
        print "      {}{}{}\n      {}{}{}\n      {}{}{}".format(*[self.cchar(self.colors[c]) for c in indices])

        indices = self.top_line(Side.L) + self.top_line(Side.F) + self.top_line(Side.R) + self.top_line(Side.B)
        for c in indices:
            sys.stdout.write(self.cchar(self.colors[c]))
        print

        indices = self.middle_line(Side.L) + self.middle_line(Side.F) + self.middle_line(Side.R) + self.middle_line(Side.B)
        for c in indices:
            sys.stdout.write(self.cchar(self.colors[c]))
        print

        indices = self.bottom_line(Side.L) + self.bottom_line(Side.F) + self.bottom_line(Side.R) + self.bottom_line(Side.B)
        for c in indices:
            sys.stdout.write(self.cchar(self.colors[c]))
        print

        indices = self.top_line(Side.D) + self.middle_line(Side.D) + self.bottom_line(Side.D)
        print "      {}{}{}\n      {}{}{}\n      {}{}{}".format(*[self.cchar(self.colors[c]) for c in indices])

        colorama.deinit()

    def execute(self, scramble, reset=False, display=False):
        if reset: self.__init__()
        items = scramble.split(' ')
        for step in items:
            if len(step) == 1:
                side = getattr(Side, step)
                self.turn(side)
            elif len(step) == 2:
                side = getattr(Side, step[0])
                if (step[1] == "'"):
                    self.turn_back(side)
                elif (step[1] == "2"):
                    self.turn_double(side)
                else:
                    raise Exception("Invalid scramble!")
            else:
                raise Exception("Invalid scramble!")

        if display: self.display()

def gen_scramble(length=25):
    sides = ["F", "U", "R", "D", "L", "B"]
    modifiers = ["", "'", "2"]
    scramble = ""
    for i in xrange(25):
        scramble += random.choice(sides)
        scramble += random.choice(modifiers)
        scramble += " "
    return scramble[:-1]

def gen_known_scramble(bad_edge_count):
    colorama.init()
    c = Cube()
    iteration = 1
    while True:
        s = gen_scramble()
        c.execute(s)
        if c.bad_edge_count() == bad_edge_count:
            print Fore.WHITE + "[{}] ".format(iteration) + Fore.GREEN+ "{}".format(s)
            colorama.deinit()
            c.display()
            return s
        else:
            print Fore.WHITE + "[{}] ".format(iteration) + Fore.RED + "{}".format(s)
            iteration += 1

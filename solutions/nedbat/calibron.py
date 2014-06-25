"""
Calibron 12-block puzzle.
"""

import itertools
import math
import sys

TILES = [(32,11),(28,14),(21,18),(21,14),(28,6),(10,7),(21,14),(14,4),(17,14),(28,7),(21,18),(32,10)]
TRAYS = [(56,56)]

#TILES = [(5,2),(3,13),(2,11),(5,13),(7,2)]
#TILES = [(7,2),(5,5),(7,3),(5,17),(2,3),(2,13),(5,11),(2,2),(7,11),(3,5),(11,3)]
# too many solutions:
#TILES = [(13,2),(3,7),(11,3),(2,5),(11,5),(7,2),(2,3),(5,5),(5,3),(13,13),(2,2),(3,13),(7,11),(7,5)]

NAMES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TILES = [(NAMES[i], w, h) for i, (w, h) in enumerate(TILES)]


def possible_answer_sizes(tiles):
    """
    What are the possible sizes of a rectangle filled with `tiles`?
    """
    rect_area = sum(x*y for n,x,y in tiles)
    thickest_skinny = max(min([x,y]) for n,x,y in tiles)

    # Find possible answer sizes.
    for y in range(2, int(math.sqrt(rect_area))+1):
        x, remainder = divmod(rect_area, y)
        if remainder == 0:
            narrow_side = min([x, y])
            if narrow_side >= thickest_skinny:
                yield x, y


def xrange2d(x0, y0, x1, y1):
    """
    Produce a sequence of x,y pairs, the whole rectangle covering [x0,x1) x [y0,y1).
    """
    for y in xrange(y0, y1):
        for x in xrange(x0, x1):
            yield x, y


def orientations(w, h):
    """
    Yield different orientations of a tile sized `w` x `h`.
    """
    yield w, h
    if w != h:
        yield h, w


progress = itertools.count()

SMALL_STEP = 100000
LARGE_STEP = SMALL_STEP * 100

class Board(object):
    def __init__(self, w, h):
        self.w = w
        self.h = h

        # tiles is a list of 5-tuples: (name, x0, y0, x1, y1)
        self.tiles = []
        # The position of the first (raster-order) empty spot.
        self.empty_x, self.empty_y = 0, 0

    def __str__(self):
        return "<{}x{}: {}>".format(
            self.w, self.h,
            " ".join(
                "{}={:2d},{:2d}".format(name, x0, y0)
                for name, x0, y0, _, _ in self.tiles
            ),
        )

    def at(self, x, y):
        """
        What tile is at x, y?
        """
        for name, x0, y0, x1, y1 in self.tiles:
            if (x0 <= x < x1) and (y0 <= y < y1):
                return name
        return None

    def at_span(self, sx0, sy0, sx1):
        """
        What tile is in the span starting at sx0,sy0 going to sx1,sy0?
        """
        for name, x0, y0, x1, y1 in self.tiles:
            if y0 <= sy0 < y1:
                if not (x1 <= sx0 or sx1 <= x0):
                    return name
        return None

    def place_tile(self, name, w, h):
        """
        Place a tile on the board at the next spot.

        Try to place a tile sized w,h on the board at the next empty spot. If
        it fits, return a new board with the tile in place.  Otherwise, return
        None.
        """

        # Report some progress
        p = next(progress)
        if p % SMALL_STEP == 0:
            if p % LARGE_STEP == 0:
                print " {}M".format(p // 1000000)
                #print self.display()
            else:
                sys.stdout.write(".")
                sys.stdout.flush()

        # Does the tile even fit on the board?
        if self.empty_x + w > self.w:
            return None
        if self.empty_y + h > self.h:
            return None

        # To see if the tile can fit, we have to check if there are any occupied
        # squares where it's going.  Because of how we fill the board in raster
        # order, we only have to check the top row of squares.  If they are all
        # free, then all of the squares are free.
        if self.at_span(self.empty_x, self.empty_y, self.empty_x+w) is not None:
            return None

        # If this tile is going to cover the top-right corner, don't place it
        # if this tile's name is less than the tile in the top-left corner.
        # This eliminates a reflection of the board, which shouldn't count as
        # an answer anyway.
        if self.tiles:
            first_tile = self.tiles[0][0]
            if name < first_tile:
                if self.empty_y == 0 and self.empty_x+w == self.w:
                    return None

                # Also for the vertical reflection.
                if self.empty_x == 0 and self.empty_y+h == self.h:
                    return None

                # And for the lower-right corner.
                if self.empty_x+w == self.w and self.empty_y+h == self.h:
                    return None

        # Tile fits! Make a new board with the tile in place, and return it.
        new_board = Board(self.w, self.h)
        new_board.tiles = list(self.tiles)
        new_board.tiles.append((name, self.empty_x, self.empty_y, self.empty_x+w, self.empty_y+h))

        for probex, probey in xrange2d(0, self.empty_y, self.w, self.h):
            if new_board.at(probex, probey) is None:
                new_board.empty_x = probex
                new_board.empty_y = probey
                break
        else:
            new_board.empty_x = new_board.empty_y = None

        return new_board

    def display(self):
        """
        Make a string representing the board, for printing.
        """
        def empty(x, y):
            if (x, y) == (self.empty_x, self.empty_y):
                return "@"
            else:
                return "_"
        return "\n".join(
            "".join((self.at(x, y) or empty(x, y)) for x in xrange(self.w))
            for y in xrange(self.h)
        )


def solve_board(board, tiles):
    """
    Place `tiles` on `board`, yielding solved boards, if any.
    """
    if not tiles:
        assert board.empty_x is None and board.empty_x is None
        yield board
        return

    if 0:   # Change this to 1 to see progress happening.
        if len(tiles) < 2:
            print board.display()
            print

    for i, (name, w, h) in enumerate(tiles):
        for w, h in orientations(w, h):
            new_board = board.place_tile(name, w, h)
            if new_board:
                for answer in solve_board(new_board, tiles[:i]+tiles[i+1:]):
                    yield answer

if not TRAYS:
    TRAYS = list(possible_answer_sizes(TILES))

print TRAYS

for board_w, board_h in TRAYS:
    print "Looking for solutions on {}x{}".format(board_w, board_h)
    for board in solve_board(Board(board_w, board_h), TILES):
        if board is not None:
            print "\n\nSolution:"
            print board.display()

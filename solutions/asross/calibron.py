import copy
import random

def area(tile):
  return tile[0] * tile[1]

def factors(n):
  return [i for i in range(1,n+1) if n%i == 0]

assert(factors(1) == [1])
assert(factors(6) == [1,2,3,6])

def possible_dimensions(tiles):
  max_height = max(tile[0] for tile in tiles)
  max_width = max(tile[1] for tile in tiles)
  min_constraint = min(max_height, max_width)
  max_constraint = max(max_height, max_width)
  total_area = sum([area(tile) for tile in tiles])
  return [(f, total_area/f) for f in factors(total_area) if f >= max_constraint and total_area/f >= min_constraint and f >= total_area/f]

assert(possible_dimensions([(32, 11)]) == [(32, 11)])
assert(possible_dimensions([(32, 11), (32, 10), (28, 14),
                            (28,  7), (28,  6), (21, 18),
                            (21, 18), (21, 14), (21, 14),
                            (17, 14), (14,  4), (10,  7) ]) == [(56, 56), (64, 49), (98, 32), (112, 28)])

def x_capacity(x,y,board):
  for i, element in enumerate(board[y][x:]):
    if element is not None: return i
  return i+1

assert(x_capacity(0, 0, [[None,'x',None],[None,None,None],[None,None,None]]) == 1)
assert(x_capacity(0, 0, [[None,None,None],[None,None,None],[None,None,None]]) == 3)
assert(x_capacity(0, 0, [[None,None,None],['x',None,None],[None,None,None]]) == 3)
assert(x_capacity(0, 2, [[None,None,None],[None,None,None],[None,None,'x']]) == 2)
assert(x_capacity(2, 1, [['x','x','x'],
                         ['x','x',None],
                         [None,'x',None]]) == 1)

def y_capacity(x,y,board):
  return x_capacity(y,x,zip(*board))

assert(y_capacity(0, 0, [[None,None,None],[None,None,None],[None,None,None]]) == 3)
assert(y_capacity(0, 0, [[None,'x',None],[None,None,None],[None,None,None]]) == 3)
assert(y_capacity(0, 0, [[None,None,None],['x',None,None],[None,None,None]]) == 1)
assert(y_capacity(2, 0, [['x','x',None],['x','x',None],[None,None,None]]) == 3)
assert(y_capacity(1, 0, [[None,None,None],['x','x',None],[None,None,None]]) == 1)
assert(y_capacity(2, 1, [['x','x','x'],
                         ['x','x',None],
                         [None,'x',None]]) == 2)

def bottomleft_space(board):
  for j, row in enumerate(board):
    for i, el in enumerate(row):
      if el is None: return (i, j)

assert(bottomleft_space([[None,None,None],[None,None,None],[None,None,None]]) == (0, 0))
assert(bottomleft_space([['x','x',None],[None,None,None],[None,None,None]]) == (2, 0))
assert(bottomleft_space([['x','x','x'],['x',None,None],[None,None,None]]) == (1, 1))
assert(bottomleft_space([['x','x','x'],
                         ['x','x',None],
                         [None,'x',None]]) == (2, 1))

def place(l, w, x, y, board):
  """return a new state
  which is the result of placing the tile
  at (x,y)"""
  new_board = copy.deepcopy(board)
  for i in range(l):
    for j in range(w):
      if i == 0 or i == l-1 or j == 0 or j == w-1:
        new_board[y+i][x+j] = '.'
      else:
        new_board[y+i][x+j] = 'x'
  return new_board

assert(place(1, 2, 1, 0, [[None,None,None],[None,None,None],[None,None,None]]) == [[None, '.', '.'],[None,None,None],[None,None,None]])
assert(place(1, 1, 0, 0, [[None,None,None],[None,None,None],[None,None,None]]) == [['.',None,None],[None,None,None],[None,None,None]])
assert(place(2, 2, 0, 0, [[None,None,None],[None,None,None],[None,None,None]]) == [['.','.',None],['.','.',None],[None,None,None]])

def print_board(board):
  for row in board: print ' '.join([str(e or ' ') for e in row])

def solve_puzzle(tiles, board):
  if random.randint(0, 1000) == 1000: print '.'
  if not tiles:
    # if there are no tiles to place, we're done!
    return board
  else:
    # figure out where we ought to place the tile (bottom left space)
    # and how much room we have to the right and above
    x, y = bottomleft_space(board)
    max_width = x_capacity(x, y, board)
    max_length = y_capacity(x, y, board)

    # for each remaining tile
    for i, tile in enumerate(tiles):
      remaining_tiles = tiles[:i] + tiles[i+1:]
      # for both of its rotations
      for width, length in [tile, reversed(tile)]:
        if width <= max_width and length <= max_length:
          # place the tile and try to solve the puzzle from the resulting state
          new_board = place(length, width, x, y, board)
          result = solve_puzzle(remaining_tiles, new_board)
          if result:
            return result

    # if we can't solve the puzzle from this board configuration,
    # no matter which tile we place, then there are no solutions this way
    return None

def calibron(tiles):
  for dimensions in possible_dimensions(tiles):
    print "Trying to solve for", dimensions
    starting_board = [[None for i in range(dimensions[0])] for j in range(dimensions[1])]
    board = solve_puzzle(tiles, starting_board)
    if board:
      print "DONE!"
      print_board(board)
      break
    else:
      print "Unable to solve for", dimensions

calibron([
  (32, 11),
  (32, 10),
  (28, 14),
  (28, 7),
  (28, 6),
  (21, 18),
  (21, 18),
  (21, 14),
  (21, 14),
  (17, 14),
  (14, 4),
  (10, 7),
])

"""
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . x x x x x x x x . . x x x x x x x x x x x x .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . . . . . . . . . . . . . .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . . . . . . . . . . . . . .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. . . . . . . . . . . . . . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. . . . . . . . . . . . . . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x . . x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x . . x x x x x . . x x x x x x x x x x x x x x x x . . x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x . . x x x x x . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . x x x x x x x x x x x x .
. x x x x x . . x x x x x . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . x x x x x x x x x x x x .
. x x x x x . . x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x . . x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x . . x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x . . x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . x x x x x x x x x x x x .
. x x x x x . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x . . x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. x x x x x . . x x x x x x x x x x x x x x x x x x x . . x x x x x x x x x x x x x x x x x x x x x x x x x x .
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
"""

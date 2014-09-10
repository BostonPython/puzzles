from copy import deepcopy

SLIDER_1 = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1],
  [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
  [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
  [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

SLIDER_2 = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1],
  [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
  [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

def open_at(pin, slider):
    """return whether the slider has a free space at the pin position"""
    x, y = pin  # a pin is represented as an (x,y) pair -- y can change, x is fixed.
    coords, xoffset = slider # a slider is represented as coords (where it's open/closed) and xoffset (how far it's moved left/right)
    xx = x + xoffset
    return xx < 0 or xx >= len(coords[y]) or coords[y][xx] == 0

def all_open(pins, sliders):
    """return whether all sliders have free spaces at all pin positions"""
    for pin in pins:
        for slider in sliders:
            if not open_at(pin, slider):
                return False
    return True

def possible_moves(state):
    """return all states reachable by moving a pin or a slider one space"""
    sliders = state['sliders']
    pins = state['pins']
    result = []

    # this is a bit repetitive -- could theoretically generalize?
    for i, pin in enumerate(pins):
        x, y = pin
        for dy, direction in [(1, 'down'), (-1, 'up')]:
            new_pin = (x, y+dy)
            move = 'move pin {0} {1}'.format(i, direction)
            if all_open([new_pin], sliders):
                new_state = deepcopy(state)
                new_state['pins'][i] = new_pin
                result.append((move, new_state))

    for i, slider in enumerate(sliders):
        coords, offset = slider
        for dx, direction in [(1, 'left'), (-1, 'right')]:
            new_slider = (coords, offset+dx)
            move = 'move slider {0} {1}'.format(i, direction)
            if all_open(pins, [new_slider]):
                new_state = deepcopy(state)
                new_state['sliders'][i] = new_slider
                result.append((move, new_state))

    return result

# create a state (box) where the only legal move is to move
# the first pin down by 1
pin_box = { 'pins': [(1,1)], 'sliders': [([[1,1,1,1],
                                           [1,0,1,1],
                                           [1,0,1,1],
                                           [1,1,1,1]], 0),
                                       ([[1,1,1,1],
                                         [1,1,0,1],
                                         [1,1,0,1],
                                         [1,1,1,1]], 1)] }
pin_moves = possible_moves(pin_box)
move, new_box = pin_moves[0]

assert(len(pin_moves) == 1)
assert(move == 'move pin 0 down')
assert(new_box['pins'] == [(1,2)])
assert(new_box['sliders'][0] == pin_box['sliders'][0])
assert(new_box['sliders'][1] == pin_box['sliders'][1])

# create a box-state whose only legal move is to slide
# the first slider left by 1
slider_box = { 'pins': [(1,1)], 'sliders': [([[1,1,1,1],
                                              [1,0,0,1],
                                              [1,0,1,1],
                                              [1,1,1,1]], 0),
                                          ([[1,1,1,1],
                                            [1,1,0,1],
                                            [1,1,1,1],
                                            [1,1,1,1]], 1)] }
slider_moves = possible_moves(slider_box)
move, new_box = slider_moves[0]

assert(len(slider_moves) == 1)
assert(move == 'move slider 0 left')
assert(new_box['pins'] == slider_box['pins'])
assert(new_box['sliders'][0][0] == slider_box['sliders'][0][0])
assert(new_box['sliders'][0][1] == 1)
assert(new_box['sliders'][1] == slider_box['sliders'][1])

def completely_removed(slider):
    """return whether a slider has fully left the labybox"""
    coords, xoffset = slider
    return abs(xoffset) >= len(coords[0])

def reached_goal(state):
    """return whether we should consider a state as having reached the goal --
    in this case, whether any of the sliders have been completely removed"""
    return any(map(completely_removed, state['sliders']))

incomplete_box = { 'pins': [(1,1)], 'sliders': [([[1,1,1,1],
                                                  [1,0,0,1],
                                                  [1,0,1,1],
                                                  [1,1,1,1]], 0),
                                                ([[1,1,1,1],
                                                  [1,1,0,1],
                                                  [1,1,1,1],
                                                  [1,1,1,1]], 0)] }

complete_box = { 'pins': [(1,1)], 'sliders': [([[1,1,1,1],
                                                [1,0,0,1],
                                                [1,0,1,1],
                                                [1,1,1,1]], 4),
                                                         ([[1,1,1,1],
                                                           [1,1,0,1],
                                                           [1,1,1,1],
                                                           [1,1,1,1]], 0)] }

assert(not reached_goal(incomplete_box))
assert(reached_goal(complete_box))

def breadth_first_search(start_state):
    """search from the start state towards the goal state. return the shortest path to reach it"""
    frontier = [[('start', start_state)]] # list of paths through the state space, represented as (move, state) pairs.
    visited = set() # set of states we've already visited
    i = 0

    while frontier:
        path = frontier.pop(0) # consider the first path in the frontier, which is guaranteed to be the shortest
        state = path[-1][1] # look at the end of the path to get its current state

        i += 1
        if i % 250 == 0: print 'iterated {0} times, shortest path is {1}, frontier has {2} states'.format(i, len(path), len(frontier))

        if reached_goal(state): # if we've reached the goal, return the full path!
            return path
        elif str(state) in visited: # ignore already visited states
            continue
        else: # mark this state as visited and queue up its successors
            visited.add(str(state))
            for move, new_state in possible_moves(state):
                new_path = deepcopy(path)
                new_path.append((move, new_state))
                frontier.append(new_path)

# Actually solve the puzzle:
result = breadth_first_search({ 'sliders': [(SLIDER_1, 0), (SLIDER_2, 0)], 'pins': [(3,1), (9,1), (15,1)] })

for move, state in result:
    print move

"""
start
move pin 2 down
move pin 2 down
move slider 0 left
move slider 0 left
move pin 0 down
move pin 0 down
move pin 1 down
move pin 1 down
move pin 2 up
move pin 2 up
move slider 0 left
move slider 0 left
move pin 0 down
move pin 0 down
move slider 0 right
move slider 0 right
move pin 2 down
move pin 2 down
move slider 0 right
move slider 0 right
move pin 1 down
move pin 1 down
move pin 2 up
move pin 2 up
move slider 1 left
move slider 1 left
move pin 1 up
move pin 1 up
move pin 2 down
move pin 2 down
move slider 0 left
move slider 0 left
move pin 2 up
move pin 2 up
move slider 0 left
move slider 0 left
move pin 1 up
move pin 1 up
move pin 2 down
move pin 2 down
move slider 1 left
move slider 1 left
move pin 2 down
move pin 2 down
move slider 1 right
move slider 1 right
move pin 1 down
move pin 1 down
move slider 0 right
move slider 0 right
move slider 0 right
move slider 0 right
move pin 1 down
move pin 1 down
move slider 1 right
move slider 1 right
move pin 1 up
move pin 1 up
move slider 0 left
move slider 0 left
move slider 0 left
move slider 0 left
move pin 0 up
move pin 0 up
move slider 0 right
move slider 0 right
move pin 0 up
move pin 0 up
move slider 0 left
move slider 0 left
move pin 1 up
move pin 1 up
move slider 1 right
move slider 1 right
move pin 2 up
move pin 2 up
move pin 2 up
move pin 2 up
move slider 1 right
move slider 1 right
move pin 1 down
move pin 1 down
move slider 0 right
move slider 0 right
move slider 1 left
move slider 1 left
move pin 2 down
move pin 2 down
move slider 0 right
move slider 0 right
move pin 1 down
move pin 1 down
move slider 0 left
move slider 0 left
move pin 2 up
move pin 2 up
move slider 0 left
move slider 0 left
move slider 1 right
move slider 1 right
move pin 2 down
move pin 2 down
move pin 2 down
move pin 2 down
move slider 0 right
move slider 0 right
move slider 0 right
move slider 0 right
move slider 1 right
move slider 1 right
move pin 1 up
move pin 1 up
move slider 0 left
move slider 0 left
move slider 0 left
move slider 0 left
move pin 1 up
move pin 1 up
move pin 2 up
move pin 2 up
move pin 2 up
move pin 2 up
move slider 1 right
move slider 1 right
move slider 1 right
move slider 1 right
move pin 2 down
move pin 2 down
move slider 1 left
move slider 1 left
move pin 2 down
move pin 2 down
move slider 1 right
move slider 1 right
move slider 1 right
move slider 1 right
move pin 2 up
move pin 2 up
move pin 2 up
move pin 2 up
move slider 1 right
move slider 1 right
move slider 1 right
move slider 1 right
move slider 1 right
move slider 1 right
move slider 1 right
move slider 1 right
move slider 1 right
move slider 1 right
move slider 1 right
"""

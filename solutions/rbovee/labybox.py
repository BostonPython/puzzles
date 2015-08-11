from heapq import heappush, heappop
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation


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

S1 = np.array(SLIDER_1)
S2 = np.array(SLIDER_2)

# multiply S1 by 0.5 to make the two sliders different colors
# when plotted in matplotlib -- can't use *= b/c dtype doesn't change
S1 = S1 * 0.5

# start off with pins and sliders at +5
OFFSET = 5

# fixed locations of the pins horizontally
PX = OFFSET + np.array([3, 9, 15])

# create one variable to hold locations of everything
START_STATE = tuple([OFFSET] + [OFFSET] + [1, 1, 1])

# for convenience, give names to the values in state for debugging
STATE_NAMES = ['slid top', 'slid bottom', 'pin 1', 'pin 2', 'pin 3']


def spots_blocked(state, debug=False):
    """
    Determine if a given a slider and pin state is physically feasible.
    Can also be used to make plots of different states using the debug
    parameter.

    Parameters
    ----------
    state: tuple
        The state of the sliders and pins in the puzzle.
    debug: bool
        If a matplotlib plot of the state should be returned instead.

    Returns
    -------
    bool
        True if the given state is physically possible, False otherwise.

    Example
    -------
    Test the starting position shown in the example
    >>> spots_blocked((5, 5, 1, 1, 1)) == 0
    True

    Test one with the top block moved 2 to the left
    >>> spots_blocked((3, 5, 1, 1, 1)) == 0
    True

    Test with the final position
    >>> spots_blocked((3, 19, 1, 1, 1)) == 0
    True

    Test with an obviously impossible position
    >>> spots_blocked((5, 5, 0, 0, 0)) != 0
    True
    """
    s1_offset, s2_offset, *py = state

    puzlen = S1.shape[1]
    z = np.zeros((S1.shape[0], 2 * puzlen))
    z[:, s1_offset:s1_offset + puzlen] += S1
    z[:, s2_offset:s2_offset + puzlen] += S2

    if debug:
        a = plt.imshow(z, cmap='afmhot_r', interpolation='nearest')
        b = plt.plot(PX, py, 'bo')[0]
        return (a, b)

    return sum(z[y, x] for x, y in zip(PX, py)) != 0



def plot_state(state):
    """
    Wrapper for `spots_blocked` to plot states.
    """
    plt.show(spots_blocked(state, True))


def pos_moves(state, as_text=False):
    """
    Return puzzle states that are accessible from the current puzzle state.

    Parameters
    ----------
    state: tuple
        Represention of a puzzle state, as in spots_blocked.
    as_text: bool
        Should text descriptions be returned instead of states.
        For debugging.

    Returns
    -------
    generator
        returns tuples indicating possible neighboring states.

    Examples
    --------
    >>> list(pos_moves((5, 5, 1, 1, 1)))
    [(5, 5, 1, 1, 2)]
    """
    for i, s in enumerate(state):
        # don't keep track of pins that have exited bottom slider
        if i > 1:
            if state[1] > PX[i - 2]:
                continue

        new_state = list(state)
        new_state[i] = s + 1
        if not spots_blocked(new_state):
            if as_text:
                yield STATE_NAMES[i], 1
            else:
                yield tuple(new_state)
        new_state[i] = s - 1
        if not spots_blocked(new_state):
            if as_text:
                yield STATE_NAMES[i], -1
            else:
                yield tuple(new_state)


def move_to_end(start_state=START_STATE, s2_end=23):
    """
    Given a starting puzzle state, uses the A* pathfinding algorithm
    to find a solution to the "open bottom" puzzle state.

    Parameters
    ----------
    start_state: tuple
        Representation of the initial positions of the sliders and pins.
    s2_end: int
        Bottom slider position required to open the puzzle.

    Returns
    -------
    list
        List of states travelling that must be travered on path to end.
    """
    def to_heap_tuple(state):
        return (s2_end - state[1], state)

    visited = {start_state: None}
    to_visit = []
    heappush(to_visit, to_heap_tuple(start_state))

    while len(to_visit) > 0:
        current = heappop(to_visit)[1]

        if to_heap_tuple(current)[0] == 0:
            path = []
            while current in visited:
                path.append(current)
                current = visited[current]
            return list(reversed(path))

        for neighbor in pos_moves(current):
            if neighbor in visited:
                continue
            elif to_heap_tuple(neighbor) not in to_visit:
                heappush(to_visit, to_heap_tuple(neighbor))
            visited[neighbor] = current
    return []


def animate_solution(start_state=START_STATE):
    """
    Plots the puzzle being solved using matplotlib.animation.
    """
    fig = plt.figure()
    ims = []
    for state in move_to_end(start_state):
        ims.append(spots_blocked(state, True))
    a = ArtistAnimation(fig, ims, interval=200, repeat_delay=200)
    plt.show()


def list_moves(state_list=None):
    """
    Returns a list of human readable strings describing how to solve
    a puzzle given a list of states used in that solution.

    Basically, takes input of moves_to_end and returns it in a
    human-readable format.

    Used to solve questions 1 and 2 of the Boston Python challenge.
    """
    if state_list is None:
        state_list = move_to_end(START_STATE)

    prev_state = state_list[0]
    prev_move_axis = None
    move_list = []

    for state in state_list:
        # get the index of what changed in the state with some numpy
        move_axis = np.sum(np.abs(np.array(state) - \
                                  np.array(prev_state)) * np.arange(5))

        if move_axis != prev_move_axis and prev_move_axis is not None:
            # figure out which direction the axis that moved, moved
            if np.sign(np.sum(np.array(state) - np.array(prev_state))) > 0:
                if move_axis < 2:
                    move_dir = 'right'
                else:
                    move_dir = 'down'
            else:
                if move_axis < 2:
                    move_dir = 'left'
                else:
                    move_dir = 'up'

            move_list.append(STATE_NAMES[move_axis] + ' ' + move_dir)

        prev_state = state
        prev_move_axis = move_axis

    return move_list


def pin_positions_with_hardness():
    """
    Given all possible starting locations of pins in the puzzle,
    return a list of the number of moves required to solve them.

    Solves problem 3 of the Boston Python challenge.
    """
    # list the possible starting pin positions
    pin1 = [1, 3, 5]
    pin2 = [1, 3, 4, 5]
    pin3 = [1, 2, 3, 5]

    # try out each possible combination and count how many moves to solve
    position_list = []
    for pin_pos in product(pin1, pin2, pin3):
        start_state = tuple([OFFSET] + [OFFSET] + list(pin_pos))
        state_list = move_to_end(start_state)
        position_list.append((len(list_moves(state_list)), pin_pos))
    return sorted(position_list)

if __name__ == '__main__':
    # print answers to the Boston Python challenges
    print(list_moves())

    print(len(list_moves()))

    pin_positions = pin_positions_with_hardness()
    # hardest pin position
    print(pin_positions[-1][1])
    # is it unique?
    print(pin_positions[-1][1] != pin_positions[-2][1])

    # also, run all the tests
    import doctest
    doctest.testmod()

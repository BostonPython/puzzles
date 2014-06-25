"""
twitter_pudddle.py

Edward J. Stronge - ejstronge@gmail.com

Solution to the twitter_puddle puzzle for the Boston Python User Group meeting.
"""
from collections import namedtuple

WallParams = namedtuple('WallParams', 'height length')


def find_puddle_volume(column_heights):
    """
    Given a sequence of heights of a bar graph, calculates
    the volume of liquid that would be held by the bar
    graph if liquid were poured onto the bar graph colummns
    (see http://programmingpraxis.com/2013/11/15/twitter-puddle)
    """
    puddle_volume = 0

    left_wall_heights_and_lengths = []
    prev_height = None
    plane_length = 1  # Number of columns with the same height
    for curr_height in column_heights:

        if prev_height is None:
            prev_height = curr_height
            continue

        if curr_height < prev_height:
            # As we descend, keep track of what we've filled in to the left
            left_wall_heights_and_lengths.append(WallParams(prev_height, plane_length))
            prev_height = curr_height

        elif curr_height > prev_height:
            # We're ascending. Need to look back to the nearest left
            # wall and add water until we've filled as much as we can

            # If there's no wall to our left, we continue. We also need
            # to reset plane_length; we won't start caring about this
            # until we've got a wall to our left.
            if not left_wall_heights_and_lengths:
                prev_height = curr_height
                plane_length = 1
                continue
            fill_level = prev_height
            while curr_height >= left_wall_heights_and_lengths[-1].height:
                # Check our left wall heights to determine how much water
                # to add. We're essentially 'leveling out' the space to
                # the left of the current column, forming a plane
                stack_height, stack_plane_length = left_wall_heights_and_lengths.pop()
                puddle_volume += (stack_height - fill_level) * plane_length
                # Now we've added water up to stack_height. Our 'plane'
                # is now a bit longer and has a new height.
                fill_level = stack_height
                plane_length += stack_plane_length
                if not left_wall_heights_and_lengths:
                    break
            # Check if we can add water up to curr_height. The alternative
            # is that there's no more left wall to retain the water we'd add;
            # in this case, we move on.
            if left_wall_heights_and_lengths:
                puddle_volume += (curr_height - fill_level) * plane_length
                plane_length += 1
            prev_height = curr_height

        else:  # curr_height == prev_height
            plane_length += 1
    return puddle_volume

#!/usr/bin/env python3
# Copyright 2014 Brett Smith <brettcsmith@brettcsmith.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools
import unittest

class Puddle:
    def __init__(self, volume, start_index, end_index):
        self.volume = volume
        self.start_index = start_index
        self.end_index = end_index

    def __repr__(self):
        return "Puddle({}, {}, {})".format(
            self.volume, self.start_index, self.end_index)

    def __lt__(self, other):
        return self.volume < other.volume


class Ledge:
    def __init__(self, start_index, height, left_volume=0):
        self.start_index = start_index
        self.end_index = start_index
        self.height = height
        self.left_volume = left_volume

    def __repr__(self):
        return "Ledge({}, {}, {})".format(
            self.start_index, self.height, self.left_volume)

    def puddle_from(self, wall, floor):
        height_diff = min(self.height, wall.height) - floor.height
        assert height_diff >= 0
        width = self.start_index - wall.end_index - 1
        self.left_volume += (height_diff * width) + floor.left_volume
        return Puddle(self.left_volume, wall.end_index + 1, self.start_index)


class LedgeStack:
    EMPTY_PUDDLE = Puddle(0, None, None)

    def __init__(self, heights):
        self.heights = enumerate(heights)
        self.stack = [Ledge(*next(self.heights))]

    def fill_puddle_to(self, new_ledge):
        assert self.stack[-1].height < new_ledge.height
        puddle = self.EMPTY_PUDDLE
        floor = self.stack.pop()
        while self.stack:
            puddle = new_ledge.puddle_from(self.stack[-1], floor)
            if self.stack[-1].height < new_ledge.height:
                floor = self.stack.pop()
            else:
                break
        self.stack.append(new_ledge)
        return puddle

    def puddles(self):
        for index, height in self.heights:
            prev_height = self.stack[-1].height
            new_ledge = Ledge(index, height)
            if height < prev_height:
                self.stack.append(new_ledge)
            elif height == prev_height:
                self.stack[-1].end_index = index
            else:
                yield self.fill_puddle_to(new_ledge)


def biggest_puddle(heights):
    stack = LedgeStack(heights)
    try:
        return max(stack.puddles())
    except TypeError:  # No puddles
        return stack.EMPTY_PUDDLE

class MeasurePuddleTest(unittest.TestCase):
    EXAMPLE = [2, 5, 1, 2, 3, 4, 7, 7, 6]
    COMB = [3, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 3]
    UP_SLOPE = range(1, 5)
    DOWN_SLOPE = range(4, -1, -1)

    def test_example(self):
        puddle = biggest_puddle(self.EXAMPLE)
        self.assertEqual(puddle.start_index, 2)
        self.assertEqual(puddle.end_index, 6)
        self.assertEqual(puddle.volume, 10)

    def test_reversed_example(self):
        puddle = biggest_puddle(reversed(self.EXAMPLE))
        self.assertEqual(puddle.start_index, 3)
        self.assertEqual(puddle.end_index, 7)
        self.assertEqual(puddle.volume, 10)

    def test_comb_unbounded(self):
        puddle = biggest_puddle(self.COMB[:-1])
        self.assertEqual(puddle.start_index, 4)
        self.assertEqual(puddle.end_index, 7)
        self.assertEqual(puddle.volume, 3)

    def test_comb_bounded(self):
        puddle = biggest_puddle(self.COMB)
        self.assertEqual(puddle.start_index, 1)
        self.assertEqual(puddle.end_index, 11)
        self.assertEqual(puddle.volume, 16)

    def test_pool(self):
        puddle = biggest_puddle(itertools.chain(self.DOWN_SLOPE, self.UP_SLOPE))
        self.assertEqual(puddle.start_index, 1)
        self.assertEqual(puddle.end_index, 8)
        self.assertEqual(puddle.volume, 16)

    def test_roof(self):
        puddle = biggest_puddle(itertools.chain(self.UP_SLOPE, self.DOWN_SLOPE))
        self.assertEqual(puddle.volume, 0)


if __name__ == '__main__':
    unittest.main()

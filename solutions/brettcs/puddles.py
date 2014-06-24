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

class EndOfPuddle(Exception):
    pass


class Puddle:
    def __init__(self, wall_height, wall_index):
        self.wall_height = wall_height
        self._start_index = wall_index + 1
        self.insides = []

    def _new_end_wall(self, height):
        try:
            self.insides.append(self.end_wall_height)
        except AttributeError:
            pass
        self.end_wall_height = height
        self._end_index = len(self.insides)

    def fits_inside(self, height):
        if not self.insides:
            return True
        try:
            return height <= self.end_wall_height
        except AttributeError:
            return height < max(self.insides)

    def add(self, height):
        if height >= self.wall_height:
            self._new_end_wall(height)
            raise EndOfPuddle()
        elif self.fits_inside(height):
            self.insides.append(height)
        else:
            self._new_end_wall(height)

    def _start_offset(self):
        offset = 0
        for height in self.insides:
            if height < self.end_wall_height:
                break
            offset += 1
        return offset

    @property
    def start_index(self):
        return self._start_index + self._start_offset()

    @property
    def end_index(self):
        return self._start_index + self._end_index

    @property
    def volume(self):
        try:
            wall_height = min(self.wall_height, self.end_wall_height)
        except AttributeError:  # No end wall yet
            return 0
        else:
            return sum(wall_height - height for height in
                       self.insides[self._start_offset():self._end_index])

    def __lt__(self, other):
        return self.volume < other.volume


def biggest_puddle(heights):
    heights = enumerate(heights)
    first_index, first_height = next(heights)
    biggest_puddle = Puddle(first_height, first_index)
    puddle = biggest_puddle
    for index, height in heights:
        try:
            puddle.add(height)
        except EndOfPuddle:
            biggest_puddle = max(puddle, biggest_puddle)
            puddle = Puddle(height, index)
    return max(puddle, biggest_puddle)


class PuddleTest(unittest.TestCase):
    def test_basic_puddle(self):
        puddle = Puddle(2, 0)
        puddle.add(1)
        self.assertRaises(EndOfPuddle, puddle.add, 2)
        self.assertEqual(puddle.start_index, 1)
        self.assertEqual(puddle.end_index, 2)
        self.assertEqual(puddle.volume, 1)

    def test_basic_running_bound_puddle(self):
        puddle = Puddle(3, 0)
        puddle.add(1)
        puddle.add(2)
        self.assertEqual(puddle.start_index, 1)
        self.assertEqual(puddle.end_index, 2)
        self.assertEqual(puddle.volume, 1)

    def test_example_puddle(self):
        puddle = Puddle(5, 1)
        for height in range(1, 5):
            puddle.add(height)
        self.assertRaises(EndOfPuddle, puddle.add, 7)
        self.assertEqual(puddle.volume, 10)
        self.assertEqual(puddle.start_index, 2)
        self.assertEqual(puddle.end_index, 6)

    def test_example_puddle_reversed(self):
        puddle = Puddle(7, 2)
        for height in range(4, 0, -1):
            puddle.add(height)
        puddle.add(5)
        puddle.add(2)
        self.assertEqual(puddle.volume, 10)
        self.assertEqual(puddle.start_index, 3)
        self.assertEqual(puddle.end_index, 7)

    def test_w_puddle(self):
        puddle = Puddle(4, 0)
        for height in [1, 2, 1, 3]:
            puddle.add(height)
        self.assertEqual(puddle.start_index, 1)
        self.assertEqual(puddle.end_index, 4)
        self.assertEqual(puddle.volume, 5)

    def test_ww_puddle(self):
        puddle = Puddle(4, 0)
        for height in [1, 3, 1, 3]:
            puddle.add(height)
        self.assertEqual(puddle.start_index, 1)
        self.assertEqual(puddle.end_index, 2)
        self.assertEqual(puddle.volume, 2)

    def test_staggered_puddle(self):
        puddle = Puddle(4, 0)
        for height in [3, 1, 3]:
            puddle.add(height)
        self.assertEqual(puddle.start_index, 2)
        self.assertEqual(puddle.end_index, 3)
        self.assertEqual(puddle.volume, 2)

    def test_no_puddle(self):
        puddle = Puddle(2, 0)
        self.assertRaises(EndOfPuddle, puddle.add, 4)
        self.assertEqual(puddle.volume, 0)

    def test_no_puddle_yet(self):
        puddle = Puddle(4, 0)
        for height in range(3, -1, -1):
            puddle.add(height)
        self.assertEqual(puddle.volume, 0)

    def test_max_puddle(self):
        small_puddle = Puddle(5, 0)
        small_puddle.add(3)
        small_puddle.add(4)
        big_puddle = Puddle(5, 0)
        big_puddle.add(0)
        big_puddle.add(4)
        self.assertIs(big_puddle, max(small_puddle, big_puddle))


class MeasurePuddleTest(unittest.TestCase):
    EXAMPLE = [2, 5, 1, 2, 3, 4, 7, 7, 6]
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

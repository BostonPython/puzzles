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
        self.start_index = wall_index + 1
        self.end_index = self.start_index
        self.volume = 0

    def add(self, height):
        height_diff = self.wall_height - height
        if height_diff > 0:
            self.volume += height_diff
            self.end_index += 1
        else:
            raise EndOfPuddle()

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
    return biggest_puddle


class PuddleTest(unittest.TestCase):
    def test_basic_puddle(self):
        puddle = Puddle(2, 0)
        puddle.add(1)
        self.assertEqual(puddle.start_index, 1)
        self.assertEqual(puddle.volume, 1)
        self.assertRaises(EndOfPuddle, puddle.add, 2)
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

    def test_no_puddle(self):
        puddle = Puddle(2, 0)
        self.assertRaises(EndOfPuddle, puddle.add, 4)
        self.assertEqual(puddle.volume, 0)

    def test_max_puddle(self):
        small_puddle = Puddle(5, 0)
        small_puddle.add(4)
        big_puddle = Puddle(5, 0)
        big_puddle.add(0)
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

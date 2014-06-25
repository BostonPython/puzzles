"""
Barry Flinn
barry@flinn.me

Solution to the hexwords puzzle for Boston Python

Inspired by Jessica McKellar's Scrabble cheating strategy.  :-)

The best dictionary to use seems to be '/usr/share/dict/words'
"""

import sys
import re

if len(sys.argv) < 2:
    print("Please supply a dictionary file")
    exit(1)

filename = sys.argv[1]

tester = re.compile("^[a-fA-F]+$")
longest_hexword = ""
longest_hexword_value = 0

try:
    with open(filename, "r") as f:
        for line in f:
            test_word = line.strip()
            match = tester.match(test_word)
            if match:
                hexword = match.group()
                hexword_value = int(hexword, 16)
                if hexword_value > longest_hexword_value:
                    longest_hexword = hexword
                    longest_hexword_value = hexword_value

    print("****")
    print(longest_hexword)
    print(longest_hexword_value)

except EnvironmentError:
    print("Oops, can't find %s." % filename)
    exit(1)

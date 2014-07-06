#!/usr/bin/env python

# Josh McGrath
# Solution to http://puzzles.bostonpython.com/poetry.html
# Tested with: Python 2.7.6

# You find yourself in a dark, wet cave. There is a heavy door with a mushroom growing on it. (Or is that an ear?)

# Nailed to the door is a poem by Emily Dickinson:

poem='''a narrow fellow in the grass
occasionally rides;
you may have met him, did you not,
his notice sudden is.

the grass divides as with a comb,
a spotted shaft is seen;
and then it closes at your feet
and opens further on.

he likes a boggy acre,
a floor too cool for corn.
yet when a child, and barefoot,
i more than once, at morn,

have passed, i thought, a whip-lash
unbraiding in the sun,
when, stooping to secure it,
it wrinkled, and was gone.

several of nature's people
i know, and they know me;
i feel for them a transport
of cordiality;

but never met this fellow,
attended or alone,
without a tighter breathing,
and zero at the bone.'''

# Below the poem is a riddle:

# say([56,38,44,56,29])

# And below that, a note:

# # hint: 'zebra' = [1,56,7,29,42]

# 1) Write a program that solves the riddle.

from collections import Counter
from sets import Set

# returns a counter containing counts of each alphabetic character
# in the string
def count_alpha_chars (str):
    def red_fn (accum, char):
        if char.isalpha():
            accum[char] += 1
        return accum
    return reduce (red_fn, str, Counter())

# given a list of values, returns the unique values
def unique_values (itr):
    counter = Counter ()
    for k in itr:
        counter[k] += 1
    return filter (lambda x: counter[x] == 1, list(counter))

# given a counter, returns a dictionary mapping unique
# counts to their keys
def unique_counts (ctr):
    # unique counts
    ucs = Set (unique_values(ctr.values()))
    def red_fn (accum, k):
        if ctr[k] in ucs:
            accum[ctr[k]] = k
        return accum
    return reduce (red_fn, ctr, {})

def say (enc_msg, text):
    ucs = unique_counts (count_alpha_chars (text))
    return reduce (lambda dec_msg, enc_chr: dec_msg + ucs[enc_chr], enc_msg, '')

def encode (s, counts):
    return reduce (lambda accum, c: accum + [counts[c]], s, [])

# What do you say?
print say ([56,38,44,56,29], poem)

counts = count_alpha_chars (poem)
assert (encode ("zebra", counts) == [1,56,7,29,42])

# 2) Write a program that shows the mapping for all letters.
print counts

# Which letters are available, i.e. have unique non-zero values?
ucs = unique_counts (counts)
avail_letters = ucs.values()
print avail_letters

# 3) Write a program that generates all such riddles based on this poem.

# dict keys and values must form a bijection
def invert_dict (d):
    inv_d = {}
    for k in d:
        inv_d[d[k]] = k
    return inv_d

def all_riddles (text, words_file):
    avail_letters_set = Set (avail_letters)
    riddles = []
    inv_ucs = invert_dict (ucs)
    with open(words_file) as f:
        for l in f:
            # remove newline char
            l = l[:-1].lower()
            if Set (l) <= avail_letters_set:
                riddles.append(encode (l, inv_ucs))
    return riddles

# What is the longest word that is a solution to a riddle based on this poem? (useful: Words (Unix))

riddles = all_riddles (poem, '/usr/share/dict/words')
print say (max (riddles), poem)

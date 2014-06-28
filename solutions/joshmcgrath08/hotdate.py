#!/usr/bin/env python

# Josh McGrath
# Solution to http://puzzles.bostonpython.com/hotdate.html
# Tested with: Python 2.7.6

# Consider these base-10 digits: 123456789. If you insert spaces between them, you get various sequences of numbers:

# 1 2 3 4 5 6 7 8 9
# 12 3 4 5 67 8 9
# 1 2 34 5 6 7 89
# 12 34 56 78 9
# 1 23456 78 9
# 12345 6789
# etc.

from itertools import *

# 1) Write a program that generates all possible combinations of those digits.

digits = map (str, range (1, 10))

# alternate the elements of two lists, until both lists exhausted
def alternate (l1, l2):
    len_l1 = len (l1)
    len_l2 = len (l2)
    l = []
    for i in range (max (len_l1, len_l2)):
        if i < len_l1:
            l.append(l1[i])
        if i < len_l2:
            l.append(l2[i])
    return l

assert (alternate ([], []) == [])
assert (alternate ([1, 2, 3], [4, 5]) == [1, 4, 2, 5, 3])
assert (alternate ([4, 5], [1, 2, 3]) == [4, 1, 5, 2, 3])

# given a list of strings and an iterator to strings, return
# an iterator to strings where a value from the iterator arg is
# inserted between each adjacent pairs of elements in the list arg
def itr_intersperse (l, itr):
    for x in product (itr, repeat=len (l) - 1):
        yield ''.join(alternate (l, x))

# # How many are there?

def itr_len (itr):
    c = 0
    for i in itr:
        c += 1
    return c

print itr_len (itr_intersperse (digits, ['', ' ']))

# Now let's insert a maximum of 8 addition or subtraction operators between the numbers, like this:

# 1+2+3+4+5+6+7-8+9
# 12-3+4+5-67-8+9
# 1+2+34+5-6-7-89
# 12-34+56+78+9
# 1+23456-78-9
# 12345+6789
# etc.

# Notice that those arithmetic expressions equate to different values:

# 1+2+3+4+5+6+7-8+9 = 29
# 12-3+4+5-67-8+9 = -48
# 1+2+34+5-6-7-89 = -60
# 12-34+56+78+9 = 121
# 1+23456-78-9 = 23370
# 12345+6789 = 19134
# etc.

# 2) Write a program that generates all possible expressions in this way.

# returns an iterator to expressions that sum to n
def expr_sum (n):
    return ifilter (lambda x: eval(x) == n, itr_intersperse (digits, ['', '+', '-']))

# How many sum to 100?
print itr_len (expr_sum (100))

# 3) Write a program that finds all such expressions for any sum.

# Which sum is the most popular, i.e. has the most expressions?
sums = map (eval, itr_intersperse (digits, ['', '+', '-']))

from collections import Counter

sum_counter = Counter ()
for s in sums:
    sum_counter[s] += 1

print sum_counter.most_common(1)[0][0]

# 4) Bonus: We can haz pretty data viz?

# Like how about a histogram of the number of expressions with sums from -23456788 to 123456789. (A log scale might help. Maybe binning, too.)

from matplotlib.pyplot import hist, show, bar

show (hist (sums, range = (-23456788, 123456789), bins = 50, normed = True, log = True))

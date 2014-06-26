#              _ _
#             |7 7|_
#    _        |    6|
#   |5|~ ~ ~ _|     |
#   | |~ ~ _|4      |
#  _| |~ _|3        |
# |2  |_|2          |
# |____1____________|
#  0 1 2 3 4 5 6 7 8
#######################

def twitter_puddle1(land):
    """quadratic-time solution to the twitter puddle problem"""
    volume = 0

    for x in range(1, len(land)-1):
        lowest_wall = min(max(land[:x]), max(land[x+1:]))
        if lowest_wall > land[x]:
            volume += lowest_wall - land[x]

    return volume

def twitter_puddle2(land):
    """linear time (one-pass) solution,
    courtesy of http://qandwhat.apps.runkite.com/i-failed-a-twitter-interview/"""
    volume = 0
    left_max = 0
    right_max = 0
    left = 0
    right = len(land) - 1

    while left < right:
      left_max = max(left_max, land[left])
      right_max = max(right_max, land[right])
      if left_max >= right_max:
        volume += right_max - land[right]
        right -= 1
      else:
        volume += left_max - land[left]
        left += 1

    return volume

assert(twitter_puddle1([]) == 0)
assert(twitter_puddle1([5]) == 0)
assert(twitter_puddle1([5, 5]) == 0)
assert(twitter_puddle1([5, 0, 5]) == 5)
assert(twitter_puddle1([2, 5, 1, 2, 3, 4, 7, 7, 6]) == 10)
assert(twitter_puddle1([2, 5, 1, 2, 3, 4, 7, 7, 6, 8]) == 11)

assert(twitter_puddle2([]) == 0)
assert(twitter_puddle2([5]) == 0)
assert(twitter_puddle2([5, 5]) == 0)
assert(twitter_puddle2([5, 0, 5]) == 5)
assert(twitter_puddle2([2, 5, 1, 2, 3, 4, 7, 7, 6]) == 10)
assert(twitter_puddle2([2, 5, 1, 2, 3, 4, 7, 7, 6, 8]) == 11)

print 'tests pass'

import timeit

for i in range(5):
  test_list = [5,3,2,4,5]*(i*20)
  print 'L =', len(test_list)
  print '  1:', timeit.timeit("twitter_puddle1(" + str(test_list) + ")", setup='from __main__ import twitter_puddle1', number=1000), 'seconds'
  print '  2:', timeit.timeit("twitter_puddle2(" + str(test_list) + ")", setup='from __main__ import twitter_puddle2', number=1000), 'seconds'

"""
L = 0
  1: 0.000443935394287 seconds
  2: 0.000288963317871 seconds
L = 100
  1: 0.313441991806 seconds
  2: 0.0417368412018 seconds
L = 200
  1: 1.10613894463 seconds
  2: 0.08522605896 seconds
L = 300
  1: 2.26546788216 seconds
  2: 0.125725030899 seconds
L = 400
  1: 3.91308808327 seconds
  2: 0.16819691658 seconds
"""

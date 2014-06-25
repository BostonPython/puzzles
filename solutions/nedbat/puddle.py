# Solutions to http://puzzles.bostonpython.com/puddle.html

#
# A one-pass solution
#

def puddle_fast(heights):
    """How much water collects in the puddles?"""
    last = 0
    water = 0
    slabs = []

    for x, h in enumerate(heights):
        # Make sure our slabs bookkeeping is large enough.
        if h > len(slabs):
            slabs.extend([None] * (h - len(slabs)))
        # Sloping down: start some new slabs.
        for s in range(h, last):
            assert slabs[s] is None
            slabs[s] = x
        # Sloping up: finish some slabs.
        for s in range(last, h):
            if slabs[s] is not None:
                water += x - slabs[s]
                slabs[s] = None

        last = h

    return water

print "Fast:", puddle_fast([2,5,1,2,3,4,7,7,6])


#
# A compact min-max solution
#

def puddle_minmax(heights):
    water = 0
    for x in range(len(heights)):
        cliff_left = max(heights[:x]+[0])
        cliff_right = max(heights[x+1:]+[0])
        water += max(0, min(cliff_left, cliff_right) - heights[x])
    return water

print "Min-max:", puddle_minmax([2,5,1,2,3,4,7,7,6])


print "Five random tests:"
import random
for i in range(5):
    heights = [random.randint(1,20) for _ in range(random.randint(20,40))]
    print heights
    print puddle_fast(heights)
    print puddle_minmax(heights)

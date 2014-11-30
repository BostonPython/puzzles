#!usr/bin/env python

# This is a universal brute force solution to the coin-passing problem (N/D 3) by J.D.R. Kramer in Puzzle Corner, Tech Review, Nov/Dec 2014, p. 62
# http://www.technologyreview.com/sites/default/files/magazine/mitnews/puzzlecorner/ND14MITPuzzleCorner.pdf
#
# John Bohannon, Cambridge, Massachusetts 6 Nov 2014
# john@johnbohannon.org

def redistribute(n, start, target_ratio):
    '''This function redistributes the wealth'''
    some_men = [ (start - i) for i in range(n) ]
    # let's keep a copy of the initial state
    some_men_initial = [i for i in some_men]
    count = 0
    # let's play it safe with a time limit
    while count < (n*start):
        giver = count % n
        receiver = (count + 1) % n
        if some_men[giver] < (count + 1):
            # redistribution complete, so let's test it
            if test((some_men, n, target_ratio)):
                # this one passed the test!
                print "(%s,%s) works for %s:" %(n,start,target_ratio)
                print some_men_initial, '-->', some_men
                return (some_men_initial, some_men, n)
            # this one failed
            return None
        # redistribute the wealth
        some_men[giver] -= (count + 1)
        some_men[receiver] += (count +1)
        count += 1
    print '(%s,%s) took too long to redistribute!' %(n,start)
    return None

def test((some_men, n, target_ratio)):
    '''This function tests the ratio between neighbors'''
    for i in range(n):
        man1, man2 = some_men[i], some_men[(i + 1) % n]
        if 0 not in (man1,man2):
            if (float(man1) / man2 == target_ratio) or (float(man2) / man1 == target_ratio):
                return True
    return False

def solve(n_max, start_max, target_ratio):
    '''This function pulls it all together'''
    solutions = 0
    for n in range(3,n_max):
        for start in range(n,start_max):
            if redistribute(n,start,target_ratio):
                solutions += 1
    print "Number of solutions found:", solutions

# You can use solve() to search at any depth for any target ratio.
# The solution to the proposed puzzle is [8, 7, 6, 5, 4, 3, 2].
# So for a ratio of 4 between neighbors, there are 7 men and the poorest man had 2 coins.
solve(n_max=10, start_max=10, target_ratio=4)



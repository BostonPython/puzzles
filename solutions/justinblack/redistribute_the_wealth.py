'''
This solves the redistribute the welth problem from
http://puzzles.bostonpython.com/wealth.html
Author of this solution: Justin Black
Date: 2014-11-11
Python version: 3.4.1
'''

def solve(c_lastp, people):
    ''' returns:
    ratio =  rich_neighbor/poor_neightbor
    circle = list of coin vaues each person has
    '''
    
    circle = [c_lastp + val for val in range(people-1,-1,-1)] #make circle    

    ind = 0         #person index
    passval = 1     #coins to pass to the next perosn
    #print('At person: %i, status: %r' % (ind, circle))
    
    while True:
        coins_curr = circle[ind]
        if coins_curr >= passval: # can still go around the circle
            circle[ind] -= passval # remove coins from current person
            #print('At person: %i, passing %i' % (ind, passval))
            ind = (ind + 1) % people # go to next person
            circle[ind] += passval # add coins to next person
            #print('At person: %i, status: %r' % (ind, circle))        
            passval += 1 # increase the needed pass value
        else: # done going around the circle
            rich = coins_curr
            ind_next = (ind + 1) % people
            poor = circle[ind_next]
            return [rich/poor, circle]


#----------------------------
# Main Problem
#----------------------------

ratios = {}     #store ratio results

for c_lastp in range(1,11):
    for people in range(3,51):
        [ratio, circle] = solve(c_lastp, people)
        
        # store ratio
        if ratio in ratios:
            ratios[ratio] += 1
        else:
            ratios[ratio] = 1
        
        # find answer we want where ratio == 4
        if ratio == 4.0:
            print('People: %i, c_lapstp: %i, ratio: %3f, Circle: %r' % (people, c_lastp, ratio, circle))
            richer = circle[-1] - c_lastp
            print('Poorest man first had %i coins, and ended with %i, getting %i richer' % (c_lastp, circle[-1], richer))

#----------------------------
# BONUS ANSWER
#----------------------------
# loop through results ratios listing items with >1 solution
for k in sorted(ratios):
    if ratios[k] > 1:
        print('Ratio %f has %i solutions' % (k, ratios[k]))
        

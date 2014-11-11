import numpy, itertools, sys

# Surprisingly (to me), numpy is unable to identify duplicate arrays of higher than 1D.
# A workaround is to convert the arrays recursively into tuples, and then use set() on them.
# http://stackoverflow.com/questions/14089453/python-remove-duplicates-from-a-multi-dimensional-array
def tuples(A):
    '''
    Try to recursively convert an N-dimensional array into a (hashable) tuple of tuples
    '''
    try: 
        return tuple(tuples(a) for a in A)
    except TypeError: 
        return A

class Tile:
    '''
    This class defines the puzzle tiles
    '''
    def __init__(self,sides):
        # let's call the set of all orientations of both sides of a tile its vectors
        self.sides = sides
        self.vectors = set()
        for side in sides:
            self.vectors.add(side)
            # now add the 3 other orientations of each side
            for turn in (1,2,3):
                # use the very handy numpy array rotation
                v = numpy.rot90(side,turn)
                # then convert to set-friendly tuples to get only unique vectors
                v = tuples(v)
                self.vectors.add(v)

class Board:
    '''
    This class defines the puzzle board for assembling the tiles
    '''
    def __init__(self,solution,tiles,cutoff=None):
        self.cutoff = cutoff
        self.solution = numpy.array(solution)
        self.rows, self.cols = numpy.shape(solution)
        # create an empty array for assembling puzzle
        self.board = numpy.empty((self.rows, self.cols))
        self.board.fill(numpy.NAN)
        # let's note the number of tiles
        self.tiles_count = len(tiles)
        # let's keep track of the tiles and vectors with dictionaries
        self.tiles = dict()
        self.vectors = []
        c = itertools.count()
        for tile_number,tile in enumerate([ Tile(t) for t in tiles ]):
            self.tiles[tile_number] = tile
            for v in tile.vectors:
                vector_number = next(c)
                array = numpy.array(v)
                rows, cols = numpy.shape(array)
                self.vectors.append({'number':vector_number, 'tile':tile_number, 'array':array, 'rows':rows, 'cols':cols})
        # Nice shortcut: the smallest tile edge determines the spacing of board locations where tiles can be placed.
        # Since these tiles are all 3x6, the step size will be 3, reducing the search graf from 216 nodes to just 24.
        edges = [i['rows'] for i in self.vectors] + [i['cols'] for i in self.vectors]
        step = min(edges)
        self.positions = [ (i,j) for i in range(0,self.rows,step) for j in range(0,self.cols,step) ]

    def search(self):
        '''
        Depth-first search to arrange TILES on board to match SOLUTION
        '''

        # To track search progress
        progress = itertools.count()
        SMALL_STEP = 1000
        BIG_STEP = SMALL_STEP * 10

        # Let's initialize the search data structures
        row,col = 0,0
        placed_tiles, visited, path = set(), set(), []
        stack = [i for i in self.vectors]

        while stack:

            v = stack.pop()

            # show progress
            p = next(progress)
            if p % SMALL_STEP == 0:
                sys.stdout.write(".")
            if (p > 0) and (p % BIG_STEP == 0):
                print "\n%s moves considered" %(p)

            # if you played it safe and included a search cutoff    
            if self.cutoff and (p > self.cutoff):
                print "\nTERMINATED EARLY"
                return None
            
            # check that tile isn't already placed in path
            if v['tile'] not in placed_tiles:

                # check that this tile isn't already visited on identical path
                if tuple( [i['number'] for i in path] + [v['number']] ) not in visited:

                    # check that it does not go beyond board edges
                    if (row + v['rows'] <= self.rows) and (col + v['cols'] <= self.cols):

                        # check that the board has a large enough empty space here
                        if all(numpy.isnan(self.board[ row:row+v['rows'], col:col+v['cols'] ]).flat):

                            # check that vector matches SOLUTION here
                            if numpy.array_equal(v['array'], self.solution[ row:row+v['rows'], col:col+v['cols'] ]):
                                # It matches!

                                # using a numpy index expression, save the indices for placing this vector on the board 
                                # and then add vector to path
                                v['indices'] = numpy.index_exp[ row:(row + v['rows']), col:(col + v['cols']) ]
                                v['position'] = (row,col)
                                path.append(v)

                                # add a tuple of the sequence of vector names for the current path
                                visited.add( tuple([ i['number'] for i in path ]) )

                                # update board
                                for i in path:
                                    self.board[i['indices']] = i['array']
                                # print self.board

                                # Did we match the solution yet?
                                if numpy.array_equal(self.board, self.solution):
                                    return path, p

                                # Move to next empty (row,col) position on board.
                                for (i,j) in self.positions:
                                    if numpy.isnan(self.board[i,j]):
                                        row,col = i,j
                                        break

                                # Update the stack with possible vectors to try here.
                                # Ignore vectors from tiles already placed on board.
                                placed_tiles = set([ i['tile'] for i in path ])
                                for v in self.vectors:
                                    if v['tile'] not in placed_tiles:
                                        stack.append(v)

            # You may need to backtrack
            if path and not stack:
                dead_end = path.pop()
                # update board
                self.board.fill(numpy.NAN)
                for i in path:
                    self.board[i['indices']] = i['array']
                # update (row,col) position
                for (i,j) in self.positions:
                    if numpy.isnan(self.board[i,j]):
                        row,col = i,j
                        break
                # refresh placed_tiles and stack
                placed_tiles = set([ i['tile'] for i in path ])
                for v in self.vectors:
                    if v['tile'] not in placed_tiles:
                        if (v['number'],(row,col)) not in visited:
                            stack.append(v)

        # If you get this far, no solution was found...
        return None

    def solve(self):
        '''
        Define ouput behavior here
        '''
        result = self.search()
        if not result:
            print "\nSOLUTION NOT FOUND"
        else:
            path, p = result
            for i in path:
                print "\nat (%s,%s) place this" %(i['position'])
                print i['array']
                print "from tile", i['tile']
                for i in numpy.array(self.tiles[i['tile']].sides):
                    print i
            print "\nSOLVED in %s moves!" %p
        

SOLUTION = [
(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
(0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0),
(0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0),
(0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0),
(0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0),
(0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0),
(0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0),
(0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0),
(0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0),
(0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0),
(0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0),
(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)]

TILES = [
(
((1,1,1,1,1,1),
(1,1,1,1,1,1),
(1,1,1,1,1,1)),
((0,1,1,1,1,1),
(0,1,1,1,1,1),
(0,0,1,1,1,1))),
(
((1,1,1,1,1,1),
(1,1,1,1,1,1),
(1,1,1,1,1,1)),
((1,1,0,0,0,0),
(1,1,0,0,0,0),
(1,0,0,0,0,0))),
(
((1,1,1,1,1,1),
(1,1,1,1,1,1),
(1,1,1,1,1,1)),
((0,0,0,0,0,0),
(1,1,0,0,0,0),
(1,1,1,1,0,0))),
(
((1,1,1,1,1,1),
(0,1,1,1,1,0),
(0,0,0,0,0,0)),
((1,1,1,1,0,0),
(1,1,0,0,0,0),
(0,0,0,0,0,0))),
(
((1,1,1,1,1,1),
(0,1,1,1,1,0),
(0,0,0,0,0,0)),
((0,0,0,0,0,0),
(0,0,0,0,0,0),
(0,0,0,0,0,0))),
(
((1,1,1,1,1,0),
(1,1,1,1,1,0),
(1,1,1,1,0,0)),
((0,0,0,0,0,0),
(0,0,0,0,0,0),
(1,0,0,0,0,0))),
(
((1,1,1,1,0,0),
(1,1,1,1,1,0),
(1,1,1,1,1,0)),
((0,0,1,1,1,1),
(0,0,0,0,1,1),
(0,0,0,0,0,0))),
(
((0,0,0,0,0,0),
(0,0,0,0,1,1),
(0,0,1,1,1,1)),
((0,0,0,0,0,0),
(0,0,0,0,0,0),
(0,0,0,0,0,0))),
(
((0,0,1,1,1,1),
(0,0,0,0,1,1),
(0,0,0,0,0,0)),
((0,0,0,0,0,0),
(0,0,0,0,0,0),
(0,0,0,0,0,1))),
(
((0,0,0,0,1,1),
(0,0,0,0,1,1),
(0,0,0,0,0,1)),
((0,0,0,0,0,0),
(0,0,0,0,0,0),
(0,0,0,0,0,0))),
(
((0,0,0,0,0,1),
(0,0,0,0,1,1),
(0,0,0,0,1,1)),
((0,0,0,0,0,0),
(0,0,0,0,0,0),
(0,0,0,0,0,1))),
(
((0,0,0,0,0,1),
(0,0,0,0,0,0),
(0,0,0,0,0,0)),
((0,0,0,0,0,0),
(0,0,0,0,0,0),
(0,0,0,0,0,0)))
]
        
B = Board(SOLUTION,TILES)
B.solve()

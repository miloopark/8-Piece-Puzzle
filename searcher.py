#
# classes for objects that perform state-space search on Eight Puzzles  
#

import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    def __init__(self, depth_limit):
        '''constructs a new Searcher object by initializing an attribute 
        states, an attribute num_tested, an attribute depth_limit
        '''
        self.states = []
        self.num_tested = 0
        self.depth_limit = depth_limit
        
    def add_state(self, new_state):
        '''takes a single State object called new_state and adds it to the 
        Searcher‘s list of untested states
        '''
        self.states += [new_state]
        
    def should_add(self, state):
        '''takes a State object called state and returns True if the called 
        Searcher should add state to its list of untested states, and False 
        otherwise
        '''
        if ((self.depth_limit != -1) and (state.num_moves > self.depth_limit))\
        or (state.creates_cycle()):
            return False
        else:
            return True
        
    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s
    
    def add_states(self, new_states):
        '''takes a list State objects called new_states, and that processes 
        the elements of new_states one at a time as follows
        '''
        for i in new_states:
            if self.should_add(i):
                self.add_state(i)
            
    def next_state(self):
        '''chooses the next state to be tested from the list of 
            untested states, removing it from the list and returning it
        '''
        s = random.choice(self.states)
        self.states.remove(s)
        return s
    
    def find_solution(self, init_state):
        '''performs a full state-space search that begins at the specified 
        initial state init_state and ends when the goal state is found or 
        when the Searcher runs out of untested states
        '''
        self.add_state(init_state)
        while self.states != []:
            self.num_tested += 1
            s = self.next_state()
            if s.is_goal():
                return s
            else:
                self.add_states(s.generate_successors())
        return None


class BFSearcher(Searcher):
    '''a class for searcher objects that perform breadth-first search (BFS)
    instead of random search
    '''
    
    def next_state(self):
        '''remove the chosen state from the list of untested states before 
        returning it
        '''
        s = self.states[0]
        self.states.remove(s)
        return s

class DFSearcher(Searcher):
    '''class for searcher objects that perform depth-first search (DFS) 
    instead of random search
    '''
    
    def next_state(self):
        '''follow LIFO (last-in first-out) ordering – choosing the state 
        that was most recently added to the list
        '''
        s = self.states[-1]
        self.states.remove(s)
        return s


def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

def h1(state):
    '''takes a State object called state, and that computes and returns an 
    estimate of how many additional moves are needed to get from state to 
    the goal state
    '''
    return state.board.num_misplaced()    

def h2(self):
    '''computes and returns an 
    estimate of how many additional moves are needed to get from state to 
    the goal state that does a better job than h1
    '''
    wrong_row = 0
    wrong_col = 0
    count = []
    '''
    for i in range(3):
        if self.board.tiles[0][i] not in '012':
            wrong_row += 1
        if self.board.tiles[1][i] not in '345':
            wrong_row += 1
        if self.board.tiles[2][i] not in '678':
            wrong_row += 1
        if self.board.tiles[i][0] not in '036':
            wrong_col += 1
        if self.board.tiles[i][1] not in '147':
            wrong_col += 1
        if self.board.tiles[i][2] not in '258':
            wrong_col += 1
       '''     
    for i in range(3):
        if self.board.tiles[0][i] not in '012':
            if self.board.tiles[0][i] not in count:
                count += self.board.tiles[0][i]
        if self.board.tiles[1][i] not in '345':
            if self.board.tiles[1][i] not in count:
                count += self.board.tiles[1][i]
        if self.board.tiles[2][i] not in '678':
            if self.board.tiles[2][i] not in count:
                count += self.board.tiles[2][i]
        if self.board.tiles[i][0] not in '036':
            if self.board.tiles[i][0] not in count:
                count += self.board.tiles[i][0]
        if self.board.tiles[i][1] not in '147':
            if self.board.tiles[i][1] not in count:
                count += self.board.tiles[i][1]
        if self.board.tiles[i][2] not in '258':
            if self.board.tiles[i][2] not in count:
                count += self.board.tiles[i][2]
        
    return len(count) -1
        

class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """

    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s
    
    def __init__(self, heuristic):
        '''constructs a new GreedySearcher object
        '''
        super().__init__(self)
        self.heuristic = heuristic
        self.depth_limit = -1
        
    def priority(self, state):
        '''computes and returns the priority of the specified state,
        based on the heuristic function used by the searcher
        '''
        return -1 * self.heuristic(state)
    
    def add_state(self, state):
        '''add a sublist that is a [priority, state] pair, where 
        priority is the priority of state that is determined by calling the 
        priority method
        '''
        self.states += [[self.priority(state), state]]
        
    def next_state(self):
        '''choose one of the states with the highest priority
        '''
        s = max(self.states)
        self.states.remove(s)
        return s[-1]

class AStarSearcher(GreedySearcher):
    ''' a subclass of GreedySearcher class for searcher objects that 
    perform A* search
    '''
    
    def priority(self, state):
        '''overrides the priority method in teh GreedySearcher class.
        Computes and returns the priority of the specified state,
        based on the heuristic function used by the searcher
        '''
        return -1 * (self.heuristic(state) + state.num_moves)
    
    















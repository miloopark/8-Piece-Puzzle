#
# A Board class for the Eight Piece Puzzle
#

# a 2-D list that corresponds to the tiles in the goal state
GOAL_TILES = [['0', '1', '2'],
              ['3', '4', '5'],
              ['6', '7', '8']]

class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[''] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1
        
        for r in range(3):
            for c in range(3):
                self.tiles[r][c] = (digitstr[3*r + c])
                if self.tiles[r][c] == '0':
                    self.blank_r = r
                    self.blank_c = c
                        
    def __repr__(self):
        '''returns a string representation of a Board object
        '''
        nump = ''
        for r in range(3):
            for c in range(3):
                if self.tiles[r][c] != '0':
                    nump += self.tiles[r][c] + ' '
                else:
                    nump += '_' + ' '
            nump += '\n'
        return nump
    
    def move_blank(self, direction):
        '''takes as input a string direction that specifies the 
        direction in which the blank should move, and that attempts 
        to modify the contents of the called Board object accordingly
        '''
        row = 0
        col = 0
        if direction == 'up':
            row = self.blank_r - 1
            col = self.blank_c
            if row > 2 or row < 0:
                return False
            else:
                self.tiles[self.blank_r][self.blank_c] = self.tiles[row][col]
                self.tiles[row][col] = '0'
                self.blank_r = row
                self.blank_c = col
                return True
        elif direction == 'down':
            row = self.blank_r + 1
            col = self.blank_c
            if row > 2 or row < 0:
                return False
            else:
                self.tiles[self.blank_r][self.blank_c] = self.tiles[row][col]
                self.tiles[row][col] = '0'
                self.blank_r = row
                self.blank_c = col
                return True
        elif direction == 'left':
            row = self.blank_r
            col = self.blank_c - 1
            if col > 2 or col < 0:
                return False
            else:
                self.tiles[self.blank_r][self.blank_c] = self.tiles[row][col]
                self.tiles[row][col] = '0'
                self.blank_r = row
                self.blank_c = col
                return True
        elif direction == 'right':
            row = self.blank_r
            col = self.blank_c + 1
            if col > 2 or col < 0:
                return False
            else:
                self.tiles[self.blank_r][self.blank_c] = self.tiles[row][col]
                self.tiles[row][col] = '0'
                self.blank_r = row
                self.blank_c = col
                return True
        else:
            return False
       
    def digit_string(self):
        '''creates and returns a string of digits that corresponds to the 
        current contents of the called Board object’s tiles attribute
        '''
        newstr = ''
        for r in range(3):
            for c in range(3):
                newstr += str(self.tiles[r][c])
        return newstr
        
    def copy(self):
        '''returns a newly-constructed Board object that is a deep copy of 
        the called object
        '''
        return Board(self.digit_string())
        
    def num_misplaced(self):
        ''' counts and returns the number of tiles in the called Board object 
        that are not where they should be in the goal state
        '''
        count = 0
        for r in range(3):
            for c in range(3):
                self.tiles[r][c] = str(self.tiles[r][c])
                if self.tiles[r][c] == '0':
                    count += 0
                elif self.tiles[r][c] != GOAL_TILES[r][c]:
                    count += 1
        return count
        
    def __eq__(self, other):
        '''return True if the called object (self) and the argument (other) 
        have the same values for the tiles attribute, and False otherwise
        '''
        if self.tiles == other.tiles:
            return True
        else:
            return False
        
        



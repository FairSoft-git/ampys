# Use these constants in your code 

MIN_SHIP_SIZE = 1
MAX_SHIP_SIZE = 10
MAX_GRID_SIZE = 10
UNKNOWN = '-'
EMPTY = '.'
HIT = 'X'
MISS = 'M'


def read_ship_data(game_file):

    """ (file open for reading) -> list of list of objects

    Return a list containing the ship characters in game_file as a list 
    of strings at index 0, and ship sizes in game_file as a list of ints 
    at index 1.
    """
    # complete the function body for read_ship_data here
    # use split to get ship_chars in a list
    line = game_file.readline()
    lst1 = line.split()
    # use for loop to get ship_sizes in a list
    line = game_file.readline()
    lst2 = []
    for char in line:
        if char.isdigit():
            lst2.append(int(char))
    return [lst1, lst2]


# Write the rest of the required functions here
# Don't forget to follow the Function Design Recipe

def has_ship(fleet_grid, ship_row, ship_column, ship, ship_size):
    
    ''' (list of list of str, int, int, str, int) -> bool
    
    Return Ture if and only if the ship is located in one row or one
    column in a fleet_grid with the corresponding ship_size and the ship
    stars at the cell with ship_row and ship_column.
    
    Precondition: ship_size, ship are valid and the ship_row, ship_column 
    are inside the fleet_grid. 
    
    >>> grid = [['a', '.', '.'], ['a', '.', '.'], ['a', '.', '.']]
    >>> has_ship(grid, 0, 0, 'a', 3)
    True
    >>> grid = [['.', 'b', '.'], ['.', '.', 'b'], ['.', '.', '.']]
    >>> has_ship(grid, 0, 1, 'b', 2)
    False
    ''' 
    # Test the start cell
    if fleet_grid[ship_row][ship_column] != ship:
        return False
    for i in range(ship_row):
        for j in range(ship_column):
            if fleet_grid[i][j] == ship:
                return False   
    # Test the ship size
    if len(get_location(fleet_grid, ship)[0]) != ship_size:
        return False
    # Test the ship location (in one row or one column)
    if not validate_ship_positions(fleet_grid, [ship], [ship_size]):
        return False       
    return True


def validate_character_count(fleet_grid, ship_chars, ship_sizes):
    
    '''(list of list of str, list of str, list of int) -> bool
    
    Return True if and only if the number of ship_chars is right related to
    each ship_sizes on the fleet_grid and the number of EMPTY characters are
    right.
    
    Precondition: ship_sizes, ship_chars are valid.
    
    >>> grid = [['a', '.', 'b'], ['a', '.', 'b'], ['a', 'c', 'c']]
    >>> validate_character_count(grid, ['a', 'b', 'c'], [3, 2, 2])
    True
    >>> grid = [['a', 'c', 'c'], ['a', '.', '.'], ['b', 'b', '.']]
    >>> validate_character_count(grid, ['a', 'b', 'c'], [3, 2, 2])
    False
    '''
    # Validate the grid size
    if len(fleet_grid) > MAX_GRID_SIZE:
        return False
    # Check every ship's size
    order = 0
    for size in ship_sizes:
        if len(get_location(fleet_grid, ship_chars[order])[0]) != size:
            return False
        if size <= 0:
            return False
        order += 1
    # Check EMPTY characters
    empty = 0
    for row in fleet_grid:
        empty = empty + row.count(EMPTY)
    if empty != len(fleet_grid) ** 2 - sum(ship_sizes):
        return False
    return True


def validate_ship_positions(fleet_grid, ship_chars, ship_sizes):
    
    ''' (list of list of str, list of str, list of int) -> bool
    
    Return True if and only if every ship in ship_chars is located in one row
    or one column with the right ship_sizes in the fleet_grid.
    
    Precondition: the fleet_grid, ship_sizes, ship_chars are valid.
    
    >>> grid = [['a', 'b', 'b'], ['a', 'c', '.'], ['a', 'c', '.']]
    >>> validate_ship_positions(grid, ['a', 'b', 'c'], [3, 2, 2])
    True
    >>> grid = [['a', '.', 'b'], ['.', 'b', '.'], ['a', '.', '.']]
    >>> validate_ship_positions(grid, ['a', 'b'], [2, 2])
    False
    '''
    # Validate grid size
    if len(fleet_grid) > MAX_GRID_SIZE:
            return False    
    location = 0
    for size in ship_sizes:
        if size != 1:
            rows = get_location(fleet_grid, ship_chars[location])[0]
            columns = get_location(fleet_grid, ship_chars[location])[1]
            # Check the whole ship is in one row or one column
            if (rows.count(rows[0]) != len(rows) and \
               columns.count(columns[0]) != len(columns)) or len(rows) != size:
                return False
            elif rows.count(rows[0]) == len(rows):
                if columns[-1] - columns[0] != size - 1:
                    return False
            elif columns.count(columns[0]) == len(columns):
                if rows[-1] - rows[0] != size - 1:
                    return False
        location += 1
    return True
    

def validate_fleet_grid(fleet_grid, ship_chars, ship_sizes):
    
    '''(list of list of str, list of str, list of int) -> bool
    
    Return True if and only if the fleet_grid is valid with the correct
    ship_chars and ship_sizes.
    
    Precondition: ship_sizes, ship_chars are valid.
    
    >>> grid = [['a', 'b', 'b'], ['a', 'c', '.'], ['a', 'c', '.']]
    >>> validate_fleet_grid(grid, ['a', 'b', 'c'], [3, 2, 2])
    True
    >>> grid = [['.', 'b', '.'], ['.', '.', 'b'], ['.', '.', '.']]
    >>> validate_fleet_grid(grid, ['b'], [2])
    False
    '''
    
    # Use functions I just defined to define this function
    return validate_character_count(fleet_grid, ship_chars, ship_sizes) and \
           validate_ship_positions(fleet_grid, ship_chars, ship_sizes)


def valid_cell(row, column, grid_size):
    '''(int, int, int) -> bool
    
    Return True if and only if the cell with row index row and column index
    column is in the grid which is a square grid with side length grid_size.
    
    >>> valid_cell(5, 4, 6)
    True
    >>> valid_cell(8, 5, 6)
    False
    '''
    # Validate cell by checking its row index and column index
    if grid_size < 1 or grid_size > MAX_GRID_SIZE:
        return False
    return row >= 0 and row < grid_size and column >= 0 and column < grid_size
    

def is_not_given_char(row, column, fleet_grid, char):
    ''' (int, int, list of list of str, str) -> bool
    
    Return True if and only if the character in the cell with row and column
    in the fleet_grid is not char.
    
    Precondition: the fleet_grid, char, and the cell with location row and 
    column are all valid.
    
    >>> grid = [['a', 'b', 'b'], ['a', 'c', '.'], ['a', 'c', '.']]
    >>> is_not_given_char(2, 1, grid, 'c')
    False
    >>> grid = [['a', '.', '.'], ['a', '.', '.'], ['c', 'c', 'c']]
    >>> is_not_given_char(1, 1, grid, 'a')
    True
    '''
    return fleet_grid[row][column] != char


def update_fleet_grid(row, column, fleet_grid, ship_chars, ship_sizes, hits):
    ''' (int, int, list of list of str, list of str, list of int, list of
    int) -> NoneType
    
    Modify the fleet_grid and hits when there is a hit in the position of row
    and column and the ship from ship_chars with relative ship_sizes has been
    hitten. Print the sunk message if the hits data for the ship is equal to
    its ship_sizes data.
    
    Precondition: the fleet_grid, ship_chars, ship_sizes, hits and the cell
    with location row and column are all valid.
    
    >>> fleet_grid = [['.', 'a', '.'], ['.', 'a', '.'], ['b', 'b', 'b']]
    >>> hits = [0, 0]
    >>> update_fleet_grid(1, 1, fleet_grid, ['a', 'b'], [2, 3], hits)
    >>> fleet_grid
    [['.', 'a', '.'], ['.', 'A', '.'], ['b', 'b', 'b']]
    >>> hits
    [1, 0]
    >>> fleet_grid = [['a', 'a', 'C'], ['.', '.', 'c'], ['b', 'b', 'b']]
    >>> hits = [0, 0, 1]
    >>> update_fleet_grid(1, 2, fleet_grid, ['a', 'b', 'c'], [2, 3, 2], hits)
    The size 2 c ship has been sunk!
    >>> fleet_grid
    [['a', 'a', 'C'], ['.', '.', 'C'], ['b', 'b', 'b']]
    >>> hits
    [0, 0, 2]
    '''
    # Find out which ship got hit and update hits list
    hit_ship = ship_chars.index(fleet_grid[row][column])
    hits[hit_ship] += 1
    # Update fleet_grid
    fleet_grid[row][column] = fleet_grid[row][column].upper()
    if hits[hit_ship] == ship_sizes[hit_ship]:
        return print_sunk_message(ship_sizes[hit_ship], ship_chars[hit_ship])
    

def update_target_grid(row, column, target_grid, fleet_grid):
    ''' (int, int, list of list of str, list of list of str) -> NoneType
    
    Show HIT or MISS on the target_grid from the information about the position 
    with row and column on the fleet_grid.
    
    Precondition: the target_grid, fleet_grid and the cell with location row and
    column are all valid.
    
    >>> target_grid = [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
    >>> fleet_grid = [['.', 'a', 'a'], ['b', '.', '.'], ['c', 'c', 'c']]
    >>> update_target_grid(0, 1, target_grid, fleet_grid)
    >>> target_grid
    [['-', 'X', '-'], ['-', '-', '-'], ['-', '-', '-']]
    >>> target_grid = [['-', '-', '-'], ['-', '-', '-'], ['-', 'M', '-']]
    >>> fleet_grid = [['.', 'a', '.'], ['b', '.', '.'], ['b', '.', 'c']]
    >>> update_target_grid(1, 2, target_grid, fleet_grid)
    >>> target_grid
    [['-', '-', '-'], ['-', '-', 'M'], ['-', 'M', '-']]
    '''
    
    if fleet_grid[row][column] == EMPTY:
        target_grid[row][column] = MISS
    else:
        target_grid[row][column] = HIT


def is_win(ship_sizes, hits_list):
    '''(list of int, list of int) -> bool
    
    Return True if and only if all the ships are sunk, which means the every
    element in the hits_list is equal to the corresponding element in the
    ship_sizes.
    
    Precondition: ship_sizes, hits_list are valid.
    
    >>> is_win([2, 1, 3], [2, 1, 3])
    True
    >>> is_win([2, 1, 3], [1, 0, 3])
    False
    '''
    return ship_sizes == hits_list


    
##################################################
## Helper function to call in update_fleet_grid
## Do not change!
##################################################


def print_sunk_message(ship_size, ship_character):
    """ (int, str) -> NoneType
  
    Print a message telling player that a ship_size ship with ship_character
    has been sunk.
    """

    print('The size {0} {1} ship has been sunk!'.format(ship_size,\
                                                        ship_character))
    
def get_location(fleet_grid, ship_char):
    ''' (list of list of str, str) -> list of list of int
    
    Return a list containing all the row index for the ship_char from in the
    fleet_grid as a list of intigers at index 0, and all the column index for
    the ship_char as a list of ints at index 1.
    
    >>> grid = [['.', 'a', '.'], ['.', 'a', 'b'], ['.', 'a', 'b']]
    >>> get_location(grid, 'a')
    [[0, 1, 2], [1, 1, 1]]
    >>> grid = [['a', 'b', 'b'], ['a', '.', '.'], ['c', 'c', 'c']]
    >>> get_location(grid, 'b')
    [[0, 0], [1, 2]]
    '''
    row_list = []
    column_list = []
    for i in range(len(fleet_grid)):
        if ship_char in fleet_grid[i]:
            char_location = 0
            for char in fleet_grid[i]:
                if char == ship_char:
                    row_list.append(i)
                    column_list.append(char_location)
                char_location += 1
    return [row_list, column_list]

    
if __name__ == '__main__': 
    import doctest
    doctest.testmod()
    # uncomment the line below to run the docstring examples     
    #doctest.testmod()
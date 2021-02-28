import random # needed for ship placement

""" A battleship game to be played against the computer using the console

The computer generates the grid of targets for the player to shoot at.
and hides the ships for the game on another grid of equal dimensions to the target grid
The grid is 10x10 for the battleship game but for testing purposes the grid can be made other sizes
The following ships are placed on the grid at random with the following sizes:
1x Battleship (5 squares)
2x Destroyers (4 squares)
To fire at a target the player enters coordinates of the form “A5”,
where “A” is the column and “5” is the row, to specify a square to target
Shots result in hits, misses or sinks. The game ends when all ships are sunk.
"""


def createTargetGrid(n_rows, n_cols):
    """Create and return the grid of strings which the player can select as a target.
    n_rows and n_cols provide the grid dimensions for the target grid to be made
    """

    string_grid = []
    for row in range(n_rows):
        row_val = str(row + 1)
        row = []
        for column in range(n_cols):
            #Convert column number to an uppercase letter, chr(97) corresponds to the letter A
            col_val = str(chr(97+column)).upper()
            val =  col_val + row_val #Concatenate strings to make target value
            row.append(val) #Add the target to the row
        string_grid.append(row) #Add the row to the grid of targets

    return string_grid


def createEmptyShipGrid(n_rows, n_cols):
    """Create and return an empty grid to add ships to.
    n_rows and n_cols provide the grid dimensions for the ship grid to be made
    """

    return [[0 for i in range(n_cols)] for j in range(n_rows)]


def displayGrid(grid):
    """Print the grid provided as an input with each element being formatted to an equal width for neatness
    """
    for row in grid:
        string = ""
        for elem in row:
            string += f'{elem: <5}' #add spaces to make each element 5 characters wide
        print (string)


def getCoordsRandomEmptySquare(ship_grid, rows, cols):
    """Return the coordinates of a random empty square in the grid

    Generate random coordinates until an empty square is found
    Return the coordinates of the empty square
    """
    square_clear = False

    # Generate random coordinates until an empty square is found
    while (square_clear == False):
        square_y = random.randrange(0,rows)
        square_x = random.randrange(0,cols)

        # Return coordinates if square is empty
        if ship_grid[square_y][square_x] == 0:
            square_clear = True
            return square_x, square_y


def getDirectionVector(dir):
    """Return the appropriate direction vector for the input value
    """
    if (dir == 1): #right from origin
        dir_vector = [0, 1]

    elif (dir == 2): #down from origin
        dir_vector = [1, 0]

    elif (dir == 3): #left from origin
        dir_vector = [0, -1]

    elif (dir == 4): #up from origin
        dir_vector = [-1, 0]


    return dir_vector


def checkGridFit(dir, origin_x, origin_y, ship_length, cols, rows):
    """Evaluate if the ship will fit the grid dimensions in the direction chosen

    For the input direction provided,
    test to see if the ship can fit into the grid.
    If the ship fits into the grid for the direction provided return True,
    otherwise return False.
    """

    grid_fit = False

    if (dir == 1): #right from origin
        if ( (origin_x + ship_length) <= cols): #check fits in grid
            grid_fit = True

    elif (dir == 2): #down from origin
        if ( (origin_y + ship_length) <= rows): #check fits in grid
            grid_fit = True

    elif (dir == 3): #left from origin
        if ( ((origin_x+1) - ship_length) >= 0): #check fits in grid
            grid_fit = True

    elif (dir == 4): #up from origin
        if ( ((origin_y+1) - ship_length) >= 0): #check fits in grid
            grid_fit = True


    return grid_fit


def shipOverlapCheck(origin_y, origin_x, dir_vector, ship_length, ship_grid):
    """Check if proposed ship placement would overlap with a ship in the grid

    Test to see if the proposed ship placement overlaps with another
    ship already in the grid. If all the spaces are empty return True.
    If there is an overlap return False
    """

    space_for_ship = True
    distance_from_origin = 1

    #Exit loop if ships overlap or once all sections of the ship have been checked
    while (space_for_ship == True) and (distance_from_origin < ship_length):
        y_coord = origin_y + (distance_from_origin * dir_vector[0])
        x_coord = origin_x + (distance_from_origin * dir_vector[1])

        # If ships overlap set Boolean to false
        if ship_grid[y_coord][x_coord] != 0:
            space_for_ship = False
        # Else increase distance from origin for the next
        else:
            distance_from_origin += 1

    return space_for_ship


def placeShipInGrid(origin_y, origin_x, dir_vector, ship_length, ship_no, ship_grid):
    """Update ship grid with new ship

    Place ship into the ship grid by setting the values of all the squares
    it occupies to its ship number
    """

    for ship_section in range(ship_length):
        y_coord = origin_y + (ship_section * dir_vector[0])
        x_coord = origin_x + (ship_section * dir_vector[1])
        ship_grid[y_coord][x_coord] = ship_no


def addShipToShipGrid(ship_length, ship_no, ship_grid):

    """Add a ship to the ship grid.

    Before placing the ship check:
    1) That the origin position is clear
    2) Select a direction and check:
    a) That the ship fits in the grid
    b) That the ship doesn't overlap with another ship
    If proposed ship placement passes the above conditions ->
    Place the ship by updating the values of the ship grid

    If the proposed ship placement does not pass conditions 1, 2a and 2b ->
    Select a new origin and direction to check

    Continue generating origins and directions until the ship can be added to the grid.
    """

    rows = len(ship_grid)
    cols = len(ship_grid[0])


    ship_placed_bool = False
    while (ship_placed_bool == False): #Loop until ship is successfully placed on the grid

        #pick an empty square of the grid randomly as the origin
        origin_x, origin_y = getCoordsRandomEmptySquare(ship_grid, rows, cols)

        # use numbers 1-4 as directions and select a random direction
        direction = random.randrange(1,5)

        #check if ship fits into grid in that direction
        grid_fit_bool = checkGridFit(direction, origin_x, origin_y, ship_length, cols, rows)

        if grid_fit_bool == True:

            # set the vector values for that direction
            dir_vector = getDirectionVector(direction)

            #check if proposed coordinates for ship overlap with an already present ship
            space_for_new_ship_bool = shipOverlapCheck(origin_y, origin_x, dir_vector, ship_length, ship_grid)

            #If all squares are clear place ship in the grid
            if space_for_new_ship_bool == True:
                placeShipInGrid(origin_y, origin_x, dir_vector, ship_length, ship_no, ship_grid)
                ship_placed_bool = True



def setupGame(rows, cols, ship_health):
    """Initiate the variables needed for the game

    1) Create the target grid
    2) Create an empty ship grid
    3) Place ships into ship grid
    4) Return the target grid, the ship grid and the number of ships in the grid

    """

    #Initiate grid of targets and a matching grid of 0's waiting for ships to be added
    targetgrid = createTargetGrid(rows,cols)
    shipgrid = createEmptyShipGrid(rows,cols)

    #Loop through the ships and add each to the grid of ships
    #Get ship_length from the ship_health array and add 1 to the array index to provide the ship number
    for ship in range(len(ship_health)):
        ship_length = ship_health[ship]
        ship_no = ship+1
        addShipToShipGrid(ship_length, ship_no, shipgrid)

    ship_count = len(ship_health) #set number of ships at start of game

    return targetgrid, shipgrid, ship_count


def getUserInput():
    """Ask the player to input a target."""

    return input("\nPlease enter coordinates for a target:\n").upper()


def checkUserInput(user_input, target_grid):
    """Check if the player has provided a valid target

    If they have provided a valid target return True,
    Otherwise return False
    """

    #special cases because they are in the target grid but aren't valid targets
    if user_input == "x" or user_input == "-":
        return False

    #For all other inputs:
    else:
        #Check if the user's input matches any targets in the target grid
        for row in target_grid:
            for target in row:
                if target == user_input:
                    return True
        #Return false if the user's input doesn't match any targets in the target grid
        else:
            return False


def fireAtTarget(user_input, target_grid, ship_grid, ship_health, ship_count):
    """Fire at target chosen by the player

    1) Get the indices of the target to be fired at
    2) Check if ship was present in that square
    3) Update the target grid to indicate hit or miss
    4) If ship gets hit then update the health pool
        a) If ship gets sunk then decrement the ship count
    5) Return the outcome - sink, hit, miss - as a string
    6) Return the ship count
    """

    for row in target_grid:
        for target in row:
            if target == user_input:
                row_no = target_grid.index(row)
                col_no = row.index(target)

    if ship_grid[row_no][col_no] != 0: #ship has been hit
        target_grid[row_no][col_no] = "x"
        ship_hit = ship_grid[row_no][col_no] - 1
        ship_health[ship_hit] -= 1

        if ship_health[ship_hit] == 0: #ship has been sunk
            outcome_string = "\nShip sunk!\n"
            ship_count -= 1

        else: #ship has been hit, but not yet sunk
            outcome_string = "\nHit!\n"

    else: #miss
        target_grid[row_no][col_no] = "-"
        outcome_string = "\nMiss\n"

    return outcome_string, ship_count



#
#
# Battleship program
#
#

#If launched as main program play a game of battleship
if __name__ == "__main__":


    # Set up the game
    rows, cols = 10, 10
    ship_health = [5, 4, 4]
    targetgrid, shipgrid, ship_count = setupGame(rows, cols, ship_health)


    # Game loop
    # While at least one ship is afloat:
    #1) Show target grid and number of ships remaining
    #2) Request a target
    #3) a) If user provides a valid target then:
    #      fire at the target and tell the player the outcome of their shot
    # 3) b) Otherwise inform the player that their target was not recognized

    while ship_count > 0:
        displayGrid(targetgrid)
        print("Ships remaining: " + str(ship_count))

        user_input = getUserInput()
        valid_target = checkUserInput(user_input, targetgrid) #Check the player provides a valid target

        if valid_target == True: #If the player provides a valid target fire at it
            shot_outcome_string, ship_count = fireAtTarget(user_input, targetgrid, shipgrid, ship_health, ship_count)
            print(shot_outcome_string)

        else: #Display error string to player if invalid target provided
            print("\nTarget not recognized. Please enter a target from the grid below:\n")


    #End the game once all ships have been sunk:
    displayGrid(targetgrid)
    print("\nCongratulations!\nAll ships destroyed")

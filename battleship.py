import random # needed for ship placement

""" A battleship game to be played against the computer using the console

Computer generates the grid of targets for the player to shoot at.
The computer then places the ships on another grid of equal dimensions to the target grid
The grid is 10x10 for the battleship game but for testing purposes the grid can be made other sizes
The following ships are placed on the grid at random with the following sizes:
1x Battleship (5 squares)
2x Destroyers (4 squares)
To fire at a target the player enters coordinates of the form “A5”,
where “A” is the column and “5” is the row, to specify a square to target
Shots result in hits, misses or sinks. The game ends when all ships are sunk.
"""


def createTargetGrid(n_rows, n_cols):
    """Create and return the grid of strings which the player can select as a target
    """

    string_grid = []
    for row in range(n_rows):
        row_val = str(row + 1)
        row = []
        for column in range(n_cols):
            val = str(chr(97+column)).upper() + row_val
            row.append(val)
        string_grid.append(row)

    return string_grid


def createEmptyShipGrid(n_rows, n_cols):
    """Create and return an empty grid to add ships to.
    """

    return [[0 for i in range(n_cols)] for j in range(n_rows)]


def displayGrid(grid):
    """Print the input grid with each element being formatted to an equal width for neatness
    """
    for row in grid:
        string = ""
        for elem in row:
            string += f'{elem: <5}'
        print (string)


def placeShipOnShipGrid(ship_length, ship_no, ship_grid):

#TODO    # """Add a ship to the grid and add its health to the health pool.
    #
    # When placing the ship check:
    # 1) That the origin position is clear
    # 2) Select a direction and check:
    # a) That the ship fits in the grid
    # b) That the ship doesn't overlap with another ship
    # If proposed ship placement passes the above conditions ->
    # Place the ship by updating the values of the grid
    # Also append the health array to include it's health
    #
    # If the proposed ship placement does not pass conditions 1, 2a and 2b ->
    # Select a new origin and direction to check
    #
    # Continue generating origins and directions until the ship can be placed.
    # """

    rows = len(ship_grid)
    cols = len(ship_grid[0])


    ship_placed = False
    while (ship_placed == False): #Loop until ship is successfully placed on the grid

        #pick an origin in the grid to try
        origin_selected = False

        while (origin_selected == False):
            origin_y = random.randrange(0,rows)
            origin_x = random.randrange(0,cols)

            if ship_grid[origin_y][origin_x] == 0:
                origin_selected = True

        # use numbers 1-4 as directions and select a random direction
        dir = random.randrange(1,5)

        #check if ship fits into grid in that direction
        #if successful set the vector values for that direction

        grid_fit = False

        if (dir == 1): #right from origin
            if ( (origin_x + ship_length) <= cols): #check fits in grid
                grid_fit = True
                dir_vector = [0, 1]

        elif (dir == 2): #down from origin
            if ( (origin_y + ship_length) <= rows): #check fits in grid
                grid_fit = True
                dir_vector = [1, 0]

        elif (dir == 3): #left from origin
            if ( ((origin_x+1) - ship_length) >= 0): #check fits in grid
                grid_fit = True
                dir_vector = [0, -1]

        elif (dir == 4): #up from origin
            if ( ((origin_y+1) - ship_length) >= 0): #check fits in grid
                grid_fit = True
                dir_vector = [-1, 0]



        if grid_fit == True:

            #check if proposed coordinates for ship overlap with an already present ship
            #if fails test select new origin
            #(selecting a new direction instead leads to patterns in grid placement)


            ships_overlap = False
            distance_from_origin = 1

#TODO            #Exit loop if ships overlap or if
            while (ships_overlap == False) and (distance_from_origin < ship_length):
                y_coord = origin_y + (distance_from_origin * dir_vector[0])
                x_coord = origin_x + (distance_from_origin * dir_vector[1])

                # If ships overlap set Boolean to true
                if ship_grid[y_coord][x_coord] != 0:
                    ships_overlap = True
                # Else increase distance from origin for the next
                else:
                    distance_from_origin += 1

            #If all squares are clear place ship
            if ships_overlap == False:
                for ship_section in range(ship_length):
                    y_coord = origin_y + (ship_section * dir_vector[0])
                    x_coord = origin_x + (ship_section * dir_vector[1])

                    ship_grid[y_coord][x_coord] = ship_no
                ship_placed = True



def setupGame(rows, cols, ship_health):
#TODO
    #Initiate grid of targets and a matching grid of 0's waiting for ships to be added
    targetgrid = createTargetGrid(rows,cols)
    shipgrid = createEmptyShipGrid(rows,cols)

    #Loop through the ships and add each to the grid of ships
    #Get ship_length from the ship_health array and add 1 to the array index to provide the ship number
    for ship in range(len(ship_health)):
        ship_length = ship_health[ship]
        ship_no = ship+1
        placeShipOnShipGrid(ship_length, ship_no, shipgrid)

    ship_count = len(ship_health) #set number of ships at start of game
    shot_outcome_string="" #set as empty for the first loop

    return targetgrid, shipgrid, ship_count, shot_outcome_string



def getUserInput():
    """Ask the player to input a target."""

    return input("\nPlease enter coordinates for a target(e.g. H5):\n").upper()

def checkUserInput(user_input, target_grid):

    if user_input == "x" or user_input == "-":
        return False

    else:
        for row in target_grid:
            for target in row:
                if target == user_input:
                    return True
        else:
            return False


# def getTarget(targetgrid):
# #TODO    """Check target is valid"""
#
#     valid_target = False
#     error_string = "\nTarget not recognized"
#
#     while valid_target == False:
#
#         user_input = getUserInput()
#
#         if user_input == "x" or user_input == "-":
#             print(error_string)
#
#         else:
#             for row in targetgrid:
#                 for target in row:
#                     if target == user_input:
#                         valid_target = True
#                         indices = [targetgrid.index(row), row.index(target)]
#                         return indices
#             else:
#                 print(error_string)
#


def fireAtTarget(user_input, target_grid, ship_grid, ship_health, ship_count):
#TODO    """Fire at target chosen by the player, provide them with the outcome,
#    update the target grid and update the health pool if necessary"""

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

if __name__ == "__main__":
#TODO

    rows, cols = 4, 5
    ship_health = [5, 4, 4]

    targetgrid, shipgrid, ship_count, shot_outcome_string = setupGame(rows, cols, ship_health)


    # Game loop
    # While at least one ship is afloat:
    #1) Tell player outcome of their shot (except on first loop)
    #2) Show current grid and number of ships remaining
    #3) Request a target (until user provides a valid target)
    #4) Fire at target

    while ship_count > 0:
        displayGrid(targetgrid)
        print("Ships remaining: " + str(ship_count))

        valid_target = False
        while valid_target == False:
            user_input = getUserInput()
            valid_target = checkUserInput(user_input, targetgrid) #True if input matches a target
            if valid_target == False: #Display error string to player if invalid target provided
                print("\nTarget not recognized")

        shot_outcome_string, ship_count = fireAtTarget(user_input, targetgrid, shipgrid, ship_health, ship_count)


    #End the game once all ships have been sunk:
    print(shot_outcome_string)
    displayGrid(targetgrid)
    print("\nCongratulations!\nAll ships destroyed")

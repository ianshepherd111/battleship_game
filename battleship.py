
import random # needed for ship placement

def createGrids(n_rows, n_cols):
    """Create the grid of target strings and an empty grid to add ships to.
    """
    string_grid = []
    for row in range(n_rows):
        row_val = str(row + 1)
        row = []
        for column in range(n_cols):
            val = str(chr(97+column)).upper() + row_val
            row.append(val)
        string_grid.append(row)

        ship_grid = [[0 for i in range(n_cols)] for j in range(n_rows)]

    return string_grid, ship_grid



def displayGrid(string_grid):
    """Print the target grid with each target having an equal width to make it neat
    """
    for row in string_grid:
        string = ""
        for elem in row:
            string += f'{elem: <5}'
        print (string)


def placeShip(ship_grid, ship_health, ship_length):
    """Add a ship to the grid and add its health to the health pool.
    When placing the ship check:
    1) That the origin position is clear
    2) Select a direction and check:
    a) That the ship fits in the grid
    b) That the ship doesn't overlap with another ship
    If proposed ship placement passes conditions -> place ship
    """

    rows = len(ship_grid)
    cols = len(ship_grid[0])

    ship_no = len(ship_health)+1

    ship_placed = False

    while (ship_placed == False):

        #pick an origin in the grid to try
        origin_selected = False

        while (origin_selected == False):
            num_coord = random.randrange(0,rows)
            alpha_coord = random.randrange(0,cols)

            if ship_grid[num_coord][alpha_coord] == 0:
                origin_selected = True


        # use numbers 1-4 as directions and select a random direction
        dir = random.randrange(1,5)

        #check if ship fits into grid in that direction
        #if successful set the vector values for that direction

        #right from origin
        if (dir == 1) and ( (alpha_coord + ship_length) <= cols):
            grid_fit = True
            dir_vector = [0, 1]

        #down from origin
        elif (dir == 2) and ( (num_coord + ship_length) <= rows):
            grid_fit = True
            dir_vector = [1, 0]

        #left from origin
        elif (dir == 3) and ( ((alpha_coord+1) - ship_length) >= 0):
            grid_fit = True
            dir_vector = [0, -1]

        #up from origin
        elif (dir == 4) and ( ((num_coord+1) - ship_length) >= 0):
            grid_fit = True
            dir_vector = [-1, 0]

        #The direction chosen fails to pass
        else:
            grid_fit = False


        if grid_fit == True:

            #check if ships proposed coordinates overlap with another ship
            #if fails test select new origin

            spaces_clear = True
            space_to_check = 1
            while (spaces_clear == True) and (space_to_check < ship_length):
                if ship_grid[num_coord + space_to_check * dir_vector[0]][alpha_coord + space_to_check * dir_vector[1]] != 0:
                    spaces_clear = False
                else:
                    space_to_check += 1

            #place ship if all squares are clear
            if spaces_clear == True:
                for space_to_occupy in range(0,ship_length):
                    ship_grid[num_coord + space_to_occupy * dir_vector[0]][alpha_coord + space_to_occupy * dir_vector[1]] = ship_no
                ship_placed = True
                ship_health.append(ship_length)


def getUserinput():
    return input("\nPlease enter coordinates for a target e.g. H5\n").upper()

def requestTarget(targetgrid):

    valid_target = False
    error_string = "\nTarget not recognized"

    while valid_target == False:

        user_input = getUserinput()

        if user_input == "x" or user_input == "-":
            print(error_string)

        else:
            for row in targetgrid:
                for available_target in row:
                    if available_target == user_input:
                        valid_target = True
                        indices = [targetgrid.index(row), row.index(available_target)]
                        return indices
            else:
                print(error_string)



def fireAtTarget(targetgrid, shipgrid, target, health, ship_count):


    if shipgrid[target[0]][target[1]] != 0:
        targetgrid[target[0]][target[1]] = "x"
        ship_no_hit = shipgrid[target[0]][target[1]]
        health[ship_no_hit-1] -= 1
        if health[ship_no_hit-1] == 0:
            outcome_string = "\nShip sunk!\n"
            ship_count -= 1

        else:
            outcome_string = "\nHit!\n"

    else:
        targetgrid[target[0]][target[1]] = "-"
        outcome_string = "\nMiss\n"

    return outcome_string, ship_count




# def debugCheckShipPlacer(rows, cols, runs):
#     """Test the distribution of ships generated by the PlaceShip function by running it "runs" many times
#     """
#
#
#     sumgrid = [[0 for i in range(cols)] for j in range(rows)]
#
#     for i in range (runs):
#         shipgrid = [[0 for i in range(cols)] for j in range(rows)]
#         health = []
#         placeShip(shipgrid, health, 5)
#         placeShip(shipgrid, health, 4)
#         placeShip(shipgrid, health, 4)
#
#
#         for i in range(cols):
#             for j in range(rows):
#                 sumgrid[i][j] += shipgrid[i][j]
#
#     # Integer division by a factor proportional to the number of runs to make it easier to see approximate ship distribution
#     if runs > 50:
#         division_factor = runs // 50
#     else:
#         division_factor = 1 #because otherwise division by zero
#
#
#     for i in range(cols):
#         for j in range(rows):
#             sumgrid[i][j] = sumgrid[i][j] // division_factor
#
#     debugDisplayShips(sumgrid)


#
#
# Battleship program
#
#

if __name__ == "__main__":

    #Initiate grid of targets and a matching grid waiting for ships to be added
    rows, cols = 10, 10
    targetgrid, shipgrid = createGrids(rows,cols)

    #debugCheckShipPlacer(rows, cols, 500000)

    #Initiate ship positions and ship health
    health = []
    placeShip(shipgrid, health, 5)
    placeShip(shipgrid, health, 4)
    placeShip(shipgrid, health, 4)

    ship_count = len(health)
    shot_outcome_string="" #set as empty for the first loop

    #debugDisplayShips(shipgrid)

    # Game loop
    #1) Tell player outcome of their shot
    #2) Show updated grid and number of ships remaining
    #3) Request a new target
    #4) Fire at target

    while ship_count > 0:
        print(shot_outcome_string)
        displayGrid(targetgrid)
        print("Ships remaining: " + str(ship_count))

        target = requestTarget(targetgrid)

        shot_outcome_string, ship_count = fireAtTarget(targetgrid, shipgrid, target, health, ship_count)



    print(shot_outcome_string)
    displayGrid(targetgrid)

    print("\nCongratulations!\nAll ships destroyed")

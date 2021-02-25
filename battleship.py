
import random # needed for ship placement

def createTargetGrid(n_rows, n_cols):
    """Create the grid of target strings
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
    """Create an empty grid to add ships to.
    """

    return [[0 for i in range(n_cols)] for j in range(n_rows)]




def displayGrid(grid):
    """Print the target grid with each target having an equal width to make it neat
    """
    for row in grid:
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

            #check if proposed coordinates for ship overlap with an already present ship
            #if fails test select new origin
            #(selecting a new direction instead leads to patterns in grid placement)
            space_for_ship = True
            distance_from_origin = 1
            while (space_for_ship == True) and (distance_from_origin < ship_length):
                if ship_grid[num_coord + distance_from_origin * dir_vector[0]][alpha_coord + distance_from_origin * dir_vector[1]] != 0:
                    space_for_ship = False
                else:
                    distance_from_origin += 1

            #place ship if all squares are clear
            if space_for_ship == True:
                for space_to_occupy in range(ship_length):
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





#
#
# Battleship program
#
#

if __name__ == "__main__":

    #Initiate grid of targets and a matching grid waiting for ships to be added
    rows, cols = 10, 10
    targetgrid = createTargetGrid(rows,cols)
    shipgrid = createEmptyShipGrid(rows,cols)

    #Initiate ship positions and ship health
    health = []
    placeShip(shipgrid, health, 5)
    placeShip(shipgrid, health, 4)
    placeShip(shipgrid, health, 4)

    ship_count = len(health)
    shot_outcome_string="" #set as empty for the first loop


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

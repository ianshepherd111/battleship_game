import random
import battleship

def debugSetupShipGrid(rows, cols, ship_health, algorithm_bool):
#TODO
    #Initiate grid of targets and a matching grid of 0's waiting for ships to be added
    shipgrid = battleship.createEmptyShipGrid(rows,cols)

    #Loop through the ships and add each to the grid of ships
    #Get ship_length from the ship_health array and add 1 to the array index to provide the ship number
    for ship in range(len(ship_health)):
        ship_length = ship_health[ship]
        ship_no = ship+1
        battleship.addShipToShipGrid(ship_length, ship_no, shipgrid, algorithm_bool)

    return shipgrid

def addShipPositionsToSumGrid(shipgrid, sumgrid, rows, cols):

    for i in range(rows):
        for j in range(cols):
            if shipgrid[i][j] != 0:
                sumgrid[i][j] += 1


def getSumGridDivisor(runs, ship_health_sum, rows, cols, factor):

    # Integer division by a factor proportional to the number of runs
    # to make it easier to see approximate ship distribution

    # factor as input value for making adjustments
    total_ship_health = runs * ship_health_sum
    total_grid_squares = rows * cols

    if total_ship_health > (total_grid_squares*factor):
        divisor = total_ship_health // (total_grid_squares*factor)
    else:
        divisor = 1 #because otherwise division by zero

    return divisor


def updateUserEveryTenPercent(i, runs):
    #
    if i % (runs//10) == 0:
        if i != 0:
            print("Ships have been placed", i, "times out of", runs)


def normalizeSumGrid(rows, cols, sumgrid, division_factor):
    #
        for i in range(rows):
            for j in range(cols):
                sumgrid[i][j] = sumgrid[i][j] // division_factor

def printNormalizedShipDistribution(rows, cols, runs, ship_health, factor, sumgrid):

    print("Relative ship occupancy ratios of a", rows,"X", cols,"grid after", runs, "ship placements have been run:")
    print("Placed ships of length:", ship_health)
    print("Normalizing factor:", factor)
    battleship.displayGrid(sumgrid)



def debugCheckShipDistribution(rows, cols, runs, ship_health, single_direction_algorithm):
    """Check the distribution of ships generated by the addShipToShipGrid function by running it "runs" many times
    """

    print("Checking the randomness of the ship placing function by running it", runs, "many times...")


    sumgrid = [[0 for i in range(cols)] for j in range(rows)]

    ship_health_sum = 0

    for health in ship_health:
        ship_health_sum += health

    normalizing_divisor = 20 # Normalizing factor
    division_factor = getSumGridDivisor(runs, ship_health_sum, rows, cols, normalizing_divisor)


    for i in range (runs):

        shipgrid = debugSetupShipGrid(rows, cols, ship_health, single_direction_algorithm) #Put ships into ship grid
        addShipPositionsToSumGrid(shipgrid, sumgrid, rows, cols) #Add their positions to running sum

        updateUserEveryTenPercent(i, runs) # Print out progress every 10% of runs completed


    normalizeSumGrid(rows, cols, sumgrid, division_factor)
    printNormalizedShipDistribution(rows, cols, runs, ship_health, normalizing_divisor, sumgrid)




def debugTestShipOverlap(runs, single_direction_bool):
    """Test ships don't overlap when placed in a 5 x 4 grid multiple times
    """

    print("Testing ship overlap", runs, "many times...")

    rows, cols = 5, 4
    ship_health = [5, 4, 4]

    count = 0
    for i in range (runs):

        shipgrid = debugSetupShipGrid(rows, cols, ship_health, single_direction_bool)

        #If the middle row doesn't consist of unique elements (i.e. different ships)
        if len(shipgrid[2]) != len(set(shipgrid[2])):
            count += 1 #Add one to the placement failure count and show the grid of ships
            battleship.displayGrid(shipgrid)

    print("Overlapping placements:", count)

    if count > 0:
        print("Overlap test failed")
    else:
        print("Overlap test passed")


def generateTargetList(targetgrid):
    """Return a list of targets made using the 2D target grid array
    """

    target_list = []

    for row in targetgrid:
        for elem in row:
            target_list.append(elem)

    return(target_list)


def getRandomTargetFromTargetList(target_list):
    """Randomly select an element from the target list, store the element in a temporary variable,
     delete that element from the target list, then return the element stored in the temporary variable.
    """
    
    index = random.randrange(0,len(target_list))
    string = target_list[index]
    del target_list[index]
    return string


#Autorun game
def debugTestGame(test_no, algorithm_bool):
#TODO
    rows, cols = 10, 10

    count = 0
    print("Running", test_no, "test games...")

    for i in range(1, test_no+1):

        ship_health = [5, 4, 4]

        targetgrid, shipgrid, ship_count = battleship.setupGame(rows, cols, ship_health, algorithm_bool)

        target_list = generateTargetList(targetgrid)


        # testGame loop
        #1) Generate a new target
        #2) Fire at target
        while ship_count > 0:

            if len(target_list) == 0:
                #raise ValueError('No targets remaining')
                print("Game number", i, "has failed")
                count += 1
                break

            user_input = getRandomTargetFromTargetList(target_list)

            shot_outcome_string, ship_count = battleship.fireAtTarget(user_input, targetgrid, shipgrid, ship_health, ship_count)


        if i % (test_no//10) == 0:
            if (i != test_no):
                print(i, "out of", test_no, "test games finished")

    if count > 0:
        print("Games failed:", count, "out of", test_no, "completed")
    else:
        print("All test games completed successfully")


def testInputHandling():
#TODO

    input_strings_to_test = ["x", "X", "-", "J11", "Alphabet", "A100", "A1-", "1",
                            "A", "1.3", "-190.54", "+", ";",
                            " A1", "A10 ", "J1", "j10", "H5", # Five which should result in shots
                             "J10", "-", "x", "X",
                             ]

    rows, cols = 10, 10
    ship_health = [5, 4, 4]
    single_direction_algorithm = True

    targetgrid, shipgrid, ship_count = battleship.setupGame(rows, cols, ship_health, single_direction_algorithm)

    count = 0

    for user_input in input_strings_to_test:
        user_input = user_input.upper().strip()

        valid_target = battleship.checkUserInput(user_input, targetgrid) #True if input matches a target

        if valid_target == True:
            count += 1
            shot_outcome_string, ship_count = battleship.fireAtTarget(user_input, targetgrid, shipgrid, ship_health, ship_count)


    if count == 5: #5 inputs should be recognized as valid targets
        print("String input test completed successfully")
    else:
         print("Input test error", count, "tests passed")
         print("5 tests should pass")


def runtests(algorithm_bool):

    debugTestShipOverlap(10000, algorithm_bool)
    debugTestGame(1000, algorithm_bool)

    rows, cols = 10, 10
    ship_health = [5, 4, 4]
    debugCheckShipDistribution(rows, cols, 100000, ship_health, algorithm_bool)
    debugCheckShipDistribution(15, 15, 400000, ship_health, algorithm_bool)


ship_health = [3, 2, 2]
single_direction_algorithm = True
debugCheckShipDistribution(10, 10, 100000, ship_health, single_direction_algorithm)
single_direction_algorithm = False
debugCheckShipDistribution(10, 10, 100000, ship_health, single_direction_algorithm)


if __name__ == "__main__":
    #TODO

    testInputHandling()


    print("Running tests for single direction per origin ship placement algorithm")

    single_direction_algorithm = True
    runtests(single_direction_algorithm)


    print("Running tests for multiple direction per origin ship placement algorithm")

    single_direction_algorithm = False
    runtests(single_direction_algorithm)
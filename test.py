import importlib

game_code = "battleship"
battleship = importlib.import_module(game_code)

#import battleship
#print(battleship.__file__)

#print(game_code, "is the module name")
#help(game_code)
#help(battleship)
#print("dir test")
#dir(battleship)
#print("end of dir")



#def debugDisplayShips(ship_grid):
#    for row in ship_grid:
#        print (' '.join(map(str,row)))


def debugCheckShipPlacer(rows, cols, runs):
    """Test the distribution of ships generated by the PlaceShip function by running it "runs" many times
    """

    print("Testing the randomness of the ship placing function by running it", runs, "many times")


    sumgrid = [[0 for i in range(cols)] for j in range(rows)]

    for i in range (runs):

        if i % (runs//10) == 0:
            if i != 0:
                print("Ships have been placed ", i, " times out of", runs)

        shipgrid = [[0 for i in range(cols)] for j in range(rows)]
        health = []
        battleship.placeShip(shipgrid, health, 5)
        battleship.placeShip(shipgrid, health, 4)
        battleship.placeShip(shipgrid, health, 4)


        for i in range(rows):
            for j in range(cols):
                sumgrid[i][j] += shipgrid[i][j]

    # Integer division by a factor proportional to the number of runs to make it easier to see approximate ship distribution
    if runs > 50:
        division_factor = runs // 50
    else:
        division_factor = 1 #because otherwise division by zero


    for i in range(rows):
        for j in range(cols):
            sumgrid[i][j] = sumgrid[i][j] // division_factor

    #debugDisplayShips(sumgrid)
    battleship.displayGrid(sumgrid)


def debugTestShipOverlap(runs):
    """Test ships don't overlap when placed in a 5 x 3 grid multiple times
    """

    rows, cols = 5, 3

    count = 0
    for i in range (runs):

        targetgrid, shipgrid = battleship.createGrids(rows,cols)
        health = []
        battleship.placeShip(shipgrid, health, 5)
        battleship.placeShip(shipgrid, health, 4)
        battleship.placeShip(shipgrid, health, 4)

        #print(len(shipgrid[0]))
        #debugDisplayShips(shipgrid)
        #print(len(set(shipgrid[0])))

        #If the middle row doesn't consists of unique elements (different ships) then:
        if len(shipgrid[2]) != len(set(shipgrid[2])):
            #Add one to the placement failure count and show the grid of ships
            count += 1
            battleship.displayGrid(shipgrid)

    if count > 0:
        print("Overlap test failed")
    else:
        print("Overlap test passed")

    print("Overlapping placements:", count)




debugTestShipOverlap(1000)

rows, cols = 10, 10
debugCheckShipPlacer(rows, cols, 50000)




#rows, cols = 5, 3
#targetgrid, shipgrid = battleship.createGrids(rows,cols)

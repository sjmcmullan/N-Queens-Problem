import random
import time
import sys

# This will create a completely random board as a start point.
def GenerateInitialBoard(gameSize):
    board = []

    # Each queen will be at a random column. However, they will be placed on unique rows.
    for i in range(0, gameSize):
        board.append(random.randint(0, gameSize - 1))
    return board

# Takes a node as [n1, n2, ..., nm] and a file to print to.
def PrintGameBoard(node):
    gameSize = len(node)

    # This will loop through each position in the given node. If it encounters a position where
    # a queen is located, it prints a Q, or else it prints a "."
    for row in range(0, gameSize):
        for column in range(0, gameSize):
            if node[row] == column:
                print('Q', end=" ")
            else:
                print('.', end=" ")
        print(" ")

# Takes a node as [n1, n2, ..., nm] and two of it's positions to check against each other.
def CheckPosition(node, checkPos, comparePos):
    # If the change in x or the change in y is equal to 0, this means that 
    # two queens lay on the same axis as each other.
    deltaX = checkPos - comparePos
    deltaY = node[checkPos] - node[comparePos]
    # The above can be expanded to include diagonal clashes; if the change in x
    # and the change in y are equal to each other (using absolute values to disallow negatives)
    # then that means both axes have changed by the same amount and therefore two queens lay on the same diagonal.
    return deltaX == 0 or deltaY == 0 or (abs(deltaX) == abs(deltaY))

# Takes a node as [n1, n2, ..., nm]
def CalculateCurrentHeuristicCost(node):
    # A variable to count how many queens are being attacked. This is the heuristic cost value.
    clashes = 0

    # For each queen in the node, it will be checked against ALL the other queens in the node.
    # Except for itself.
    for checkPos in range(0, len(node)):
        for comparePos in range(0, len(node)):
            if comparePos != checkPos:
                # Checkpos will return true if there is a clash either horizontally, diagonally, or vertically.
                if CheckPosition(node, checkPos, comparePos) == True:
                    clashes += 1
    return clashes

# Takes a node as [n1, n2, ..., nm], the value of the parents heuristic cost and a value to keep track of how many comparisons have been made.
def GenerateBestNeighbour(parentNode, parentHeuristicCost, ):
    bestNeighbour = None
    # We initalise the best found heuristic cost value to be the same as the parents.
    bestHeuristicCost = parentHeuristicCost

    # Each queen will be moved into each position in its row. When it is moved, this is a new (neighbour) state.
    for row in range(0, len(parentNode)):
        for column in range(0, len(parentNode)):
            tmpNode = parentNode[:]

            if column != parentNode[row]:
                tmpNode[row] = column
                # We want to get the heuristic cost value of the newly created neighbour
                currentHeuristicCost = CalculateCurrentHeuristicCost(tmpNode)

                # If the heuristic cost we just created is less than (so better) than the previously recorded best one,
                # then the new best is the newly created heuristic cost and we save that node as the "best" neighbour.
                if currentHeuristicCost < bestHeuristicCost:
                    bestHeuristicCost = currentHeuristicCost
                    bestNeighbour = tmpNode
    
    return bestNeighbour, bestHeuristicCost

# Just takes the game size, n, generates a random starting board and it's heuristic cost.
def CreateInitialNode(gameSize):
    currentNode = GenerateInitialBoard(gameSize)
    currentHeuristicCost = CalculateCurrentHeuristicCost(currentNode)
    return currentNode, currentHeuristicCost

def HillClimbingSearch(gameSize):
    currentNode, currentHeuristicCost = CreateInitialNode(gameSize)
    # The path stores each "jump" i.e. the progression from start to finish.
    # Stores each node and it's heuristic cost.
    path = [(currentNode, currentHeuristicCost)]
    restartCount = 0
    
    while True:
        neighbourNode, neighbourHeuristicCost = GenerateBestNeighbour(currentNode, currentHeuristicCost, )

        # If the heuristic cost that we just created is no improvement over the last, we have hit a plateu.
        if neighbourHeuristicCost == currentHeuristicCost:
            # Restart with a brand new random node.
            restartCount += 1
            currentNode, currentHeuristicCost = CreateInitialNode(gameSize)
            path = [(currentNode, currentHeuristicCost)]
        
        else:
            # If the current node has a heuristic cost value of 0, then there are no queen attacks and we have hit a goal state.
            # Record the information and return it.
            if neighbourHeuristicCost == 0:
                path.append((neighbourNode, neighbourHeuristicCost))
                return path, restartCount
            
            # However, if it's not a goal state but an improvement, we continue.
            path.append((neighbourNode, neighbourHeuristicCost))
            currentNode = neighbourNode
            currentHeuristicCost = neighbourHeuristicCost

minBoardSize = eval(sys.argv[1])
maxBoardSize = eval(sys.argv[2])
printSolution = eval(sys.argv[3])

for x in range(minBoardSize, maxBoardSize + 1):
    startTime = time.time()
    solutionPath, failures = HillClimbingSearch(x)
    endTime = time.time()

    if printSolution == True:
        print("Solution for n=", x)
        PrintGameBoard(solutionPath[-1][0])

    print(x)
    print(endTime - startTime)
    print(len(solutionPath))
    print(failures)
    print()
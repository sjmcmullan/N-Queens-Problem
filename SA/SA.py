import random
import time
import sys
import math

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

def GenerateNeighbour(currentState):
    newState = currentState[:]
    row = random.randint(0, len(currentState) - 1)
    possiblePositions = [x for x in range(0, len(currentState)) if x != newState[row]]
    newState[row] = random.choice(possiblePositions)
    
    return newState, CalculateCurrentHeuristicCost(newState)


def SimulatedAnnealingSearch(gameSize):
    temperature = 100
    coolRate = 0.01
    currentState = GenerateInitialBoard(gameSize)
    currentCost = CalculateCurrentHeuristicCost(currentState)
    solutionPath = [(currentState, currentCost)]

    while temperature > 0:
        for x in range(0, 17001):
            neighbourState, neighbourStateCost = GenerateNeighbour(currentState)

            if neighbourStateCost < currentCost:
                if neighbourStateCost == 0:
                    return neighbourState
                else:
                    currentState = neighbourState
                    currentCost = neighbourStateCost
                    solutionPath = [(currentState, currentCost)]
            elif neighbourStateCost > currentCost:
                p = math.exp(-(neighbourStateCost - currentCost)/temperature)
                if p >= random.random():
                    currentState = neighbourState
                    currentCost = neighbourStateCost
                    solutionPath = [(currentState, currentCost)]
        
        temperature -= coolRate


minBoardSize = eval(sys.argv[1])
maxBoardSize = eval(sys.argv[2])
printSolution = eval(sys.argv[3])

for x in range(minBoardSize, maxBoardSize + 1):
    startTime = time.time()
    solution = SimulatedAnnealingSearch(x)
    endTime = time.time()

    print(x)
    if printSolution == True:
        PrintGameBoard(solution)
    print(endTime - startTime)
    print()